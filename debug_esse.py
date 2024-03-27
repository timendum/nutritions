import glob
import json

from esselunga import Esselunga

id = 5868969

esse = Esselunga()
prod = None
for jfile in glob.glob("data/*.json"):
    with open(jfile) as fi:
        products = json.load(fi)
    try:
        for _, p in products:
            if id == p["displayableProduct"]["id"]:
                prod = p
                break
    except:
        continue
if prod:
    esse._save_products([prod])
