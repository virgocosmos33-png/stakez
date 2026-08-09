"""Reshape the freshly-repacked SQUARE symbol cells into the portrait card
footprint, in place, in static/assets.

The repo-root tools/make_symbols_portrait.py owns the actual card shaping
(cover-fit for faces, contain for objects, thin bezel, rounded corners,
transparent side margins). But it is hardcoded to the legacy white-room/assets/
Vite folder (now empty) and reads square originals from a STALE snapshot cache
(assets-raw/symbols_square holds the OLD art). This driver reuses its make_card
logic but sources the square pixels straight from the just-repacked sheets in
static/assets and writes back there, so it always reshapes the CURRENT art.

Spin `_blur` and `_burn` frames are left untouched (the shipped game keeps
full-width smears), matching the committed atlas.

Run AFTER repack_madam_symbols.py + gen_symbol_spines.py:
    python tools/reshape_symbols_portrait_inplace.py
"""

from __future__ import annotations

import json
import os
import sys
import time

from PIL import Image


def _atomic_save(img: Image.Image, dest: str, **kwargs) -> None:
    """Write to a temp file then swap it in — the dev server keeps these files
    open on Windows, and a direct open-for-write dies with EINVAL."""
    root, ext = os.path.splitext(dest)
    tmp = f"{root}.__tmp__{ext}"
    img.save(tmp, **kwargs)
    for attempt in range(10):
        try:
            os.replace(tmp, dest)
            return
        except OSError:
            if attempt == 9:
                raise
            time.sleep(0.5)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))
import make_symbols_portrait as msp  # noqa: E402

STATIC_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic"))
SPINE_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "spines", "mm_symbols"))

# Premiums are cover-fit (full-bleed photo). The reframed Grin (h3) stands
# farther back, so he gets an extra centre-crop to match the doctor's scale.
PREMIUM_ZOOM = {"h1": 1.2, "h2": 1.2, "h3": 1.44, "h4": 1.2, "h5": 1.2}

# The royals are magenta-keyed TRANSPARENT 3D prop renders (RGBA masters, see
# key_magenta_royals.py). They are CONTAIN-fit (whole prop visible) at this
# pad, a touch back from the premiums, on a fully TRANSPARENT card interior —
# only the thin bezel frames them, the board shows through behind the prop.
ROYAL_PAD = 0.82


def _is_card(stem: str) -> bool:
    # only non-blur / non-burn base cards get reshaped
    return stem in msp.CARDS


def _shape(src, stem):
    """Premiums: cover-fit photo. Royals: contain-fit the transparent prop."""
    if stem in msp.PHOTO_CARDS:
        z = PREMIUM_ZOOM.get(stem, 1.0)
        if z > 1.0:
            w, h = src.size
            cw, ch = w / z, h / z
            src = src.crop(
                (round((w - cw) / 2), round((h - ch) / 2), round((w + cw) / 2), round((h + ch) / 2))
            ).resize((w, h), Image.LANCZOS)
        return msp.make_card(src, cover=True)
    # royal object card: transparent interior — make_card fills the card with
    # backdrop(src) (the corner colour, black for these masters), so swap in a
    # fully transparent fill for the duration of the call.
    orig_backdrop = msp.backdrop
    msp.backdrop = lambda img: (0, 0, 0, 0)
    try:
        msp.CONTAIN_PAD = ROYAL_PAD
        return msp.make_card(src, cover=False)
    finally:
        msp.backdrop = orig_backdrop


def reshape_static() -> int:
    with open(os.path.join(STATIC_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        atlas = json.load(f)
    sheet = Image.open(os.path.join(STATIC_DIR, "symbolsStatic.png")).convert("RGBA")
    n = 0
    for frame_name, meta in atlas["frames"].items():
        stem = frame_name.split(".")[0]
        if not _is_card(stem):
            continue
        r = meta["frame"]
        box = (r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"])
        card = _shape(sheet.crop(box), stem)
        sheet.paste(card, box)
        n += 1
    _atomic_save(sheet, os.path.join(STATIC_DIR, "symbolsStatic.png"))
    _atomic_save(sheet, os.path.join(STATIC_DIR, "symbolsStatic.webp"), lossless=True)
    print(f"static: reshaped {n} cards")
    return n


def reshape_spine() -> int:
    atlas_path = os.path.join(SPINE_DIR, "mm_symbols.atlas")
    lines = open(atlas_path, encoding="utf-8").read().splitlines()
    sheet = Image.open(os.path.join(SPINE_DIR, "mm_symbols.png")).convert("RGBA")
    n = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("bounds:"):
            name = lines[i - 1].strip()
            if not _is_card(name):
                continue
            x, y, w, h = (int(v) for v in line.split(":")[1].split(","))
            box = (x, y, x + w, y + h)
            card = _shape(sheet.crop(box), name)
            sheet.paste(card, box)
            n += 1
    _atomic_save(sheet, os.path.join(SPINE_DIR, "mm_symbols.png"))
    _atomic_save(sheet, os.path.join(SPINE_DIR, "mm_symbols.webp"), lossless=True)
    print(f"spine: reshaped {n} cards")
    return n


if __name__ == "__main__":
    reshape_static()
    reshape_spine()
    print("done")
