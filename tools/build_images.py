"""Build-time image pipeline (NOT used by the web app at runtime).

Inputs
  tools/selections.json : {id: {"name": 한글이름, "category": fruit|veg|animal|vehicle,
                                "title": "File:... on Wikimedia Commons", "crop": [l,t,r,b] fractions (optional)}}
  <info.json>           : Commons metadata gathered by tools/commons_info.py
  <review dir>          : downloaded copies from tools/commons_fetch.py

Output
  assets/images/<category dir>/<id>.jpg  (max 500px, JPEG q80, metadata stripped)
  assets/images/catalog.json             (name <-> file mapping + source/license)

Usage: python3 tools/build_images.py tools/selections.json info.json reviewdir
"""
import json, sys, os, glob, hashlib
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = {"animal": "animals", "fruit": "fruits", "veg": "vegetables", "vehicle": "vehicles"}
MAX_SIDE = 500

def main():
    sel = json.load(open(sys.argv[1], encoding="utf-8"))
    info = json.load(open(sys.argv[2], encoding="utf-8"))
    by_title = {r["title"]: r for r in info.values() if r.get("exists")}
    review = sys.argv[3]
    cat_path = os.path.join(ROOT, "assets/images/catalog.json")
    catalog = json.load(open(cat_path, encoding="utf-8"))
    by_id = {e["id"]: e for e in catalog["items"]}
    for iid, s in sel.items():
        r = by_title[s["title"]]
        src = f"{review}/{s.get('key', iid)}__{hashlib.md5(r['title'].encode()).hexdigest()[:6]}.jpg"
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        if s.get("crop"):
            l, t, rr, b = s["crop"]; W, H = im.size
            im = im.crop((int(l * W), int(t * H), int(rr * W), int(b * H)))
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        out_rel = f"assets/images/{DIRS[s['category']]}/{iid}.jpg"
        im.save(os.path.join(ROOT, out_rel), "JPEG", quality=80, optimize=True, progressive=True)
        by_id[iid] = dict(id=iid, name=s["name"], category=s["category"], file=out_rel, source=dict(
            title=r["title"], url=r["page"], author=r.get("author") or "",
            license=r.get("license") or "", license_url=r.get("license_url") or "",
            modified=("cropped and " if s.get("crop") else "") + f"resized to max {MAX_SIDE}px JPEG"))
    order = {"fruit": 0, "veg": 1, "animal": 2, "vehicle": 3}
    catalog["items"] = sorted(by_id.values(), key=lambda e: (order[e["category"]], e["id"]))
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=1); f.write("\n")
    print("catalog items:", len(catalog["items"]))

if __name__ == "__main__":
    main()
