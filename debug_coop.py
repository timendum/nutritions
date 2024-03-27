import glob
import json

from coop import Coop

slug = "kefir-bianco-naturale-500-ml-podere-cittadella"

coop = Coop("w0d0t0")
prod = None
for jfile in glob.glob("data/*.json"):
    with open(jfile) as fi:
        products = json.load(fi)
    for p in products:
        if slug == p["slug"]:
            prod = p
            break
if prod:
    coop._save_products([prod])
