"""Search Wikimedia Commons for candidate photos (build-time only, for manual review).
Usage: python3 tools/commons_search.py seed.json out.json [limit]
Uses the lightweight list=search API and computes thumbnail URLs locally."""
import json, sys, time, os, hashlib, urllib.parse, requests
UA = {"User-Agent": "KidsMemoryGameBuilder/1.0 (https://github.com/kimja378/kids-memory-game)"}
API = "https://commons.wikimedia.org/w/api.php"

def thumb_url(title, width=250):
    name = title.split(":", 1)[1].replace(" ", "_")
    h = hashlib.md5(name.encode()).hexdigest()
    q = urllib.parse.quote(name)
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{width}px-{q}"

def get(params):
    for wait in [0, 20, 40, 80, 160, 300]:
        time.sleep(wait)
        r = requests.get(API, headers=UA, params=params, timeout=60)
        if r.status_code == 200: return r.json()
        print("  status", r.status_code, file=sys.stderr, flush=True)
    raise SystemExit("gave up")

if __name__ == "__main__":
    seed, out = sys.argv[1], sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    res = json.load(open(out)) if os.path.exists(out) else {}
    for row in json.load(open(seed)):
        cat, iid, ko, q = row[:4]
        key = row[4] if len(row) > 4 else iid
        if key in res: continue
        d = get(dict(action="query", format="json", list="search", srnamespace=6,
                     srsearch=q + " filetype:bitmap", srlimit=limit, srprop="size"))
        cands = [dict(title=h["title"], thumb=thumb_url(h["title"])) for h in d.get("query", {}).get("search", [])
                 if h["title"].lower().endswith((".jpg", ".jpeg", ".png"))]
        res[key] = dict(cat=cat, id=iid, ko=ko, q=q, cands=cands)
        json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
        print(key, len(cands), flush=True)
        time.sleep(3)
