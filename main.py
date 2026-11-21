#!/usr/bin/env python3
"""news-image-20261121 entry for make.fun (@syukuran).

The program copies the pre-rendered image (entry.png, drawn by render.py
in this repository) to /output/entry.png. Standard library only,
deterministic (the same bytes on every run), no network.

Local run:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT_DIR, "entry.png")
shutil.copyfile(src, dst)
print("wrote", dst, os.path.getsize(dst), "bytes")
