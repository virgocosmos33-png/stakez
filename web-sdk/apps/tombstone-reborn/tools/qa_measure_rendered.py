"""Measure the rendered board in a shot: locate the gold border (warm px) and
the dark reel recess along the board's centre row & column.
Run: python tools/qa_measure_rendered.py <shot.png>
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
W, H = im.size
px = im.load()


def is_gold(r, g, b):
    return r > 110 and g > 80 and r - b > 35 and g - b > 10


def is_dark(r, g, b):
    return r < 40 and g < 40 and b < 45


# board is roughly centred horizontally in the canvas; scan a band of rows
cy = int(H * 0.5)
row = [px[x, cy] for x in range(W)]
gold_x = [x for x, (r, g, b) in enumerate(row) if is_gold(r, g, b)]
dark_x = [x for x, (r, g, b) in enumerate(row) if is_dark(r, g, b)]
print(f"{Path(sys.argv[1]).name}  {W}x{H}  row y={cy}")
if gold_x:
    print(f"  gold  x[{min(gold_x)}..{max(gold_x)}] ({min(gold_x)/W:.3f}..{max(gold_x)/W:.3f})")
if dark_x:
    print(f"  dark  x[{min(dark_x)}..{max(dark_x)}] ({min(dark_x)/W:.3f}..{max(dark_x)/W:.3f})")

cx = int(W * 0.5)
col = [px[cx, y] for y in range(H)]
gold_y = [y for y, (r, g, b) in enumerate(col) if is_gold(r, g, b)]
dark_y = [y for y, (r, g, b) in enumerate(col) if is_dark(r, g, b)]
if gold_y:
    print(f"  gold  y[{min(gold_y)}..{max(gold_y)}] ({min(gold_y)/H:.3f}..{max(gold_y)/H:.3f})")
if dark_y:
    print(f"  dark  y[{min(dark_y)}..{max(dark_y)}] ({min(dark_y)/H:.3f}..{max(dark_y)/H:.3f})")
