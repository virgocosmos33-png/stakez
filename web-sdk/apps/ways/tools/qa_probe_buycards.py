"""Probe the buy-bonus card webp files: size, mode, alpha stats, border sampling."""
from __future__ import annotations
from pathlib import Path
from PIL import Image
import numpy as np

DIR = Path("static/assets/sprites/mirror")
CARDS = [
    "buy_ante.webp", "buy_feature1.webp", "buy_feature2.webp",
    "buy_feature3.webp", "buy_seance.webp", "buy_otherside.webp",
    "buy_bloodmoon.webp", "buy_bonus_logo.webp",
]

for name in CARDS:
    p = DIR / name
    if not p.exists():
        print(f"[MISS] {name}")
        continue
    im = Image.open(p).convert("RGBA")
    a = np.asarray(im)
    alpha = a[..., 3]
    rgb = a[..., :3]
    total = alpha.size
    fully_transp = (alpha == 0).sum() / total
    fully_opaque = (alpha == 255).sum() / total
    # border alpha (how transparent are the edges already?)
    border = np.concatenate([
        alpha[0, :], alpha[-1, :], alpha[:, 0], alpha[:, -1]
    ])
    border_opaque = (border > 200).mean()
    # among opaque pixels, how many are near-black? (interior dark art)
    opaque_mask = alpha > 200
    if opaque_mask.any():
        lum = rgb[opaque_mask].max(axis=1)  # brightness proxy
        near_black_opaque = (lum < 24).mean()
    else:
        near_black_opaque = 0.0
    print(f"{name:22s} {str(im.size):12s} transp={fully_transp:5.1%} "
          f"opaque={fully_opaque:5.1%} borderOpaque={border_opaque:5.1%} "
          f"nearBlackOpaque={near_black_opaque:5.1%}")
