"""Print the gold-border DEPTH profile along the top edge and left edge so we can
read off (a) the corner-cluster extent and (b) the plain-rail thickness and
(c) the centre-cartouche depth -- to pick nine-slice insets by hand.

depth(col) = deepest gold pixel from that edge (inner tip of the ornament),
found by scanning from mid inward-out. gold = opaque & max(r,g,b) >= 25.

Run from web-sdk/apps/ways:  python tools/profile_frame_depth.py
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image

APP = Path(__file__).resolve().parent.parent
SRC = APP / "static" / "assets" / "sprites" / "mirror" / "mirror_frame_wide.png"

ALPHA_T = 40
DARK = 25


def main() -> None:
    im = Image.open(SRC).convert("RGBA")
    W, H = im.size
    px = im.load()

    def gold(x, y):
        r, g, b, a = px[x, y]
        return a > ALPHA_T and max(r, g, b) >= DARK

    ymid = int(H * 0.45)
    xmid = int(W * 0.45)

    print(f"size {W}x{H}")
    print("\n[TOP depth] x -> deepest gold y (scan 0..0.45H). Corner=big at ends, cartouche=big at centre, rail=small")
    for x in range(0, W, 40):
        d = 0
        for y in range(ymid, -1, -1):
            if gold(x, y):
                d = y
                break
        print(f"  x={x:4} ({x/W:.2f})  topDepth={d}")

    print("\n[LEFT depth] y -> deepest gold x (scan 0..0.45W). Corner=big at ends, rail=small in middle")
    for y in range(0, H, 40):
        d = 0
        for x in range(xmid, -1, -1):
            if gold(x, y):
                d = x
                break
        print(f"  y={y:4} ({y/H:.2f})  leftDepth={d}")


if __name__ == "__main__":
    main()
