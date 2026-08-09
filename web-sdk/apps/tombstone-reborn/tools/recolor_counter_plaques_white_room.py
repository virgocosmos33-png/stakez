"""Recolor Madam purple-gem counter plaques to white/silver clinical (alpha-preserving)."""
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parents[1] / "static" / "assets" / "sprites" / "mirror"


def recolor(name: str) -> None:
    p = BASE / name
    im = Image.open(p).convert("RGBA")
    arr = np.asarray(im).astype(np.float32)
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    purple = (a > 20) & (b > r + 12) & (b > g + 12) & (b > 70)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    silver = np.clip(lum * 1.15 + 40, 0, 255)
    r2, g2, b2 = r.copy(), g.copy(), b.copy()
    r2[purple] = silver[purple]
    g2[purple] = silver[purple] * 0.98
    b2[purple] = np.minimum(255, silver[purple] * 1.02)
    out = np.stack([r2, g2, b2, a], axis=-1).astype(np.uint8)
    bak = BASE / name.replace(".png", "_madam_bak.png")
    if not bak.exists():
        im.save(bak)
    Image.fromarray(out, "RGBA").save(p)
    px = list(Image.fromarray(out, "RGBA").getdata())
    n = len(px)
    purple_n = sum(1 for rr, gg, bb, aa in px if aa > 40 and bb > rr + 20 and bb > gg + 20 and bb > 80)
    print(f"{name}: purple%={100 * purple_n / n:.2f} bak={bak.name}")


if __name__ == "__main__":
    for name in ("ways_frame.png", "fs_frame.png"):
        recolor(name)
