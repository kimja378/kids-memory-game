"""Build feature-detective object photos (build-time only; the page never loads external images).
Usage: python3 tools/build_fd_images.py tools/fd_selections.json SCRATCH_DIR
SCRATCH_DIR holds fd.json (tools/openverse_search.py output) and fd/ review copies.
Writes feature-detective/assets/images/<id>.jpg (max 480px JPEG) and feature-detective/assets/images/credits.json,
then regenerates feature-detective/CREDITS.md."""
import json, sys, os
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "feature-detective/assets/images")
CC = {"by": "CC BY", "by-sa": "CC BY-SA", "cc0": "CC0", "pdm": "Public Domain Mark"}
sel = json.load(open(sys.argv[1], encoding="utf-8")); scratch = sys.argv[2]
ov = json.load(open(f"{scratch}/fd.json", encoding="utf-8"))
os.makedirs(OUT, exist_ok=True)
cpath = os.path.join(OUT, "credits.json")
credits = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
for iid, s in sel.items():
    k, n = s["ov"].split("/"); c = ov[k]["cands"][int(n)]
    assert c["license"] in CC, (iid, c["license"])
    im = ImageOps.exif_transpose(Image.open(f"{scratch}/fd/{k}__{n}.jpg")).convert("RGB")
    if s.get("crop"):
        l, t, r, b = s["crop"]; W, H = im.size
        im = im.crop((int(l*W), int(t*H), int(r*W), int(b*H)))
    im.thumbnail((480, 480), Image.LANCZOS)
    im.save(f"{OUT}/{iid}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    lic = CC[c["license"]] + ("" if c["license"] in ("cc0", "pdm") else " " + (c.get("license_version") or ""))
    credits[iid] = dict(name=s["name"], file=f"assets/images/{iid}.jpg", title=c.get("title") or "",
        url=c.get("foreign_landing_url") or "", author=c.get("creator") or f"({c.get('source')})",
        license=lic.strip(), license_url=c.get("license_url") or "", via=f"Openverse ({c.get('source')})",
        modified=("cropped, " if s.get("crop") else "") + "resized to max 480px JPEG")
json.dump(dict(sorted(credits.items())), open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L = ["# 특징 탐정 놀이 — 생활 물건 사진 출처", "", "`feature-detective/assets/images/credits.json` 에서 자동 생성됩니다. 모든 사진은 크기 축소(일부 잘라내기)만 했습니다.", "",
     "| 이름 | 파일 | 원본 | 저작자 | 라이선스 |", "|---|---|---|---|---|"]
for iid, c in sorted(credits.items()):
    lic = f"[{c['license']}]({c['license_url']})" if c["license_url"] else c["license"]
    L.append(f"| {c['name']} | `{c['file']}` | [{(c['title'] or iid).replace('|','/')}]({c['url']}) | {c['author'].replace('|','/')} | {lic} |")
open(os.path.join(ROOT, "feature-detective/CREDITS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("built", len(sel), "credits total", len(credits))
