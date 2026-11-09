"""Build-time image pipeline (NOT used by the web app at runtime).

Inputs
  tools/selections.json : {id: {"name": 한글이름, "category": fruit|veg|animal|vehicle,
                                "commons": "<Wikimedia Commons file name>"  or  "ov": "<openverse key>/<index>",
                                "crop": [left, top, right, bottom] as fractions (optional)}}
  info.json / ov.json   : metadata gathered by tools/commons_info.py and tools/openverse_search.py
  review dirs           : downloaded copies from tools/commons_fetch.py (rev/) and openverse_search.py (ov/)

Output
  assets/images/<category dir>/<id>.jpg  (long side max 500px, JPEG q80, EXIF stripped)
  assets/images/catalog.json             (name <-> file mapping + source/license)

Usage: python3 tools/build_images.py tools/selections.json SCRATCH_DIR
       (SCRATCH_DIR contains info.json, ov.json, rev/, ov/)
"""
import json, sys, os, hashlib
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = {"animal": "animals", "fruit": "fruits", "veg": "vegetables", "vehicle": "vehicles"}
MAX_SIDE = 500
CC = {"by": "CC BY", "by-sa": "CC BY-SA", "cc0": "CC0", "pdm": "Public Domain Mark"}

def main():
    sel = json.load(open(sys.argv[1], encoding="utf-8"))
    scratch = sys.argv[2]
    info = json.load(open(f"{scratch}/info.json", encoding="utf-8"))
    ov = json.load(open(f"{scratch}/ov.json", encoding="utf-8"))
    cat_path = os.path.join(ROOT, "assets/images/catalog.json")
    catalog = json.load(open(cat_path, encoding="utf-8"))
    by_id = {e["id"]: e for e in catalog["items"]}
    for iid, s in sel.items():
        if "commons" in s:
            r = info["File:" + s["commons"]]
            src = f"{scratch}/rev/{iid}__{hashlib.md5(r['title'].encode()).hexdigest()[:6]}.jpg"
            source = dict(title=r["title"], url=r["page"], author=r.get("author") or "",
                          license=r.get("license") or "", license_url=r.get("license_url") or "",
                          via="Wikimedia Commons")
        else:
            key, idx = s["ov"].split("/")
            c = ov[key]["cands"][int(idx)]
            src = f"{scratch}/ov/{key}__{idx}.jpg"
            lic = CC.get(c["license"], c["license"].upper())
            if c["license"] not in ("cc0", "pdm"): lic += " " + (c.get("license_version") or "")
            source = dict(title=c.get("title") or "", url=c.get("foreign_landing_url") or "",
                          author=c.get("creator") or f"({c.get('source')})", license=lic.strip(),
                          license_url=c.get("license_url") or "", via=f"Openverse ({c.get('source')})")
            assert c["license"] in CC, (iid, c["license"])
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        if s.get("crop"):
            l, t, rr, b = s["crop"]; W, H = im.size
            im = im.crop((int(l * W), int(t * H), int(rr * W), int(b * H)))
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        out_rel = f"assets/images/{DIRS[s['category']]}/{iid}.jpg"
        im.save(os.path.join(ROOT, out_rel), "JPEG", quality=80, optimize=True, progressive=True)
        source["modified"] = ("cropped, " if s.get("crop") else "") + f"resized to max {MAX_SIDE}px JPEG"
        by_id[iid] = dict(id=iid, name=s["name"], category=s["category"], file=out_rel, source=source)
    order = {"fruit": 0, "veg": 1, "animal": 2, "vehicle": 3}
    catalog["items"] = sorted(by_id.values(), key=lambda e: (order[e["category"]], e["id"]))
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=1); f.write("\n")
    print("catalog items:", len(catalog["items"]))

if __name__ == "__main__":
    main()
