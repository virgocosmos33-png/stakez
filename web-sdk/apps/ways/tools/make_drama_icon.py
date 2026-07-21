#!/usr/bin/env python3
"""Recolor the Flaticon "drama" theatrical-masks icon into a clean WHITE,
HUD-ready monochrome asset (white ink on transparent background).

The source art (Flaticon free icon id 8363672) is pure black ink on a
transparent background:
  - opaque black pixels  -> the mask ink (silhouette + outlines)
  - transparent pixels   -> the background AND intentional negative space
                            (the comedy mask's open face, and the tragedy
                            mask's eye/mouth cut-outs)

Because the HUD is pure white-on-black, we tint every ink pixel to white
(0xFFFFFF) while PRESERVING the original alpha channel. That keeps the
anti-aliased edges crisp and keeps the negative-space holes transparent so
the black HUD shows through them. We then trim the transparent padding and
re-pad with a small, even margin on a centered square canvas.

Usage:
    python make_drama_icon.py            # uses default paths (see below)
    python make_drama_icon.py --margin 0.08 --no-square

Reproducible: paths are resolved relative to this file's location inside the
`web-sdk/apps/ways` app.

Attribution: icon by Freepik / Flaticon (https://www.flaticon.com/free-icon/drama_8363672).
Flaticon free license requires attribution.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

# This file lives at: web-sdk/apps/ways/tools/make_drama_icon.py
# HUD sprites live at: web-sdk/apps/ways/static/assets/sprites/hud/
APP_ROOT = Path(__file__).resolve().parents[1]
HUD_DIR = APP_ROOT / "static" / "assets" / "sprites" / "hud"
DEFAULT_SRC = HUD_DIR / "drama_masks_src.png"
DEFAULT_OUT = HUD_DIR / "drama_masks.png"

WHITE = (255, 255, 255)


def recolor_white(img: Image.Image) -> Image.Image:
    """Return an RGBA copy with every channel forced to white, alpha preserved.

    Setting RGB to white for ALL pixels (even fully transparent ones) avoids
    dark colour fringing when the sprite is later scaled/filtered, while the
    preserved alpha keeps the shape and negative space intact.
    """
    img = img.convert("RGBA")
    alpha = img.getchannel("A")
    white = Image.new("RGBA", img.size, WHITE + (0,))
    white.putalpha(alpha)
    return white


def trim_and_pad(img: Image.Image, margin_frac: float, square: bool) -> Image.Image:
    """Crop to the alpha bounding box, then re-pad with an even margin."""
    bbox = img.getchannel("A").getbbox()
    if bbox is None:
        return img
    content = img.crop(bbox)
    cw, ch = content.size

    margin = round(max(cw, ch) * margin_frac)
    if square:
        side = max(cw, ch) + 2 * margin
        canvas_w = canvas_h = side
    else:
        canvas_w = cw + 2 * margin
        canvas_h = ch + 2 * margin

    canvas = Image.new("RGBA", (canvas_w, canvas_h), WHITE + (0,))
    offset = ((canvas_w - cw) // 2, (canvas_h - ch) // 2)
    canvas.paste(content, offset)
    return canvas


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC, help="source PNG")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output PNG")
    ap.add_argument("--margin", type=float, default=0.08,
                    help="margin as a fraction of the content's longest side")
    ap.add_argument("--no-square", dest="square", action="store_false",
                    help="do not force a square canvas")
    args = ap.parse_args()

    src = Image.open(args.src)
    white = recolor_white(src)
    result = trim_and_pad(white, args.margin, args.square)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.out)

    print(f"source : {args.src}  {src.size}")
    print(f"output : {args.out}  {result.size}")


if __name__ == "__main__":
    main()
