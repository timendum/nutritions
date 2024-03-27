import json
import sqlite3
import sys
import xml.etree.ElementTree as ET  # noqa: N817
from http.cookiejar import MozillaCookieJar
from time import sleep
from typing import Any

import requests

KCAL_TO_KJ = 4.184


class Coop:
    def __init__(self, hash: str) -> None:
        self.hash = hash
        self._create_session()
        self._create_db()

    def _create_session(self):
        sess = requests.Session()
        cj = MozillaCookieJar()
        cj.load("cookies.txt", ignore_discard=True, ignore_expires=True)
        sess.cookies.update(cj)
        sess.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; rv:123.0) Gecko/20100101 Firefox/123.0"
        )

        def wait(hook_data, **_):
            del hook_data
            sleep(1)

        sess.hooks["response"].append(wait)

        self._sess = sess

    def _create_db(self):
        conn = sqlite3.connect("nutritions.db")

        with open("db_init.sql") as fp:
            conn.executescript(fp.read())
        conn.commit()
        self._conn = conn
        cur = conn.cursor()
        self._facts_labels = {k: v for v, k in cur.execute("SELECT id, label from nutrition_facts")}

    def get_slugs_by_category(self, category_id: int) -> list[str]:
        current_page = 1
        slugs = []
        while True:
            req = self._sess.get(
                "https://www.coopshop.it/ebsn/api/products",
                params={
                    "parent_category_id": category_id,
                    "page": current_page,
                    "page_size": 24,  # FIXME
                    "hash": self.hash,
                },
            )
            req.raise_for_status()
            jresp = req.json()
            if jresp["response"]["status"] != 0:
                raise ValueError(f"Reponse status {req.url}: {jresp}")
            slugs.extend(p["slug"] for p in jresp["data"]["products"])
            if jresp["data"]["page"]["totPages"] <= current_page:
                # all pages done
                break
            current_page += 1
        return slugs

    def _map_ninfos(self, p: Any) -> list[tuple]:
        try:
            return self._real_map_ninfos(p)
        except Exception as e:
            print(f"Error on {p.get('id', p['displayableProduct']['id'])}", e)
            return []

    def _four_td_transform(self, tree: ET.Element) -> ET.Element:
        if len([tr for tr in tree.findall(".//table[1]//tr") if len(tr.findall("td")) == 4]) < 4:
            return tree
        thd = ["".join(e.itertext()) for e in tree.findall(".//table[1]//tr[1]/td")]
        thd = [e for e in thd if e]
        if len(thd) == 2:
            for tr in tree.findall(".//table[1]//tr"):
                tds = tr.findall("td")
                if len(tds) != 4:
                    continue
                tds[0].text = " ".join((e.text for e in tds[0:2] if e.text))  # noqa: UP034
                # tds[2].text = " ".join((e.text for e in tds[2:4] if e.text))
                tr.remove(tds[3])
                tr.remove(tds[1])
        elif len(thd) == 3:
            for tr in tree.findall(".//table[1]//tr"):
                tds = tr.findall("td")
                if len(tds) != 4:
                    continue
                tr.remove(tds[2])
                tr.remove(tds[3])
        return tree

    @staticmethod
    def handle_kcal(v: str):
        if "kcal" in v:
            if "/" in v:
                v = v.replace("/", "-")
            if v.count(" ") == 3:
                inner = v.split(" ")
                v = " ".join(inner[0:2]) + " - " + " ".join(inner[2:4])
            if v.count(" ") == 1 and "kj" in v:
                v = v.replace(" ", "-")
            if "-" in v:
                for inner in v.split("-"):
                    if "kcal" in inner:
                        v = " ".join(
                            [c.strip() for c in inner.strip(" \t\n()").split("kcal") if c.strip()]
                            + ["kcal"]
                        ).strip()
                        break
            else:
                v = " ".join(
                    [c.strip() for c in v.strip().split("kcal") if c.strip()] + ["kcal"]
                ).strip()
        elif "kj" in v:
            # kJ to kCal
            v = v.split(" ")[0]
            v = v.replace(",", ".")
            try:
                v = str(float(v) / KCAL_TO_KJ)
            except ValueError:
                v = str(float(v.replace("kj", "").strip()) / KCAL_TO_KJ)
        return v

    @staticmethod
    def _prase_value(v: str) -> float | None:
        v = Coop.handle_kcal(v)
        if v.replace(",", ".").replace(" ", "").startswith("<0."):
            v = "0"
        else:
            v = v.split(" ")[0]
            v = v.replace(",", ".")
        if not v:
            return None
        if "µ" in v:
            return None
        if v.endswith("mg"):
            return float(v.replace("mg", "").strip()) / 1000
        try:
            val = float(v)
        except ValueError:
            val = float(v[:-1])

        return val

    def _real_map_ninfos(self, p: Any) -> list[tuple]:
        try:
            xml = p["metaData"]["product_description"]["NUTRITIONAL_INFO"]
        except KeyError:
            print(f"No Nutritional Info for {p['slug']}")
            return []
        xml = xml.replace("&nbsp;", " ").replace("&deg;", " ").replace("&egrave;", "e")
        tree = ET.fromstring("<root>" + xml + "</root>")
        tree = self._four_td_transform(tree)
        rows = [
            ("".join(e[0].itertext()), "".join(e[1].itertext()))
            for e in tree.findall(".//table[1]//tr")
            if len(e) >= 2
        ]
        if "100" not in "".join(tree.find(".//table[1]//tr").itertext()):
            if tree.find(".//p") and "100" not in "".join(tree.find(".//p").itertext()):
                raise ValueError(
                    f"Not 100 for {p['slug']} in {''.join(tree.find('table[1]//tr').itertext())}"
                )
        infos = []
        for row in rows:
            t, v = row
            t, v = t.lower().replace("di cui", "").strip("-:* \t\n"), v.strip().lower()
            if "100 g" in v:
                continue
            if not any([c.isnumeric() for c in v]):
                continue
            if not t:
                continue

            val = self._prase_value(v)
            if val is None:
                continue
            try:
                infos.append((p["id"], val, self._facts_labels[t]))
            except KeyError:
                print(f"Missing {repr(t)} on {p['slug']}")
        return infos

    def get_products(self, slugs: list[str]) -> list[dict[str, Any]]:
        products = []
        for slug in slugs:
            req = self._sess.get(
                "https://www.coopshop.it/ebsn/api/products",
                params={"slug": slug, "hash": self.hash},
            )
            req.raise_for_status()
            jresp = req.json()
            if jresp["response"]["status"] != 0:
                raise ValueError(f"Reponse status {req.url}: {jresp}")
            p = jresp["data"]
            products.append(p)

        return products

    def _save_products(self, products: list[Any]):
        self._conn.executemany(
            """
            INSERT OR REPLACE INTO products(id,[name],slug,short,brand,[description],price,code,source)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                (
                    p["id"],
                    p["name"],
                    p["slug"],
                    f"{p.get('priceUmDisplay', '?')} €/{p['weightUnitDisplay']}",
                    p["shortDescr"],
                    p["description"],
                    int(p.get("price", 0) * 100),
                    p["code"],
                    "COOP",
                )
                for p in products
            ),
        )
        self._conn.executemany(
            """
            INSERT OR REPLACE INTO item_menu(product_id, menu_id)
            VALUES (?,?)""",
            ((p["id"], p["categoryId"]) for p in products),
        )
        self._conn.executemany(
            """
            INSERT OR REPLACE INTO product_facts(fact_id, product_id, unit_value)
            SELECT nf.id, ?, ? from nutrition_facts as nf where nf.id = ? and nf.id > 0""",
            (ninfos for p in products for ninfos in self._map_ninfos(p)),
        )
        self._conn.commit()
        return products

    def category_by_slug(self, slug: str):
        """Fetch and save"""
        req = self._sess.get(
            "https://www.coopshop.it/ebsn/api/category",
            params={"slug": slug, "hash": self.hash},
        )
        req.raise_for_status()
        jresp = req.json()
        if jresp["response"]["status"] != 0:
            raise ValueError(f"Reponse status {req.url}: {jresp}")
        c = jresp["data"]["category"]
        # Insert category
        self._conn.execute(
            """
            INSERT OR REPLACE INTO menus(id, name, slug, parent_id)
            VALUES(?, ?, ?, ?)""",
            (c["categoryId"], c["name"], c["slug"], None),
        )
        # Insert child category
        self._conn.executemany(
            """
            INSERT OR REPLACE INTO menus(id, name, slug, parent_id)
            VALUES(?, ?, ?, ?)""",
            (
                (i["categoryId"], i["name"], i["slug"], c["categoryId"])
                for i in c.get("children", [])
            ),
        )
        self._conn.commit()
        return c["categoryId"]

    def parse(self, category_slug: str):
        filename = "".join(c if c.isalnum() else "-" for c in category_slug).strip("-")
        try:
            with open(f"data\\{filename}.json") as fi:
                products = json.load(fi)
            _ = self.category_by_slug(category_slug)
        except FileNotFoundError:
            category = self.category_by_slug(category_slug)
            pids = self.get_slugs_by_category(category)
            products = self.get_products(pids)
            with open(f"data\\{filename}.json", "w") as fo:
                json.dump(products, fo)
        self._save_products(products)


def main():
    category = sys.argv[1]
    hash = sys.argv[2]
    coop = Coop(hash)
    coop.parse(category)


if __name__ == "__main__":
    main()
