"""Crop a region from a shot for close inspection.
Run: python tools/qa_crop.py <src.png> <out.png> <left> <top> <right> <bottom>
Coords are fractions (0..1) of the image.
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image

src, out = Path(sys.argv[1]), Path(sys.argv[2])
l, t, r, b = (float(x) for x in sys.argv[3:7])
im = Image.open(src).convert("RGB")
W, H = im.size
crop = im.crop((int(l * W), int(t * H), int(r * W), int(b * H)))
# upscale x2 for visibility
crop = crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST)
crop.save(out)
print(f"[crop] {out} <- {src.name} ({crop.size})")
