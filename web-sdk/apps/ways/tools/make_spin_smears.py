"""Bake NLC-style spin SMEAR frames into the symbolsStatic atlas.

For every reel symbol (h1-h5, l1-l5, w, s, hm_intact) this renders a
`<name>_blur` frame: the card art vertically stretched and directionally
blurred (motion smear) with feathered ends, slightly lifted brightness and
softened contrast - the classic smear-frame trick that sells reel speed.

The original frames are preserved byte-for-byte; smear frames are appended
below them in a rebuilt sheet. Frame names gain a `_blur` suffix before the
extension (h1.webp -> h1_blur.webp) so constants.ts can route the `spin`
symbol state at them.

Run:  python tools/make_spin_smears.py
"""

from __future__ import annotations

import json
import os
import shutil

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(
    os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic")
)
BACKUP_DIR = os.path.join(ATLAS_DIR, "backup_pre_smear")

CELL = 300
PADDING = 2
COLUMNS = 4

# how far (px) the smear reaches above/below the stretched card
SMEAR = 72
# vertical stretch of the card core before blurring
STRETCH = 1.12
SMEAR_H = int(CELL * STRETCH) + 2 * SMEAR  # 480 -> sizeRatios height 1.6

SMEAR_SOURCES = [
    "h1.webp", "h2.webp", "h3.webp", "h4.webp", "h5.webp",
    "l1.webp", "l2.webp", "l3.webp", "l4.webp", "l5.webp",
    "w.png", "s.png", "hm_intact.png",
]


def blur_name(frame_name: str) -> str:
    stem, ext = frame_name.rsplit(".", 1)
    return f"{stem}_blur.{ext}"


def extract_frame(atlas_img: Image.Image, frame: dict) -> Image.Image:
    f = frame["frame"]
    region = atlas_img.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    src = frame.get("spriteSourceSize", {"x": 0, "y": 0})
    cell.paste(region, (src.get("x", 0), src.get("y", 0)))
    return cell


def make_smear(card: Image.Image) -> Image.Image:
    """Vertical motion smear: premultiplied directional blur of the
    stretched card + a faint sharp ghost so the symbol stays readable."""
    stretched = card.resize((CELL, int(CELL * STRETCH)), Image.LANCZOS)

    canvas = np.zeros((SMEAR_H, CELL, 4), dtype=np.float32)
    src = np.asarray(stretched, dtype=np.float32)
    # premultiply so transparent pixels never bleed dark halos
    src_pm = src.copy()
    src_pm[..., :3] *= src[..., 3:4] / 255.0

    # triangular-weighted accumulation of vertically shifted copies
    steps = 25
    total = 0.0
    for i in range(steps):
        f = i / (steps - 1)  # 0..1
        offset = int(round((f - 0.5) * 2 * SMEAR))
        weight = 1.0 - abs(f - 0.5) * 1.5  # heavier center
        y0 = SMEAR + offset
        canvas[y0 : y0 + src_pm.shape[0], :, :] += src_pm * weight
        total += weight
    canvas /= total

    # soften contrast toward mid-grey (motion washes out detail)
    alpha = canvas[..., 3:4] / 255.0
    canvas[..., :3] = canvas[..., :3] * 0.88 + (128.0 * alpha) * 0.12
    # slight brightness lift so the streak reads on the dark board
    canvas[..., :3] *= 1.06

    # faint sharp ghost at the center keeps the symbol identifiable
    ghost_y = SMEAR + (canvas.shape[0] - 2 * SMEAR - src_pm.shape[0]) // 2
    canvas[ghost_y : ghost_y + src_pm.shape[0], :, :] += src_pm * 0.22
    canvas = np.clip(canvas, 0, 255 * 1.22)

    # un-premultiply
    out_alpha = np.clip(canvas[..., 3], 0, 255)
    safe = np.maximum(out_alpha[..., None], 1e-5)
    rgb = np.clip(canvas[..., :3] / (safe / 255.0), 0, 255)
    out = np.concatenate([rgb, out_alpha[..., None]], axis=-1).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


if __name__ == "__main__":
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for name in ("symbolsStatic.json", "symbolsStatic.webp", "symbolsStatic.png"):
        src = os.path.join(ATLAS_DIR, name)
        dst = os.path.join(BACKUP_DIR, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"backed up {name}")

    with open(os.path.join(ATLAS_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        current_json = json.load(f)
    current_img = Image.open(os.path.join(ATLAS_DIR, "symbolsStatic.webp")).convert("RGBA")

    # carry every existing ORIGINAL frame (drop stale _blur frames on re-runs)
    cells: dict[str, Image.Image] = {
        name: extract_frame(current_img, frame)
        for name, frame in current_json["frames"].items()
        if "_blur." not in name
    }

    smears: dict[str, Image.Image] = {}
    for name in SMEAR_SOURCES:
        if name not in cells:
            print(f"  (skip {name}: not in atlas)")
            continue
        smears[blur_name(name)] = make_smear(cells[name])
        print(f"smeared {name} -> {blur_name(name)}  ({CELL}x{SMEAR_H})")

    # sheet: original 300x300 grid on top, smear grid below
    names = sorted(cells.keys())
    rows = (len(names) + COLUMNS - 1) // COLUMNS
    sheet_w = COLUMNS * (CELL + PADDING) + PADDING
    cards_h = rows * (CELL + PADDING) + PADDING
    smear_names = sorted(smears.keys())
    smear_rows = (len(smear_names) + COLUMNS - 1) // COLUMNS
    sheet_h = cards_h + smear_rows * (SMEAR_H + PADDING) + PADDING
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

    frames: dict[str, dict] = {}

    def frame_entry(x: int, y: int, w: int, h: int) -> dict:
        return {
            "frame": {"x": x, "y": y, "w": w, "h": h},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": w, "h": h},
            "sourceSize": {"w": w, "h": h},
            "pivot": {"x": 0.5, "y": 0.5},
        }

    for i, name in enumerate(names):
        col, row = i % COLUMNS, i // COLUMNS
        x = PADDING + col * (CELL + PADDING)
        y = PADDING + row * (CELL + PADDING)
        sheet.paste(cells[name], (x, y))
        frames[name] = frame_entry(x, y, CELL, CELL)

    for i, name in enumerate(smear_names):
        col, row = i % COLUMNS, i // COLUMNS
        x = PADDING + col * (CELL + PADDING)
        y = cards_h + PADDING + row * (SMEAR_H + PADDING)
        sheet.paste(smears[name], (x, y))
        frames[name] = frame_entry(x, y, CELL, SMEAR_H)

    atlas = {
        "frames": frames,
        "meta": {
            "app": "make_spin_smears.py",
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
    print(f"smear frame size {CELL}x{SMEAR_H} (sizeRatios height = {SMEAR_H / CELL:.3f})")
