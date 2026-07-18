"""Derive the absinthe-green 'ghost' bitmap font from the blood 'gold' font.

The gold atlas (Ghastly Panic, blood gradient + dark rim) is channel-swapped
R<->G, which turns arterial red -> spectral green while preserving the
gradient, rim and highlight structure. Writes a self-contained ghostFont
folder (mm_ghost.png/webp/xml, face="ghost").

Re-run after any make_blood_font.py rebuild:  python tools/make_ghost_font.py
"""

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
GOLD_DIR = os.path.join(APP, "static", "assets", "fonts", "goldFont")
GHOST_DIR = os.path.join(APP, "static", "assets", "fonts", "ghostFont")


def main() -> None:
    os.makedirs(GHOST_DIR, exist_ok=True)

    atlas = Image.open(os.path.join(GOLD_DIR, "mm_gold.png")).convert("RGBA")
    r, g, b, a = atlas.split()
    ghost = Image.merge("RGBA", (g, r, b, a))
    ghost.save(os.path.join(GHOST_DIR, "mm_ghost.png"))
    ghost.save(os.path.join(GHOST_DIR, "mm_ghost.webp"), lossless=True)

    with open(os.path.join(GOLD_DIR, "mm_gold.xml"), encoding="utf-8") as f:
        xml = f.read()
    xml = xml.replace('face="gold"', 'face="ghost"').replace("mm_gold.webp", "mm_ghost.webp")
    with open(os.path.join(GHOST_DIR, "mm_ghost.xml"), "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"ghost font written -> {GHOST_DIR} ({atlas.size[0]}x{atlas.size[1]})")


if __name__ == "__main__":
    main()
