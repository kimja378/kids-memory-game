"""Download review copies (500px thumbnails) of Commons files, paced for rate limits (build-time only).
Usage: python3 tools/commons_fetch.py info.json list.txt outdir   (list lines: key|File title)"""
import json, sys, os, time, hashlib, urllib.parse, requests
UA = {"User-Agent": "KidsMemoryGameBuilder/1.0 (https://github.com/kimja378/kids-memory-game)"}
def thumb(title, url, w, width=500):
    if w <= 700: return url
    name = title.split(":", 1)[1].replace(" ", "_"); h = hashlib.md5(name.encode()).hexdigest()
    q = urllib.parse.quote(name)
    sfx = ".jpg" if name.lower().endswith((".tif", ".tiff")) else ""
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{width}px-{q}{sfx}"
info = json.load(open(sys.argv[1])); out = sys.argv[3]; os.makedirs(out, exist_ok=True)
by_title = {r.get("title"): r for r in info.values() if r.get("exists")}
by_asked = {k: r for k, r in info.items() if r.get("exists")}
for line in open(sys.argv[2]):
    if "|" not in line: continue
    key, t = line.strip().split("|", 1); t = t if t.startswith("File:") else "File:" + t
    r = by_title.get(t) or by_asked.get(t)
    if not r: print("unknown", t, flush=True); continue
    fn = f"{out}/{key}__{hashlib.md5(r['title'].encode()).hexdigest()[:6]}.jpg"
    if os.path.exists(fn): continue
    u = thumb(r["title"], r["url"], r["w"])
    while True:
        resp = requests.get(u, headers=UA, timeout=120)
        if resp.status_code == 200: break
        if resp.status_code == 404 and u != r["url"] and r["w"] < 3000: u = r["url"]; continue
        wait = max(int(resp.headers.get("retry-after", "30") or 30), 300)
        print("  ", resp.status_code, "wait", wait, file=sys.stderr, flush=True); time.sleep(wait)
    open(fn, "wb").write(resp.content)
    json.dump(dict(key=key, title=r["title"]), open(fn + ".json", "w"), ensure_ascii=False)
    print("got", key, len(resp.content), flush=True)
    time.sleep(12)
