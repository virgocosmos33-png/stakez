"""Append the Madam's Eye symbol (me.png + me_blur.png) to the symbolsStatic atlas.

Existing frames keep their exact pixel positions - the sheet just grows at the
bottom by one row holding the new static card and its baked spin-smear frame.
The smear is generated the same way as the existing *_blur frames read: the
card is edge-extended to 300x480 and vertically motion-blurred.

Run:  python tools/repack_add_eye.py
"""

import json
import os
import shutil

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic"))
BACKUP_DIR = os.path.join(ATLAS_DIR, "backup_pre_eye")
SRC_CARD = os.path.join(HERE, "symbol_art", "card_me_madams_eye.png")

CELL = 300
BLUR_H = 480
PADDING = 2


def make_blur(card: Image.Image) -> Image.Image:
    """Vertical spin-smear: edge-extend the card to 300x480, then box-blur each
    column over a ~56px vertical window (matches the look of the baked frames)."""
    rgba = np.asarray(card.convert("RGBA"), dtype=np.float32)
    pad = (BLUR_H - CELL) // 2
    extended = np.pad(rgba, ((pad, pad), (0, 0), (0, 0)), mode="edge")

    kernel = 56
    # cumulative-sum box filter along the vertical axis
    padded = np.pad(extended, ((kernel // 2, kernel // 2), (0, 0), (0, 0)), mode="edge")
    csum = np.cumsum(padded, axis=0)
    blurred = (csum[kernel:] - csum[:-kernel]) / kernel

    return Image.fromarray(np.clip(blurred, 0, 255).astype(np.uint8), "RGBA")


if __name__ == "__main__":
    # 1. backup
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for name in ("symbolsStatic.json", "symbolsStatic.webp", "symbolsStatic.png"):
        src = os.path.join(ATLAS_DIR, name)
        dst = os.path.join(BACKUP_DIR, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"backed up {name}")

    # 2. load current atlas
    with open(os.path.join(ATLAS_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        atlas = json.load(f)
    sheet = Image.open(os.path.join(ATLAS_DIR, "symbolsStatic.webp")).convert("RGBA")

    # 3. build the new cells
    card = Image.open(SRC_CARD).convert("RGBA").resize((CELL, CELL), Image.LANCZOS)
    blur = make_blur(card)

    if "me.png" in atlas["frames"]:
        # already packed: replace the pixels in place, geometry unchanged
        rect_card = atlas["frames"]["me.png"]["frame"]
        rect_blur = atlas["frames"]["me_blur.png"]["frame"]
        sheet.paste(card, (rect_card["x"], rect_card["y"]))
        sheet.paste(blur, (rect_blur["x"], rect_blur["y"]))
        sheet.save(os.path.join(ATLAS_DIR, "symbolsStatic.png"))
        sheet.save(os.path.join(ATLAS_DIR, "symbolsStatic.webp"), lossless=True)
        print(f"replaced me.png + me_blur.png in place; sheet {sheet.width}x{sheet.height}")
        raise SystemExit(0)

    # 4. grow the sheet by one row below the last occupied pixel
    bottom = max(f["frame"]["y"] + f["frame"]["h"] for f in atlas["frames"].values())
    new_y = bottom + PADDING
    new_h = new_y + BLUR_H + PADDING
    new_w = max(sheet.width, PADDING + CELL + PADDING + CELL + PADDING)
    grown = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    grown.paste(sheet, (0, 0))
    grown.paste(card, (PADDING, new_y))
    grown.paste(blur, (PADDING + CELL + PADDING, new_y))

    def frame(x, y, w, h):
        return {
            "frame": {"x": x, "y": y, "w": w, "h": h},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": w, "h": h},
            "sourceSize": {"w": w, "h": h},
            "pivot": {"x": 0.5, "y": 0.5},
        }

    atlas["frames"]["me.png"] = frame(PADDING, new_y, CELL, CELL)
    atlas["frames"]["me_blur.png"] = frame(PADDING + CELL + PADDING, new_y, CELL, BLUR_H)
    atlas["meta"]["size"] = {"w": new_w, "h": new_h}

    # 5. write
    grown.save(os.path.join(ATLAS_DIR, "symbolsStatic.png"))
    grown.save(os.path.join(ATLAS_DIR, "symbolsStatic.webp"), lossless=True)
    with open(os.path.join(ATLAS_DIR, "symbolsStatic.json"), "w", encoding="utf-8") as f:
        json.dump(atlas, f, indent=1)

    print(f"appended me.png + me_blur.png; sheet now {new_w}x{new_h}, {len(atlas['frames'])} frames")
