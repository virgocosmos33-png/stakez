"""Count distinctive glyph colours inside the plus/minus cells of a pill crop.

Usage: python tools/qa_color_count.py <crop.png>
Crop is 420x192 (210x96 @ 2x). Plus cell ~ right third; minus cell ~ left sixth.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
p = OUT / sys.argv[1]


def count(im, box, label):
    crop = im.crop(box)
    red = green = white = black = other = 0
    for (r, g, b) in crop.getdata():
        if r > 150 and g < 100 and b < 100:
            red += 1
        elif g > 150 and r < 120 and b < 120:
            green += 1
        elif r > 205 and g > 205 and b > 205:
            white += 1
        elif r < 60 and g < 60 and b < 60:
            black += 1
        else:
            other += 1
    print(f"[{label}] box={box} red={red} green={green} white={white} black={black} other={other}", flush=True)


def main():
    im = Image.open(p).convert("RGB")
    w, h = im.size
    print(f"size={im.size}", flush=True)
    # minus cell (left ~ x:20..75 of 210 => *2), plus cell (x:150..205 => *2)
    count(im, (int(w * 0.05), 0, int(w * 0.36), h), "MINUS-cell")
    count(im, (int(w * 0.70), 0, w, h), "PLUS-cell")


if __name__ == "__main__":
    main()
