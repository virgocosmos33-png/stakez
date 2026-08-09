"""Scan the CURRENT mirror_frame.png alpha along the central row & column to
report the true transparent opening vs opaque gold border runs."""
from __future__ import annotations
from pathlib import Path
from PIL import Image

ASSET = (Path(__file__).resolve().parents[1] / "static" / "assets" / "sprites"
         / "mirror" / "mirror_frame.png")
im = Image.open(ASSET).convert("RGBA")
W, H = im.size
px = im.load()


def runs(vals):
    """list of (start,end,opaque?) runs where opaque == alpha>=128"""
    out = []
    s = 0
    cur = vals[0] >= 128
    for i in range(1, len(vals)):
        o = vals[i] >= 128
        if o != cur:
            out.append((s, i - 1, cur))
            s = i
            cur = o
    out.append((s, len(vals) - 1, cur))
    return out


cy = H // 2
row = [px[x, cy][3] for x in range(W)]
print(f"ROW y={cy} (W={W}):")
for s, e, o in runs(row):
    if e - s > 3:
        print(f"  {'GOLD' if o else 'open'} x[{s}..{e}] ({s/W:.3f}..{e/W:.3f}) len={e-s}")

cx = W // 2
col = [px[cx, y][3] for y in range(H)]
print(f"COL x={cx} (H={H}):")
for s, e, o in runs(col):
    if e - s > 3:
        print(f"  {'GOLD' if o else 'open'} y[{s}..{e}] ({s/H:.3f}..{e/H:.3f}) len={e-s}")
