"""Repack the symbolsStatic atlas for the new Madam Mirror symbol schema.

Replaces the 10 paying-symbol frames (h1-h5, l1-l5) with the freshly generated
card art in tools/symbol_art/, and carries the untouched special frames
(w, s, hm_intact, hm_cracked, explodedW) straight out of the CURRENT atlas so
the wild / scatter / haunted-mirror art is preserved byte-for-byte in layout.

Frame NAMES are unchanged (h1.webp ... l5.webp), so no frontend code needs to
change - only the pixels behind each frame.

Run:  python tools/repack_madam_symbols.py
"""

import json
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic"))
SRC_DIR = os.path.join(HERE, "symbol_art")
BACKUP_DIR = os.path.join(ATLAS_DIR, "backup_pre_reskin")

CELL = 300
PADDING = 2
COLUMNS = 4

# new source card -> atlas frame name (full-bleed square plates)
NEW_ICONS = {
    "card_h1_lady_mirror.png": "h1.webp",
    "card_h2_wife.png": "h2.webp",
    "card_h3_man.png": "h3.webp",
    "card_h4_young_woman.png": "h4.webp",
    "card_h5_dog.png": "h5.webp",
    "card_l1_ace.png": "l1.webp",
    "card_l2_king.png": "l2.webp",
    "card_l3_queen.png": "l3.webp",
    "card_l4_jack.png": "l4.webp",
    "card_l5_ten.png": "l5.webp",
}

# frames kept from the current atlas unchanged (wild / scatter / mirror / fx)
KEEP_FRAMES = ["w.png", "s.png", "hm_intact.png", "hm_cracked.png", "explodedW.png"]


def extract_frame(atlas_img: Image.Image, frame: dict) -> Image.Image:
    """Pull a frame out of the current atlas onto a CELLxCELL canvas."""
    f = frame["frame"]
    if frame.get("rotated"):
        region = atlas_img.crop((f["x"], f["y"], f["x"] + f["h"], f["y"] + f["w"]))
        region = region.transpose(Image.ROTATE_90)
    else:
        region = atlas_img.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
    src = frame.get("spriteSourceSize", {"x": 0, "y": 0})
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.paste(region, (src.get("x", 0), src.get("y", 0)))
    return cell


if __name__ == "__main__":
    # 1. back up the current atlas once
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for name in ("symbolsStatic.json", "symbolsStatic.webp", "symbolsStatic.png"):
        src = os.path.join(ATLAS_DIR, name)
        dst = os.path.join(BACKUP_DIR, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"backed up {name}")

    # 2. read the current atlas (source of the KEEP frames)
    with open(os.path.join(ATLAS_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        current_json = json.load(f)
    current_img = Image.open(os.path.join(ATLAS_DIR, "symbolsStatic.webp")).convert("RGBA")

    cells: dict[str, Image.Image] = {}

    # 3. new card art -> resized full-bleed cells
    for icon_file, frame_name in NEW_ICONS.items():
        path = os.path.join(SRC_DIR, icon_file)
        im = Image.open(path).convert("RGBA").resize((CELL, CELL), Image.LANCZOS)
        cells[frame_name] = im
        print(f"packed new  {icon_file} -> {frame_name}")

    # 4. carry the untouched frames over from the current atlas
    for frame_name in KEEP_FRAMES:
        if frame_name not in current_json["frames"]:
            print(f"  (skip {frame_name}: not in current atlas)")
            continue
        cells[frame_name] = extract_frame(current_img, current_json["frames"][frame_name])
        print(f"kept        {frame_name}")

    # 5. compose the sheet
    names = sorted(cells.keys())
    rows = (len(names) + COLUMNS - 1) // COLUMNS
    sheet_w = COLUMNS * (CELL + PADDING) + PADDING
    sheet_h = rows * (CELL + PADDING) + PADDING
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

    frames = {}
    for i, name in enumerate(names):
        col, row = i % COLUMNS, i // COLUMNS
        x = PADDING + col * (CELL + PADDING)
        y = PADDING + row * (CELL + PADDING)
        sheet.paste(cells[name], (x, y))
        frames[name] = {
            "frame": {"x": x, "y": y, "w": CELL, "h": CELL},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": CELL, "h": CELL},
            "sourceSize": {"w": CELL, "h": CELL},
            "pivot": {"x": 0.5, "y": 0.5},
        }

    atlas = {
        "frames": frames,
        "meta": {
            "app": "repack_madam_symbols.py",
            "version": "1.0",
            "image": "symbolsStatic.webp",
            "format": "RGBA8888",
            "size": {"w": sheet_w, "h": sheet_h},
            "scale": "1",
        },
    }

    sheet.save(os.path.join(ATLAS_DIR, "symbolsStatic.png"))
    sheet.save(os.path.join(ATLAS_DIR, "symbolsStatic.webp"), lossless=True)
    with open(os.path.join(ATLAS_DIR, "symbolsStatic.json"), "w", encoding="utf-8") as f:
        json.dump(atlas, f, indent=1)

    print(f"\nwrote {sheet_w}x{sheet_h} atlas with {len(frames)} frames -> {ATLAS_DIR}")
