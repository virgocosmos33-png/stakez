"""Make PNG previews of the feature icons so they can be inspected (WebP can't be
decoded by the image reader here). Saves downscaled RGB PNGs.
Run from web-sdk/apps/ways.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

DIR = Path("static/assets/sprites/mirror")
OUT = Path("../../qa-shots/hud/_icons")
OUT.mkdir(parents=True, exist_ok=True)
FILES = [
    "buy_ante.webp",
    "buy_feature1.webp",
    "buy_feature2.webp",
    "buy_feature3.webp",
    "buy_seance.webp",
    "buy_otherside.webp",
    "buy_bloodmoon.webp",
]


def main() -> None:
    for f in FILES:
        p = DIR / f
        if not p.exists():
            print(f"MISSING {f}")
            continue
        im = Image.open(p).convert("RGB")
        im.thumbnail((520, 520))
        out = OUT / (Path(f).stem + ".png")
        im.save(out)
        print(f"saved {out}")


if __name__ == "__main__":
    main()
