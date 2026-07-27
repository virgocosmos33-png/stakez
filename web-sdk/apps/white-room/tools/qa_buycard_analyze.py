"""Analyze flood-fill removal of outer black on buy cards + export PNG previews.

For each card, build a 'dark' mask (luminance <= THRESH), label connected
components, and measure the border-connected dark region. Then produce a preview
composite of the flood-filled result over a checkerboard so we can eyeball it.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage

DIR = Path("static/assets/sprites/mirror")
OUT = Path("tools/_buycard_preview")
OUT.mkdir(parents=True, exist_ok=True)

CARDS = [
    "buy_ante.webp", "buy_feature1.webp", "buy_feature2.webp",
    "buy_feature3.webp", "buy_seance.webp", "buy_otherside.webp",
    "buy_bloodmoon.webp",
]

THRESH = 40  # max-channel luminance <= this counts as "dark/background"


def border_connected_dark(alpha_rgb):
    rgb = alpha_rgb[..., :3].astype(np.int32)
    lum = rgb.max(axis=2)
    dark = lum <= THRESH
    # label 4-connected dark regions
    lbl, n = ndimage.label(dark, structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))
    # collect labels touching the border
    border_labels = set(lbl[0, :]) | set(lbl[-1, :]) | set(lbl[:, 0]) | set(lbl[:, -1])
    border_labels.discard(0)
    bg = np.isin(lbl, list(border_labels))
    return dark, bg


def checker(w, h, sq=24):
    c = np.zeros((h, w, 3), np.uint8)
    for y in range(0, h, sq):
        for x in range(0, w, sq):
            if ((x // sq) + (y // sq)) % 2 == 0:
                c[y:y+sq, x:x+sq] = 90
            else:
                c[y:y+sq, x:x+sq] = 150
    return c


for name in CARDS:
    p = DIR / name
    im = Image.open(p).convert("RGBA")
    arr = np.asarray(im)
    dark, bg = border_connected_dark(arr)
    total = bg.size
    print(f"{name:20s} dark={dark.mean():5.1%} borderBg={bg.mean():5.1%} "
          f"interiorDark={(dark & ~bg).mean():5.1%}")
    # build result: alpha 0 where bg
    out = arr.copy()
    out[..., 3] = np.where(bg, 0, 255)
    # preview over checker
    ch = checker(im.width, im.height)
    a = (out[..., 3:4] / 255.0)
    comp = (out[..., :3] * a + ch * (1 - a)).astype(np.uint8)
    Image.fromarray(comp).save(OUT / f"{name}.preview.png")

print("wrote previews to", OUT)
