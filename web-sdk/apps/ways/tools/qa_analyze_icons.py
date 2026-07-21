"""Analyze the bonus/buy feature icons for transparency + baked backgrounds.

Reports per file: mode, size, whether it has an alpha channel, the fraction of
fully-transparent and fully-opaque pixels, and the four corner pixels (a strong
signal for a baked opaque background). Run from web-sdk/apps/ways.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

DIR = Path("static/assets/sprites/mirror")
FILES = [
    "buy_ante.webp",
    "buy_feature1.webp",
    "buy_feature2.webp",
    "buy_feature3.webp",
    "buy_seance.webp",
    "buy_otherside.webp",
    "buy_bloodmoon.webp",
]


def analyze(path: Path) -> None:
    im = Image.open(path)
    has_alpha = im.mode in ("RGBA", "LA") or ("transparency" in im.info)
    print(f"\n=== {path.name} ===")
    print(f"  format={im.format} mode={im.mode} size={im.size} has_alpha={has_alpha}")
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    total = w * h
    transparent = 0
    opaque = 0
    # sample every pixel for small images; step for big ones
    step = max(1, (w * h) // 400000)
    counted = 0
    for y in range(0, h, 1 if step == 1 else int(step ** 0.5) or 1):
        for x in range(0, w, 1 if step == 1 else int(step ** 0.5) or 1):
            a = px[x, y][3]
            counted += 1
            if a <= 8:
                transparent += 1
            elif a >= 248:
                opaque += 1
    print(f"  sampled={counted} transparent={transparent / counted:.1%} opaque={opaque / counted:.1%}")
    corners = {
        "TL": px[0, 0],
        "TR": px[w - 1, 0],
        "BL": px[0, h - 1],
        "BR": px[w - 1, h - 1],
        "C": px[w // 2, h // 2],
    }
    print(f"  corners(rgba): {corners}")
    corner_alphas = [px[0, 0][3], px[w - 1, 0][3], px[0, h - 1][3], px[w - 1, h - 1][3]]
    baked_bg = all(a >= 248 for a in corner_alphas)
    print(f"  -> corners_opaque={baked_bg}  (baked background likely: {baked_bg})")


def main() -> None:
    for f in FILES:
        p = DIR / f
        if p.exists():
            analyze(p)
        else:
            print(f"\n=== {f} === MISSING at {p}")


if __name__ == "__main__":
    main()
