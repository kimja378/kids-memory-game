#!/usr/bin/env python3
"""Validate assets/images/catalog.json against the image files on disk.

Checks: required fields, lowercase file names, file exists, image decodes fully
(detects truncated/corrupt files), minimum resolution, file size budget,
duplicate ids / files / identical image content, orphan files, and that every
category has at least 3 distinct names (one game question needs 3 cards).

Usage:
  python3 tools/validate_images.py                 # validate, exit 1 on error
  python3 tools/validate_images.py --write-credits # also regenerate CREDITS.md
"""
import json, os, re, sys, hashlib
from collections import defaultdict
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "assets/images/catalog.json")
DIRS = {"animal": "animals", "fruit": "fruits", "veg": "vegetables", "vehicle": "vehicles"}
MIN_SIDE, MAX_BYTES = 150, 250_000
ID_RE = re.compile(r"^[a-z0-9_]+$")

def main():
    errors, warnings = [], []
    try:
        cat = json.load(open(CATALOG, encoding="utf-8"))
    except Exception as e:
        print("ERROR: catalog.json unreadable:", e); return 1
    items = cat.get("items", [])
    ids, files, hashes = set(), set(), {}
    names = defaultdict(set); photos = defaultdict(int)
    for it in items:
        tag = it.get("id", "?")
        for k in ("id", "name", "category", "file", "source"):
            if not it.get(k): errors.append(f"{tag}: missing field '{k}'")
        if not ID_RE.match(it.get("id", "")): errors.append(f"{tag}: id must be lowercase a-z0-9_")
        if it.get("category") not in DIRS: errors.append(f"{tag}: bad category {it.get('category')}"); continue
        f = it.get("file", "")
        exp = f"assets/images/{DIRS[it['category']]}/{it['id']}.jpg"
        if f != exp: errors.append(f"{tag}: file should be {exp} (got {f})")
        if f != f.lower(): errors.append(f"{tag}: file name not lowercase")
        if tag in ids: errors.append(f"{tag}: duplicate id")
        if f in files: errors.append(f"{tag}: duplicate file")
        ids.add(tag); files.add(f)
        p = os.path.join(ROOT, f)
        if not os.path.isfile(p): errors.append(f"{tag}: MISSING file {f}"); continue
        size = os.path.getsize(p)
        if size > MAX_BYTES: warnings.append(f"{tag}: large file {size} bytes")
        try:
            with Image.open(p) as im: im.verify()
            with Image.open(p) as im:
                im.load(); w, h = im.size; fmt = im.format
            if fmt != "JPEG": errors.append(f"{tag}: not a JPEG ({fmt})")
            if min(w, h) < MIN_SIDE: errors.append(f"{tag}: too small {w}x{h}")
        except Exception as e:
            errors.append(f"{tag}: CORRUPT image ({e})"); continue
        hsh = hashlib.sha1(open(p, "rb").read()).hexdigest()
        if hsh in hashes: errors.append(f"{tag}: identical image content to {hashes[hsh]}")
        hashes[hsh] = tag
        src = it.get("source", {})
        if src.get("license") in (None, "", "unknown"):
            warnings.append(f"{tag}: license unknown (legacy upload)")
        names[it["category"]].add(it["name"]); photos[it["category"]] += 1
    for d in DIRS.values():
        full = os.path.join(ROOT, "assets/images", d)
        for fn in sorted(os.listdir(full)) if os.path.isdir(full) else []:
            if f"assets/images/{d}/{fn}" not in files: warnings.append(f"orphan file not in catalog: {d}/{fn}")
    print("category   photos  distinct-names")
    for c in DIRS:
        print(f"{c:10} {photos[c]:6}  {len(names[c]):6}")
        if len(names[c]) < 3: errors.append(f"category {c} has fewer than 3 distinct names")
    for w in warnings: print("WARN:", w)
    for e in errors: print("ERROR:", e)
    print(f"{len(items)} items, {len(errors)} errors, {len(warnings)} warnings")
    if "--write-credits" in sys.argv: write_credits(items)
    return 1 if errors else 0

def write_credits(items):
    L = ["# 사진 출처 및 라이선스 (Photo credits)", "",
         "이 파일은 `python3 tools/validate_images.py --write-credits` 로 `assets/images/catalog.json` 에서 자동 생성됩니다.", "",
         "Wikimedia Commons 사진은 각 라이선스 조건에 따라 저작자 표시와 함께 사용하며, 크기 축소(및 일부 잘라내기)만 했습니다.", "",
         "| 분류 | 이름 | 파일 | 원본 | 저작자 | 라이선스 |", "|---|---|---|---|---|---|"]
    for it in items:
        s = it["source"]
        orig = f"[{s['title'].replace('|','/')}]({s['url']})" if s.get("url") else s.get("title", "")
        lic = f"[{s['license']}]({s['license_url']})" if s.get("license_url") else (s.get("license") or "")
        author = (s.get("author") or "").replace("|", "/").replace("\n", " ")
        L.append(f"| {it['category']} | {it['name']} | `{it['file']}` | {orig} | {author} | {lic} |")
    open(os.path.join(ROOT, "CREDITS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote CREDITS.md")

if __name__ == "__main__":
    sys.exit(main())
