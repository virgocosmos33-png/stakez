"""Probe the frame texture composition: alpha histogram + pixel samples so we
know whether the interior is transparent or opaque, and how the corners are
shaped. Run from web-sdk/apps/ways: python tools/probe_frame.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

APP = Path(__file__).resolve().parent.parent
SRC = APP / "static" / "assets" / "sprites" / "mirror" / "mirror_frame_wide.png"


def main() -> None:
    im = Image.open(SRC).convert("RGBA")
    W, H = im.size
    px = im.load()
    print(f"size {W}x{H}")

    a = im.getchannel("A")
    hist = a.histogram()
    total = W * H
    print(f"alpha==0   : {hist[0]:>9}  ({100*hist[0]/total:.1f}%)")
    print(f"alpha==255 : {hist[255]:>9}  ({100*hist[255]/total:.1f}%)")
    mid = sum(hist[1:255])
    print(f"alpha 1..254: {mid:>9}  ({100*mid/total:.1f}%)")

    pts = {
        "outer TL (5,5)": (5, 5),
        "outer TR (W-5,5)": (W - 5, 5),
        "outer BL (5,H-5)": (5, H - 5),
        "outer BR (W-5,H-5)": (W - 5, H - 5),
        "top edge mid (W/2,5)": (W // 2, 5),
        "left edge mid (5,H/2)": (5, H // 2),
        "center (W/2,H/2)": (W // 2, H // 2),
        "quarter (W/4,H/4)": (W // 4, H // 4),
        "inner near TL (120,120)": (120, 120),
    }
    for label, (x, y) in pts.items():
        print(f"{label:28} = {px[x, y]}")

    # alpha profile across the horizontal centre line (sampled every ~5%)
    print("\n[alpha along horizontal center]")
    y = H // 2
    for f in [i / 20 for i in range(21)]:
        x = min(W - 1, int(f * W))
        print(f"  x={x:4} ({f:.2f}) a={px[x, y][3]:3} rgb={px[x,y][:3]}")

    print("\n[alpha along vertical center]")
    x = W // 2
    for f in [i / 20 for i in range(21)]:
        y = min(H - 1, int(f * H))
        print(f"  y={y:4} ({f:.2f}) a={px[x, y][3]:3} rgb={px[x,y][:3]}")

    # For nine-slice we care where the GOLD (bright) inner edge is. Detect on the
    # centre lines: brightness threshold, find inner edge of the bright rail.
    def bright(x, y):
        r, g, b, al = px[x, y]
        return al > 40 and (r + g + b) / 3 > 70

    y = H // 2
    xL = 0
    while xL < W and not bright(xL, y):
        xL += 1
    xLend = xL
    while xLend < W and bright(xLend, y):
        xLend += 1
    print(f"\n[left gold @midY] starts x={xL} inner edge x={xLend}")
    x = W // 2
    yT = 0
    while yT < H and not bright(x, yT):
        yT += 1
    yTend = yT
    while yTend < H and bright(x, yTend):
        yTend += 1
    print(f"[top gold @midX] starts y={yT} inner edge y={yTend}")


if __name__ == "__main__":
    main()
