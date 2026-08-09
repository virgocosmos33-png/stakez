"""Demonstrate that a background key CANNOT cleanly separate a floating subject
from these icons: keying black only drops the backdrop and leaves the ornate
frame + baked title, while also punching holes in the dark areas inside the art.
Composites the keyed result over a magenta checkerboard so leftover frame/holes
are obvious. Run from web-sdk/apps/ways.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

DIR = Path("static/assets/sprites/mirror")
OUT = Path("../../qa-shots/hud/_icons")
OUT.mkdir(parents=True, exist_ok=True)
FILES = ["buy_seance.webp", "buy_otherside.webp"]
THRESH = 40  # treat pixels darker than this (max channel) as background


def checker(size, box=24):
    w, h = size
    bg = Image.new("RGBA", size, (40, 40, 48, 255))
    px = bg.load()
    for y in range(h):
        for x in range(w):
            if ((x // box) + (y // box)) % 2 == 0:
                px[x, y] = (150, 30, 120, 255)
    return bg


def main() -> None:
    for f in FILES:
        im = Image.open(DIR / f).convert("RGBA")
        im.thumbnail((520, 520))
        px = im.load()
        w, h = im.size
        for y in range(h):
            for x in range(w):
                r, g, b, _ = px[x, y]
                if max(r, g, b) < THRESH:
                    px[x, y] = (r, g, b, 0)
        base = checker(im.size)
        base.alpha_composite(im)
        out = OUT / (Path(f).stem + "_keyed.png")
        base.convert("RGB").save(out)
        print(f"saved {out}")


if __name__ == "__main__":
    main()
