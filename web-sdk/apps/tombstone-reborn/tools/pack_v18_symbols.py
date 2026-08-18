"""Pack the v18 hand-painted symbol set into the atlas.

Replaces ALL ten paying faces (h1..h5 premium busts, l1..l5 object emblems)
with the painterly generations. Every other frame (w/s/hm/me/exploded/burn)
carries over from v13 unchanged. `_blur` spin smears are rebuilt from the
new cards. Also patches the mm_symbols spine sheet and the paytable PNGs.

Generated 3:4 art is resized straight onto the 226x292 card (a ~3% vertical
squash, imperceptible) so nothing is cropped and nothing shows paper gaps.

Writes v18 to static/assets and assets-src (never an app-root assets/).

Run:  python tools/pack_v18_symbols.py
"""

from __future__ import annotations

import json
import os
import time

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
GEN = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
    )
)

CELL = 300
CARD_H = 292
CARD_W = round(CARD_H * 0.775)  # 226 — matches SYMBOL_CARD_W/H
CORNER_R = 22
ATLAS_OUT = "symbolsStatic.v18"
SRC_ATLAS = "symbolsStatic.v13"

CARDS = {
    "h1.webp": "tr_v18_h1_gunslinger.png",
    "h2.webp": "tr_v18_h2_duchess.png",
    "h3.webp": "tr_v18_h3_butcher.png",
    "h4.webp": "tr_v18_h4_cardshark.png",
    "h5.webp": "tr_v18_h5_preacher.png",
    "l1.webp": "tr_v18_l1_bullet.png",
    "l2.webp": "tr_v18_l2_whiskey.png",
    "l3.webp": "tr_v18_l3_spur.png",
    "l4.webp": "tr_v18_l4_horseshoe.png",
    "l5.webp": "tr_v18_l5_deadmanshand.png",
}

ATLAS_DIRS = [
    os.path.join(APP, "static", "assets", "sprites", "symbolsStatic"),
    os.path.join(APP, "assets-src", "assets", "sprites", "symbolsStatic"),
    os.path.join(APP, "assets-src", "sprites", "symbolsStatic"),
]
SPINE_DIRS = [
    os.path.join(APP, "static", "assets", "spines", "mm_symbols"),
    os.path.join(APP, "assets-src", "spines", "mm_symbols"),
    os.path.join(APP, "assets-src", "assets", "spines", "mm_symbols"),
]
PAYTABLE_DIRS = [
    os.path.join(APP, "static", "assets", "paytable"),
    os.path.join(APP, "assets-src", "paytable"),
    os.path.join(APP, "assets-src", "assets", "paytable"),
]


def _atomic_save(img: Image.Image, dest: str, **kwargs) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    root, ext = os.path.splitext(dest)
    tmp = f"{root}.__tmp__{ext}"
    img.save(tmp, **kwargs)
    for attempt in range(12):
        try:
            os.replace(tmp, dest)
            return
        except OSError:
            if attempt == 11:
                raise
            time.sleep(0.4)


def _atomic_save_json(obj, dest: str) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".__tmp__"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(obj, handle, indent=1)
    for attempt in range(12):
        try:
            os.replace(tmp, dest)
            return
        except OSError:
            if attempt == 11:
                raise
            time.sleep(0.4)


def _rounded_mask(w: int, h: int, r: int) -> Image.Image:
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255)
    return mask


