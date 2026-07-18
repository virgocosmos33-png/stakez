"""Derive the violet 'amethyst' bitmap font from the blood 'gold' font.

The gold atlas (Ghastly Panic, blood gradient + dark rim) is hue-rotated from
arterial red into amethyst violet (~+270 deg) while alpha, gradient, rim and
highlight structure survive untouched. Used for glowing win amounts.

Re-run after any make_blood_font.py rebuild:  python tools/make_amethyst_font.py
"""

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
GOLD_DIR = os.path.join(APP, "static", "assets", "fonts", "goldFont")
AMETHYST_DIR = os.path.join(APP, "static", "assets", "fonts", "amethystFont")

HUE_SHIFT = 191  # (270/360)*255 -> red becomes blue-violet


def main() -> None:
    os.makedirs(AMETHYST_DIR, exist_ok=True)

    atlas = Image.open(os.path.join(GOLD_DIR, "mm_gold.png")).convert("RGBA")
    alpha = atlas.getchannel("A")
    h, s, v = atlas.convert("RGB").convert("HSV").split()
    h = h.point(lambda value: (value + HUE_SHIFT) % 256)
    # lift shadows hard: the blood gradient runs to near-black, which reads as
    # a dark smudge on the outro panel; the amount must glow luminous lavender
    v = v.point(lambda value: min(110 + int(value * 0.62), 255))
    s = s.point(lambda value: int(value * 0.82))
    shifted = Image.merge("HSV", (h, s, v)).convert("RGB")
    shifted.putalpha(alpha)

    shifted.save(os.path.join(AMETHYST_DIR, "mm_amethyst.png"))
    shifted.save(os.path.join(AMETHYST_DIR, "mm_amethyst.webp"), lossless=True)

    with open(os.path.join(GOLD_DIR, "mm_gold.xml"), encoding="utf-8") as f:
        xml = f.read()
    xml = xml.replace('face="gold"', 'face="amethyst"').replace("mm_gold.webp", "mm_amethyst.webp")
    with open(os.path.join(AMETHYST_DIR, "mm_amethyst.xml"), "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"amethyst font written -> {AMETHYST_DIR} ({atlas.size[0]}x{atlas.size[1]})")


if __name__ == "__main__":
    main()
