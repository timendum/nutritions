from itertools import product
import json
import sqlite3
import sys
import xml.etree.ElementTree as ET  # noqa: N817
from typing import Any

from coop import Coop


class Esselunga(Coop):
    def __init__(self) -> None:
        self._create_db()

    def _create_session(self):
        self._sess = None

    def parse(self, filename: str):
        with open(filename) as fp:
            jdata = json.load(fp)
        products = [x[1] for x in jdata]
        self._save_categories(products)
        self._save_products(products)

    def _save_categories(self, products: list[Any]):
        for p in products:
            # Insert missing menu
            self._conn.executemany(
                """
            INSERT OR REPLACE INTO menus(id, name, parent_id)
            VALUES (?, ?, ?)""",
                [
                    (m["menuItemId"], m["label"], m["parentMenuItemId"])
                    for m in p["displayableProduct"]["menuItemPath"]
                ],
            )

    def _real_map_ninfos(self, p: Any) -> list[tuple]:
        # Search for Nutritional Facts
        for infos in p["informations"]:
            if infos["label"].strip().lower() != "valori nutrizionali":
                continue
            # fix XML
            infos["value"] = (
                infos["value"]
                .replace("<0,", "&lt;0,")
                .replace("<0.", "&lt;0,")
                .replace("< 0", "&lt; 0")
                .replace("<1", "&lt;1")
            )
            tree = ET.fromstring("<root>" + infos["value"] + "</root>")
            trs = tree.findall("table/tbody/tr")
            ths = tree.findall("table/thead/tr/th")
            headings = "".join(ths[1].itertext()).strip().lower()
            if (
                "100" not in headings
                and "dichiarazione nutrizionale" not in headings
                and "informazioni nutrizionali" not in headings
            ):
                raise ValueError("".join(ths[1].itertext()))
            ret = []
            for tds in trs:
                val = self.tr_to_data(tds)
                if val is None:
                    continue
                label = "".join(tds[0].itertext()).lower().replace("di cui", "").strip(":-()* \t")
                if not label:
                    continue
                try:
                    ret.append((p["displayableProduct"]["id"], val, self._facts_labels[label]))
                except KeyError:
                    print(f"Missing {repr(label)} on {p['displayableProduct']['id']}")
            return ret
        raise ValueError("Missing Valori nutrizionali")

    def _save_products(self, products: list[Any]):
        self._conn.executemany(
            """
            INSERT OR REPLACE INTO products(id,[name],slug,short,brand,[description],price,code,source)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                (
                    p["displayableProduct"]["id"],
                    p["displayableProduct"]["description"],
                    p["displayableProduct"]["code"],
                    p["displayableProduct"]["label"],
                    p["displayableProduct"]["brand"],
                    f"{p['displayableProduct']['unitValue']} {p['displayableProduct']['unitText']}",
                    int(p["displayableProduct"].get("price", 0) * 100),
                    p["displayableProduct"]["barcode"],
                    "ESSELUNGA",
                )
                for p in products
            ),
        )
        self._conn.executemany(
            """
            INSERT OR REPLACE INTO item_menu(product_id, menu_id)
            VALUES (?,?)""",
            [
                (
                    p["displayableProduct"]["id"],
                    p["displayableProduct"]["menuItemPath"][-1]["menuItemId"],
                )
                for p in products
            ],
        )
        self._conn.executemany(
            """
            INSERT OR REPLACE INTO product_facts(fact_id, product_id, unit_value)
            SELECT nf.id, ?, ? from nutrition_facts as nf where nf.id = ? and nf.id > 0""",
            (ninfos for p in products for ninfos in self._map_ninfos(p)),
        )
        self._conn.commit()
        return products

    def tr_to_data(self, tds):
        v = "".join(tds[1].itertext()).strip().strip("()*").lower()
        return self._prase_value(v)


def main():
    esselunga = Esselunga()
    esselunga.parse(sys.argv[1])


if __name__ == "__main__":
    main()
