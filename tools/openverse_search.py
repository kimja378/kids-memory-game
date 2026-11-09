"""Search Openverse (https://openverse.org, CC-licensed media) for candidate photos and download
their 600px thumbnails for manual review (build-time only; the app never calls Openverse).
Only licenses that allow modification and commercial use are requested (CC0, PDM, BY, BY-SA).
Usage: python3 tools/openverse_search.py seed.json out.json reviewdir [per_item]
seed rows: [category, id, 한글이름, "english query", {optional extra API params}]"""
import json, sys, os, time, io, requests
from PIL import Image
UA = {"User-Agent": "KidsMemoryGameBuilder/1.0 (https://github.com/kimja378/kids-memory-game)"}
API = "https://api.openverse.org/v1/images/"
def get(url, **params):
    while True:
        r = requests.get(url, headers=UA, params=params, timeout=90)
        if r.status_code != 429: return r
        print("  429", r.headers.get("retry-after"), file=sys.stderr, flush=True)
        time.sleep(max(int(r.headers.get("retry-after", "60") or 60), 30))
seed, out, rev = sys.argv[1], sys.argv[2], sys.argv[3]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 8
os.makedirs(rev, exist_ok=True)
res = json.load(open(out)) if os.path.exists(out) else {}
for row in json.load(open(seed)):
    cat, iid, ko, q = row[:4]; extra = row[4] if len(row) > 4 else {}
    if iid not in res:
        r = get(API, q=q, page_size=20, license_type="commercial,modification", category="photograph", mature="false", **extra)
        if r.status_code != 200: print("search fail", iid, r.status_code, r.text[:200], flush=True); continue
        rows = [x for x in r.json()["results"] if x.get("source") != "wikimedia"][:n]
        res[iid] = dict(cat=cat, ko=ko, q=q, cands=[{k: x.get(k) for k in ("id", "title", "url", "foreign_landing_url",
                   "creator", "creator_url", "license", "license_version", "license_url", "source", "width", "height",
                   "thumbnail", "attribution")} for x in rows])
        json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
        time.sleep(4)
    for i, c in enumerate(res[iid]["cands"]):
        fn = f"{rev}/{iid}__{i}.jpg"
        if os.path.exists(fn): continue
        r = get(c["thumbnail"])
        if r.status_code != 200: print("  thumb fail", iid, i, r.status_code, flush=True); continue
        try:
            Image.open(io.BytesIO(r.content)).convert("RGB").save(fn, "JPEG", quality=92)
        except Exception as e:
            print("  bad thumb", iid, i, e, flush=True)
        time.sleep(1)
    print("done", iid, len(res[iid]["cands"]), flush=True)
