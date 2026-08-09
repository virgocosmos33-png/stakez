"""Key the flat magenta studio backdrop off the 3D royal renders and install
them as transparent RGBA masters in tools/symbol_art.

Distance keying against the measured corner colour (NOT border flood fill): the
magenta showing THROUGH the syringe's glass barrel must also clear, or the
glass reads as filled with pink. A soft alpha ramp keeps the edges clean and a
local despill greys out any leftover magenta fringe (only where r AND b exceed
g, which never matches the props' red liquid / amber glass).

Usage: python key_magenta_royals.py <src1> <dst1> [<src2> <dst2> ...]
"""

from __future__ import annotations

import sys

import numpy as np
from PIL import Image

# channel distance to the backdrop colour: fully bg below, fully prop above
BG_TOL = 60
EDGE_TOL = 110


def key(src_path: str, dst_path: str) -> None:
    img = Image.open(src_path).convert("RGBA")
    a = np.asarray(img).astype(np.int32)
    rgb = a[..., :3]

    corners = np.stack([rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]])
    bg = np.median(corners, axis=0)

    dist = np.abs(rgb - bg).max(axis=2)
    alpha = np.clip((dist - BG_TOL) * 255 // (EDGE_TOL - BG_TOL), 0, 255)

    out = a.copy()
    out[..., 3] = np.minimum(a[..., 3], alpha)

    # despill the semi-transparent edge zone: magenta fringe has r>g AND b>g
    edge = (out[..., 3] > 0) & (out[..., 3] < 255)
    fringe = edge & (rgb[..., 0] > rgb[..., 1]) & (rgb[..., 2] > rgb[..., 1])
    g = rgb[..., 1]
    out[..., 0] = np.where(fringe, g, out[..., 0])
    out[..., 2] = np.where(fringe, g, out[..., 2])

    res = Image.fromarray(out.astype(np.uint8), "RGBA")
    # pad to square so the repack contain-fit never distorts the prop
    w, h = res.size
    if w != h:
        side = max(w, h)
        sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        sq.paste(res, ((side - w) // 2, (side - h) // 2))
        res = sq
    if res.size[0] != 1024:
        res = res.resize((1024, 1024), Image.LANCZOS)
    res.save(dst_path)
    solid = (np.asarray(res)[..., 3] == 255).mean()
    print(f"{dst_path}: {res.size}, {solid:.1%} solid")


if __name__ == "__main__":
    args = sys.argv[1:]
    for s, d in zip(args[::2], args[1::2]):
        key(s, d)
