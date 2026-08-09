"""Key the flat black studio background out of the 3D royal renders.

The generated props sit on a vignetted near-black backdrop. Contain-fitting that
whole square into a card leaves a visible darker rectangle inside the cell (the
render's own background, a different black from the reel cell). We only want the
PROP, so we flood the connected background from the borders to transparent and
keep the object — even where the object itself is dark — because the object is
enclosed by its own bright rim and is never reached by the border flood.

Usage:
    python tools/debg_royals.py IN.png OUT.png [--thresh N] [--feather F]
"""

from __future__ import annotations

import argparse
from collections import deque

import numpy as np
from PIL import Image, ImageFilter


def remove_bg(img: Image.Image, thresh: int, feather: float) -> Image.Image:
    img = img.convert("RGBA")
    w, h = img.size
    a = np.asarray(img)
    lum = a[..., :3].astype(np.int32).mean(axis=2)

    # Background = near-black pixels CONNECTED to the border. A BFS from every
    # border pixel that is under threshold floods the surrounding backdrop but
    # cannot cross the prop's brighter edges, so dark interiors of the prop stay.
    dark = lum < thresh
    bg = np.zeros((h, w), dtype=bool)
    dq: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            if dark[y, x] and not bg[y, x]:
                bg[y, x] = True
                dq.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if dark[y, x] and not bg[y, x]:
                bg[y, x] = True
                dq.append((x, y))
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and dark[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True
                dq.append((nx, ny))

    alpha = np.where(bg, 0, 255).astype(np.uint8)
    alpha_img = Image.fromarray(alpha, "L")
    if feather > 0:
        alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(feather))

    out = img.copy()
    out.putalpha(alpha_img)
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--thresh", type=int, default=48)
    p.add_argument("--feather", type=float, default=1.0)
    args = p.parse_args()
    remove_bg(Image.open(args.src), args.thresh, args.feather).save(args.dst)
    print(f"wrote {args.dst}")
