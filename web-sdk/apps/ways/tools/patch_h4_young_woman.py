"""Swap the H4 art (The Little Girl -> blonde young woman) in-place.

Patches the pixels of every frame derived from the h4 card without moving
any frame, so no JSON/atlas coordinates change:

  symbolsStatic:  h4.webp, h4_blur.webp (make_spin_smears.make_smear),
                  h4_burn.webp (make_burn_cards flame composite, same seed)
  mm_symbols:     the 'h4' spine atlas region
  paytable:       static/assets/paytable/h4.png

Run:  python tools/patch_h4_young_woman.py
"""

import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from make_spin_smears import make_smear  # noqa: E402
from make_burn_cards import (  # noqa: E402
    REF_PATH,
    compose_burn,
    extract_flame_layer,
    extract_frame,
    measure_medallion_radius,
)

STATIC_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic"))
SPINE_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "spines", "mm_symbols"))
PAYTABLE_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "paytable"))
NEW_ART = os.path.join(HERE, "symbol_art", "card_h4_young_woman.png")

CELL = 300
# make_burn_cards used seed=i*3+1 with h4 at index 3 in BURN_SOURCES
H4_BURN_SEED = 10


def paste_frame(sheet: Image.Image, frame: dict, image: Image.Image) -> None:
    f = frame["frame"]
    assert image.size == (f["w"], f["h"]), (image.size, f)
    sheet.paste(image, (f["x"], f["y"]))


if __name__ == "__main__":
    card = Image.open(NEW_ART).convert("RGBA").resize((CELL, CELL), Image.LANCZOS)

    # --- symbolsStatic: h4 / h4_blur / h4_burn ---
    with open(os.path.join(STATIC_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        atlas = json.load(f)
    sheet = Image.open(os.path.join(STATIC_DIR, "symbolsStatic.webp")).convert("RGBA")

    paste_frame(sheet, atlas["frames"]["h4.webp"], card)
    print("patched h4.webp")

    paste_frame(sheet, atlas["frames"]["h4_blur.webp"], make_smear(card))
    print("patched h4_blur.webp")

    ref = Image.open(REF_PATH)
    flame, ring_radius = extract_flame_layer(ref)
    medallion = measure_medallion_radius(extract_frame(sheet, atlas["frames"]["l1.webp"]))
    burn = compose_burn(card, flame, ring_radius, medallion, seed=H4_BURN_SEED)
    paste_frame(sheet, atlas["frames"]["h4_burn.webp"], burn)
    print("patched h4_burn.webp")

    sheet.save(os.path.join(STATIC_DIR, "symbolsStatic.png"))
    sheet.save(os.path.join(STATIC_DIR, "symbolsStatic.webp"), lossless=True)
    print(f"wrote {STATIC_DIR}")

    # --- mm_symbols spine atlas: 'h4' region ---
    atlas_txt = open(os.path.join(SPINE_DIR, "mm_symbols.atlas"), encoding="utf-8").read()
    lines = atlas_txt.splitlines()
    bounds = None
    for i, line in enumerate(lines):
        if line.strip() == "h4":
            bounds = [int(v) for v in lines[i + 1].split(":")[1].split(",")]
            break
    if bounds is None:
        raise RuntimeError("h4 region not found in mm_symbols.atlas")
    x, y, w, h = bounds
    spine_sheet = Image.open(os.path.join(SPINE_DIR, "mm_symbols.png")).convert("RGBA")
    spine_sheet.paste(card.resize((w, h), Image.LANCZOS), (x, y))
    spine_sheet.save(os.path.join(SPINE_DIR, "mm_symbols.png"))
    spine_sheet.save(os.path.join(SPINE_DIR, "mm_symbols.webp"), lossless=True)
    print(f"patched spine region h4 at {bounds} -> {SPINE_DIR}")

    # --- paytable crop ---
    card.save(os.path.join(PAYTABLE_DIR, "h4.png"))
    print(f"wrote {PAYTABLE_DIR}/h4.png")

    print("done")
