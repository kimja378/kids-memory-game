"""Download 250px candidate thumbnails and build labeled contact sheets for manual review (build-time only)."""
import json, sys, os, time, requests, subprocess
UA = {"User-Agent": "KidsMemoryGameBuilder/1.0 (https://github.com/kimja378/kids-memory-game)"}
cands_file, outdir = sys.argv[1], sys.argv[2]
keys = sys.argv[3].split(",") if len(sys.argv) > 3 else None
os.makedirs(outdir, exist_ok=True)
data = json.load(open(cands_file))
for key, it in data.items():
    if keys and key not in keys: continue
    files = []
    for i, c in enumerate(it["cands"]):
        fn = f"{outdir}/{key}_{i}.jpg"
        if not os.path.exists(fn) and c.get("thumb"):
            for wait in [0, 10, 30, 60]:
                time.sleep(wait)
                r = requests.get(c["thumb"], headers=UA, timeout=60)
                if r.status_code == 200:
                    open(fn, "wb").write(r.content); break
                print("thumb", r.status_code, key, i, file=sys.stderr)
            time.sleep(1)
        if os.path.exists(fn): files.append(fn)
    if files:
        args = ["montage"]
        for f in files:
            i = f.rsplit("_", 1)[1].split(".")[0]
            args += ["-label", f"{i}", f]
        args += ["-tile", "8x1", "-geometry", "180x180+3+3", "-pointsize", "20", "-title", f"{key} {it['ko']}", f"{outdir}/sheet_{key}.jpg"]
        subprocess.run(args, check=False)
        print("sheet", key, flush=True)
