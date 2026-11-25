#!/usr/bin/env python3
"""Download every image the site uses from the Wix CDN into src/img/.

Run once (python3 razburg/tools/fetch_images.py from the repo root, or tools/fetch_images.py
in the razburg-site repo), then rebuild: build.py switches to the local copies automatically.
"""
import json, sys, time, urllib.request
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
manifest = json.loads((SRC / "images.json").read_text())
out = SRC / "img"
out.mkdir(exist_ok=True)
ok = fail = 0
for local, remote in sorted(manifest.items()):
    dest = out / local
    if dest.exists() and dest.stat().st_size > 0:
        ok += 1
        continue
    req = urllib.request.Request(remote, headers={"User-Agent": "Mozilla/5.0", "Accept": "image/jpeg,image/png,*/*"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                dest.write_bytes(r.read())
            ok += 1
            break
        except Exception as e:
            if attempt == 2:
                print("FAILED", local, e, file=sys.stderr)
                fail += 1
            time.sleep(1 + attempt)
print(f"{ok} images saved in {out}, {fail} failed")
sys.exit(1 if fail else 0)
