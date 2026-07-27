"""Fast (numpy) measurement of the frame's gold inner/outer edges + corner extent.
Run from web-sdk/apps/ways:  python tools/measure_fast.py
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
from PIL import Image

APP = Path(__file__).resolve().parent.parent
SRC = APP / "static" / "assets" / "sprites" / "mirror" / "mirror_frame_wide.png"


def bbox(mask: np.ndarray):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def main() -> None:
    im = Image.open(SRC).convert("RGBA")
    a = np.asarray(im)
    H, W, _ = a.shape
    r, g, b, al = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int), a[..., 3]
    mx = np.maximum(np.maximum(r, g), b)

    gold = (al > 40) & (mx >= 25)
    interior = (al > 40) & (mx < 25)

    gb = bbox(gold)
    ib = bbox(interior)
    print(f"size {W}x{H}")
    print(f"gold outer bbox     {gb}  -> outer margins L{gb[0]} T{gb[1]} R{W-gb[2]} B{H-gb[3]}")
    print(f"interior bbox       {ib}  -> gold INNER edge L{ib[0]} T{ib[1]} R{W-ib[2]} B{H-ib[3]}")

    # corner cluster extent: bounding box of gold within each corner QUADRANT,
    # but restricted to the region that pokes past the straight rails. We take
    # the quadrant gold bbox directly (rails are part of the corner tile anyway).
    q = 0.42
    qw, qh = int(W * q), int(H * q)
    corners = {
        "TL": gold[0:qh, 0:qw],
        "TR": gold[0:qh, W - qw:W],
        "BL": gold[H - qh:H, 0:qw],
        "BR": gold[H - qh:H, W - qw:W],
    }
    # how far the corner gold reaches inward (max, across the 4 corners)
    inx = 0
    iny = 0
    for name, m in corners.items():
        bb = bbox(m)
        # inward reach within the quadrant (distance from the OUTER corner)
        if name in ("TL", "BL"):
            rx = bb[2]  # rightmost gold col in a left quadrant
        else:
            rx = qw - bb[0]
        if name in ("TL", "TR"):
            ry = bb[3]
        else:
            ry = qh - bb[1]
        print(f"corner {name}: quadrant bbox {bb} inwardX={rx} inwardY={ry}")
        inx = max(inx, rx)
        iny = max(iny, ry)
    print(f"[corner max inward reach] X={inx} Y={iny}")
    print(f"[suggested insets] left=right={max(inx, ib[0])+8}  top=bottom={max(iny, ib[1])+8}")


if __name__ == "__main__":
    main()
