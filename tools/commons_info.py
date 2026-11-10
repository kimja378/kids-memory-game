"""Look up Wikimedia Commons file metadata (size, license, author) for many titles,
50 titles per API call, paced to respect Wikimedia rate limits (build-time only).
Usage: python3 tools/commons_info.py titles.txt out.json   (lines: key|File title)"""
import json, sys, time, os, re, html, requests
UA = {"User-Agent": "KidsMemoryGameBuilder/1.0 (https://github.com/kimja378/kids-memory-game)"}
API = "https://commons.wikimedia.org/w/api.php"
def paced_get(params):
    while True:
        r = requests.get(API, headers=UA, params=params, timeout=60)
        if r.status_code == 200: return r.json()
        wait = max(int(r.headers.get("retry-after", "30") or 30), 30)
        print("  429, waiting", wait, file=sys.stderr, flush=True); time.sleep(wait)
def strip(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
rows = [l.rstrip("\n").split("|", 1) for l in open(sys.argv[1]) if "|" in l]
out = json.load(open(sys.argv[2])) if os.path.exists(sys.argv[2]) else {}
todo = [(k, t if t.startswith("File:") else "File:" + t) for k, t in rows]
todo = [x for x in todo if x[1] not in out]
for i in range(0, len(todo), 50):
    chunk = todo[i:i+50]
    d = paced_get(dict(action="query", format="json", redirects=1, titles="|".join(t for _, t in chunk),
                       prop="imageinfo", iiprop="url|size|mime|extmetadata",
                       iiextmetadatafilter="LicenseShortName|Artist|LicenseUrl|UsageTerms|Restrictions"))
    q = d.get("query", {})
    alias = {}
    for n in q.get("normalized", []): alias[n["to"]] = n["from"]
    for rd in q.get("redirects", []): alias[rd["to"]] = alias.get(rd["from"], rd["from"])
    pages = {p["title"]: p for p in q.get("pages", {}).values()}
    for key, title in chunk:
        # find page for this title via normalization/redirect chain
        page = None
        for t, p in pages.items():
            src = t
            while src in alias: src = alias[src]
            if src == title or t == title: page = p
        rec = dict(key=key, asked=title, exists=False)
        if page and "imageinfo" in page:
            ii = page["imageinfo"][0]; em = ii.get("extmetadata", {})
            rec.update(exists=True, title=page["title"], w=ii["width"], h=ii["height"], mime=ii["mime"],
                       url=ii["url"], page=ii["descriptionurl"],
                       license=em.get("LicenseShortName", {}).get("value"),
                       license_url=em.get("LicenseUrl", {}).get("value", ""),
                       author=strip(em.get("Artist", {}).get("value")),
                       restrictions=em.get("Restrictions", {}).get("value", ""))
        out[title] = rec
    json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
    print("batch done", i, flush=True)
    time.sleep(20)
