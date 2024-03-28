import glob
import json

from coop import Coop

slug = "composta-di-albicocche-270-gr-alce-nero"

coop = Coop("w0d0t0")
prod = None
for jfile in glob.glob("data/*.json"):
    with open(jfile) as fi:
        products = json.load(fi)
    try:
        for p in products:
            if slug == p.get("slug", ""):
                prod = p
                break
    except:
        continue
if prod:
    coop._save_products([prod])
