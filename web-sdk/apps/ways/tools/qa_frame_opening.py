"""Measure the ornate mirror_frame.png geometry so the reel backing can be
sized to the frame's actual transparent opening (not guessed).

Prints, as fractions of the full image:
  - content bbox (opaque gold extent)
  - inner opening bbox (largest central transparent hole)
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ASSET = (
    Path(__file__).resolve().parents[1]
    / "static" / "assets" / "sprites" / "mirror" / "mirror_frame.png"
)


def main() -> None:
    im = Image.open(ASSET).convert("RGBA")
    W, H = im.size
    alpha = im.getchannel("A")
    px = alpha.load()
    THRESH = 40  # >THRESH == opaque gold

    # content bbox (any opaque pixel)
    bbox = alpha.getbbox()
    print(f"image = {W}x{H}  ratio(w/h)={W/H:.3f}")
    print(f"content bbox = {bbox}  -> "
          f"x[{bbox[0]/W:.3f},{bbox[2]/W:.3f}] y[{bbox[1]/H:.3f},{bbox[3]/H:.3f}]")

    # inner opening: scan each row/col through the CENTER and find the
    # transparent span bounded by gold on both sides.
    cx, cy = W // 2, H // 2

    # horizontal opening at mid height
    left = cx
    while left > 0 and px[left, cy] <= THRESH:
        left -= 1
    right = cx
    while right < W - 1 and px[right, cy] <= THRESH:
        right += 1

    # vertical opening at mid width
    top = cy
    while top > 0 and px[cx, top] <= THRESH:
        top -= 1
    bot = cy
    while bot < H - 1 and px[cx, bot] <= THRESH:
        bot += 1

    print(f"opening @center  x[{left}..{right}] ({(right-left)/W:.3f} of W)  "
          f"y[{top}..{bot}] ({(bot-top)/H:.3f} of H)")
    print(f"opening frac  wL={left/W:.3f} wR={right/W:.3f}  hT={top/H:.3f} hB={bot/H:.3f}")

    # widest opening across all rows / tallest across all cols (approx inner rect)
    min_l, max_r, min_t, max_b = W, 0, H, 0
    for y in range(H):
        row_l = cx
        while row_l > 0 and px[row_l, y] <= THRESH:
            row_l -= 1
        row_r = cx
        while row_r < W - 1 and px[row_r, y] <= THRESH:
            row_r += 1
        if row_r - row_l > 4:
            min_l = min(min_l, row_l)
            max_r = max(max_r, row_r)
    for x in range(W):
        col_t = cy
        while col_t > 0 and px[x, col_t] <= THRESH:
            col_t -= 1
        col_b = cy
        while col_b < H - 1 and px[x, col_b] <= THRESH:
            col_b += 1
        if col_b - col_t > 4:
            min_t = min(min_t, col_t)
            max_b = max(max_b, col_b)
    print(f"widest opening  x[{min_l}..{max_r}] ({(max_r-min_l)/W:.3f} of W)  "
          f"y[{min_t}..{max_b}] ({(max_b-min_t)/H:.3f} of H)")


if __name__ == "__main__":
    main()