def shape_card(src: Image.Image) -> Image.Image:
    """Full-bleed fit: stretch straight onto the card (max ~3% distortion)."""
    card = src.convert("RGBA").resize((CARD_W, CARD_H), Image.LANCZOS)
    card.putalpha(
        Image.composite(
            card.getchannel("A"),
            Image.new("L", card.size, 0),
            _rounded_mask(CARD_W, CARD_H, CORNER_R),
        )
    )
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.paste(card, ((CELL - CARD_W) // 2, (CELL - CARD_H) // 2), card)
    return cell


def vertical_smear(card: Image.Image, spread: int = 26, steps: int = 9) -> Image.Image:
    out = Image.new("RGBA", card.size, (0, 0, 0, 0))
    for i in range(-steps, steps + 1):
        dy = round(i / steps * spread)
        layer = card.copy()
        fade = max(0.06, 1.0 - abs(i) / steps)
        layer.putalpha(layer.getchannel("A").point(lambda v, f=fade: int(v * f)))
        shifted = Image.new("RGBA", card.size, (0, 0, 0, 0))
        shifted.paste(layer, (0, dy), layer)
        out = Image.alpha_composite(out, shifted)
    return out.filter(ImageFilter.GaussianBlur(1.2))


def load_cards() -> dict[str, Image.Image]:
    cards = {}
    for frame, name in CARDS.items():
        path = os.path.join(GEN, name)
        src = Image.open(path).convert("RGBA")
        print(f"  {name:32s} {src.size[0]}x{src.size[1]} -> {frame}")
        cards[frame] = shape_card(src)
    return cards


def pack_atlas(src_dir: str, dest_dir: str, cards: dict[str, Image.Image]) -> None:
    src_json = os.path.join(src_dir, f"{SRC_ATLAS}.json")
    src_img = os.path.join(src_dir, f"{SRC_ATLAS}.webp")
    if not os.path.isfile(src_json):
        print(f"  skip atlas (no {SRC_ATLAS}): {src_dir}")
        return
    with open(src_json, encoding="utf-8") as handle:
        atlas = json.load(handle)
    sheet = Image.open(src_img).convert("RGBA")
    cells: dict[str, Image.Image] = {}
    for name, meta in atlas["frames"].items():
        box = meta["frame"]
        cells[name] = sheet.crop((box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]))
    for frame, card in cards.items():
        cells[frame] = card
        blur = frame.replace(".", "_blur.")
        if blur in cells:
            cells[blur] = vertical_smear(card)

    names = sorted(cells)
    cols, pad = 4, 2
    rows = (len(names) + cols - 1) // cols
    col_w = max(im.width for im in cells.values())
    row_h = max(im.height for im in cells.values())
    out = Image.new("RGBA", (cols * (col_w + pad) + pad, rows * (row_h + pad) + pad), (0, 0, 0, 0))
    frames = {}
    for i, name in enumerate(names):
        c, r = i % cols, i // cols
        x = pad + c * (col_w + pad)
        y = pad + r * (row_h + pad)
        out.paste(cells[name], (x, y))
        w, h = cells[name].size
        frames[name] = {
            "frame": {"x": x, "y": y, "w": w, "h": h},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": w, "h": h},
            "sourceSize": {"w": w, "h": h},
            "pivot": {"x": 0.5, "y": 0.5},
        }
    atlas_out = {
        "frames": frames,
        "meta": {
            "app": "pack_v18_symbols.py",
            "version": "1.0",
            "image": f"{ATLAS_OUT}.webp",
            "format": "RGBA8888",
            "size": {"w": out.width, "h": out.height},
            "scale": "1",
        },
    }
    os.makedirs(dest_dir, exist_ok=True)
    _atomic_save(out, os.path.join(dest_dir, f"{ATLAS_OUT}.png"))
    _atomic_save(out, os.path.join(dest_dir, f"{ATLAS_OUT}.webp"), lossless=True)
    _atomic_save_json(atlas_out, os.path.join(dest_dir, f"{ATLAS_OUT}.json"))
    print(f"  atlas {out.width}x{out.height} -> {dest_dir}")


def patch_spine(spine_dir: str, cards: dict[str, Image.Image]) -> None:
    atlas_path = os.path.join(spine_dir, "mm_symbols.atlas")
    png_path = os.path.join(spine_dir, "mm_symbols.png")
    if not os.path.isfile(atlas_path) or not os.path.isfile(png_path):
        print(f"  skip spine: {spine_dir}")
        return
    lines = open(atlas_path, encoding="utf-8").read().splitlines()
    sheet = Image.open(png_path).convert("RGBA")
    n = 0
    for i, line in enumerate(lines):
        if not line.strip().startswith("bounds:"):
            continue
        name = lines[i - 1].strip()
        frame = f"{name}.webp"
        if frame not in cards:
            continue
        x, y, w, h = (int(v) for v in line.split(":")[1].split(","))
        sheet.paste(cards[frame].resize((w, h), Image.LANCZOS), (x, y))
        n += 1
    _atomic_save(sheet, png_path)
    webp = os.path.join(spine_dir, "mm_symbols.webp")
    if os.path.isfile(webp):
        _atomic_save(sheet, webp, lossless=True)
    print(f"  spine patched {n} cards -> {spine_dir}")


def write_paytable(cards: dict[str, Image.Image]) -> None:
    for dest in PAYTABLE_DIRS:
        if not os.path.isdir(dest) and dest != PAYTABLE_DIRS[0]:
            continue
        os.makedirs(dest, exist_ok=True)
        for frame, card in cards.items():
            name = frame.split(".")[0]
            _atomic_save(card, os.path.join(dest, f"{name}.png"))
        print(f"  paytable h1-h5 / l1-l5 -> {dest}")


if __name__ == "__main__":
    print("Shaping v18 painted cards (full-bleed)...")
    cards = load_cards()
    src_atlas = ATLAS_DIRS[0]
    for dest in ATLAS_DIRS:
        pack_atlas(src_atlas, dest, cards)
    for dest in SPINE_DIRS:
        patch_spine(dest, cards)
    write_paytable(cards)
    print("done")
