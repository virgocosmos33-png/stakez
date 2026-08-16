"""Wire the freshly generated Tombstone Reborn card art into the game.

The board symbols are SPRITE-ONLY (see src/game/constants.ts SYMBOL_INFO_MAP:
every state routes to the static card, spin -> the `_blur` frame). So all we
need to touch is:

  1. symbolsStatic atlas  — h1..h5 / l1..l5 static cards + their `_blur` spin
     frames (every OTHER frame in the atlas is carried over unchanged).
  2. mirror/wr_wild.png    — the Wild card.
  3. mirror/wr_scatter_1..5.png + wr_scatter_blur.png — the five Scatter faces.

Each generated square card (with its ornate iron frame + transparent corners)
is COVER-FIT into the same portrait card footprint the old cards used (~226x292
inside a 300x300 cell), so it seats in the board socket exactly like before.

Originals are backed up (*.bak_new.*) before anything is overwritten.

Run:  python tools/wire_tombstone_symbols.py
"""

from __future__ import annotations

import json
import os
import shutil
import time

from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
ATLAS_DIR = os.path.join(APP, "assets", "sprites", "symbolsStatic")
MIRROR_DIR = os.path.join(APP, "assets", "sprites", "mirror")

# generated art lives in the cursor project assets folder
GEN_DIR = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
    )
)

CELL = 300
# portrait card footprint inside the square cell (matches SYMBOL_CARD_W/H:
# H = 300*292/300, W = H*0.775). Cover-fit fills this, cropping only the outer
# scrollwork on the left/right of the square frame.
CARD_H = 292
CARD_W = round(CARD_H * 0.775)  # ~226
CORNER_R = 22

# versioned atlas out-name so a fresh URL defeats any texture cache.
# v5 = LIGHT-graded premiums (Tombstone R.I.P. lightly-tinted portraits) mixed
# with the full-monochrome lows/specials.
ATLAS_OUT = "symbolsStatic.v13"

# MONOCHROME grade: the deck reads as desaturated near-grayscale (Tombstone
# R.I.P. reference) — full grayscale + gentle autocontrast, alpha untouched.
MONO = True

# RAW cards get NO code colour manipulation at all (grade 'none'): the v6 premium
# posters are generated already scary + almost-monochrome + with a WHISPER of the
# rank bg tint baked into the paper (H1 purple .. H5 yellow). We use them exactly
# as generated so no double grading / no code tint fights the art.
RAW_CARDS = {"h1.webp", "h2.webp", "h3.webp", "h4.webp", "h5.webp"}

# generated file -> atlas frame name (static). v6 premiums = scary R.I.P.-style
# portraits, grey poster paper with a faint baked rank tint, no text; lows are
# scrawled charcoal letters. Both cover-fit.
CARD_MAP = {
    # premiums = scary portraits, faint baked bg tint (H1 purple .. H5 yellow), no text.
    # v8 = FULL-BLEED busts (figure runs to all edges, no paper margin/border) so
    # they fill the slot with no white gap; Butcher stays on the v6 reference art.
    "tr_v8_premium_gunslinger.png": "h1.webp",
    "tr_v8_premium_duchess.png": "h2.webp",
    "tr_v6_premium_butcher.png": "h3.webp",
    "tr_v8_premium_cardshark.png": "h4.webp",
    "tr_v8_premium_preacher.png": "h5.webp",
    "tr_v3_royal_A.png": "l1.webp",
    "tr_v3_royal_K.png": "l2.webp",
    "tr_v3_royal_Q.png": "l3.webp",
    "tr_v3_royal_J.png": "l4.webp",
    "tr_v3_royal_10.png": "l5.webp",
}

# wild + scatter art (optional — swapped only if present).
# v9 wild = smoking revolver over pale poster paper with GOLD "WILD" — already
# graded in the art, so it is wired RAW (grade 'none'; mono would kill the gold).
# v10 wild = smoking revolver in a gloved hand over DARK charcoal poster with
# gold WILD — the v9 pale-paper one read as a white splatter blob on the board.
WILD_SRC = "tr_v10_symbol_wild.png"
SCATTER_SRC = "tr_v3_symbol_scatter.png"


def _atomic_save(img: Image.Image, dest: str, **kwargs) -> None:
    """Temp-write then swap — the dev server holds these open on Windows."""
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


def _rounded_mask(w: int, h: int, r: int) -> Image.Image:
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255)
    return m


def to_mono(img: Image.Image) -> Image.Image:
    """Grayscale grade, alpha preserved. Gentle autocontrast so the greys keep
    their punch after losing the colour separation."""
    gray = ImageOps.autocontrast(img.convert("RGB").convert("L"), cutoff=1)
    out = Image.merge("RGB", (gray, gray, gray)).convert("RGBA")
    out.putalpha(img.getchannel("A"))
    return out


def to_tint(img: Image.Image, rgb: tuple[float, float, float]) -> Image.Image:
    """Multiply the RGB by a pale colour so bright (paper) pixels take the hue
    and dark (ink) pixels barely change. Alpha untouched."""
    r, g, b, a = img.convert("RGBA").split()
    r = r.point(lambda v: int(v * rgb[0]))
    g = g.point(lambda v: int(v * rgb[1]))
    b = b.point(lambda v: int(v * rgb[2]))
    return Image.merge("RGBA", (r, g, b, a))


def to_light(img: Image.Image, retain: float = 0.6) -> Image.Image:
    """Almost-monochrome: blend the grayscale toward the original so only a
    faint colour wash survives (retain = fraction of original colour kept)."""
    rgb = img.convert("RGB")
    gray = rgb.convert("L").convert("RGB")
    out = Image.blend(gray, rgb, retain).convert("RGBA")
    out.putalpha(img.getchannel("A"))
    return out


def shape_card(src: Image.Image, grade: str = "mono") -> Image.Image:
    """Cover-fit a square generated card into the portrait footprint, centered
    on a transparent CELLxCELL cell, with rounded corners. `grade` is one of
    'mono' (full grayscale), 'light' (faint tint) or 'none'."""
    src = src.convert("RGBA")
    if grade == "light":
        src = to_light(src)
    elif grade == "mono" and MONO:
        src = to_mono(src)
    scale = max(CARD_W / src.width, CARD_H / src.height)
    resized = src.resize(
        (max(1, round(src.width * scale)), max(1, round(src.height * scale))),
        Image.LANCZOS,
    )
    left = (resized.width - CARD_W) // 2
    top = (resized.height - CARD_H) // 2
    card = resized.crop((left, top, left + CARD_W, top + CARD_H))

    # round the (now hard-cut) corners so the crop edge reads clean in-socket
    mask = _rounded_mask(CARD_W, CARD_H, CORNER_R)
    a = card.getchannel("A")
    a = Image.composite(a, Image.new("L", card.size, 0), mask)
    card.putalpha(a)

    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.paste(card, ((CELL - CARD_W) // 2, (CELL - CARD_H) // 2), card)
    return cell


def vertical_smear(card: Image.Image, spread: int = 26, steps: int = 9) -> Image.Image:
    """Cheap vertical motion smear for the spin `_blur` frame: stack y-shifted,
    alpha-faded copies of the card, then a light gaussian."""
    out = Image.new("RGBA", card.size, (0, 0, 0, 0))
    for i in range(-steps, steps + 1):
        dy = round(i / steps * spread)
        layer = card.copy()
        # fade with distance from center
        fade = max(0.06, 1.0 - abs(i) / steps)
        alpha = layer.getchannel("A").point(lambda v, f=fade: int(v * f))
        layer.putalpha(alpha)
        shifted = Image.new("RGBA", card.size, (0, 0, 0, 0))
        shifted.paste(layer, (0, dy), layer)
        out = Image.alpha_composite(out, shifted)
    return out.filter(ImageFilter.GaussianBlur(1.2))


def rebuild_atlas() -> None:
    # read the CURRENT atlas for carry-over frames (explodedW / burn / etc.)
    src_json = os.path.join(ATLAS_DIR, "symbolsStatic.json")
    src_png = os.path.join(ATLAS_DIR, "symbolsStatic.png")
    # write a fresh VERSIONED atlas so no cache can serve a stale texture
    json_path = os.path.join(ATLAS_DIR, f"{ATLAS_OUT}.json")
    png_path = os.path.join(ATLAS_DIR, f"{ATLAS_OUT}.png")
    webp_path = os.path.join(ATLAS_DIR, f"{ATLAS_OUT}.webp")

    with open(src_json, encoding="utf-8") as f:
        atlas = json.load(f)
    sheet = Image.open(src_png).convert("RGBA")

    # start from EVERY existing frame (carried over unchanged), then overwrite
    # the ones we have new art for + regenerate their blur frames.
    cells: dict[str, Image.Image] = {}
    for name, meta in atlas["frames"].items():
        r = meta["frame"]
        cells[name] = sheet.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))

    shaped: dict[str, Image.Image] = {}
    for gen_file, frame in CARD_MAP.items():
        src = Image.open(os.path.join(GEN_DIR, gen_file))
        grade = "none" if frame in RAW_CARDS else "mono"
        card = shape_card(src, grade)
        shaped[frame] = card
        cells[frame] = card
        blur_name = frame.replace(".", "_blur.")
        if blur_name in cells:
            cells[blur_name] = vertical_smear(card)
        print(f"  {gen_file:32s} -> {frame} (+{blur_name})")

    # repack: 4 columns, CELL grid, 2px padding (same as repack_symbols.py)
    names = sorted(cells.keys())
    cols = 4
    pad = 2
    rows = (len(names) + cols - 1) // cols
    # all cells are CELL square except carried-over frames that may differ; keep
    # each frame at its own source size to be safe.
    widths = {n: cells[n].width for n in names}
    heights = {n: cells[n].height for n in names}
    col_w = max(widths.values())
    row_h = max(heights.values())
    sheet_w = cols * (col_w + pad) + pad
    sheet_h = rows * (row_h + pad) + pad
    out = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

    frames = {}
    for i, n in enumerate(names):
        c, rw = i % cols, i // cols
        x = pad + c * (col_w + pad)
        y = pad + rw * (row_h + pad)
        out.paste(cells[n], (x, y))
        w, h = widths[n], heights[n]
        frames[n] = {
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
            "app": "wire_tombstone_symbols.py",
            "version": "1.0",
            "image": f"{ATLAS_OUT}.webp",
            "format": "RGBA8888",
            "size": {"w": sheet_w, "h": sheet_h},
            "scale": "1",
        },
    }

    _atomic_save(out, png_path)
    _atomic_save(out, webp_path, lossless=True)
    _atomic_save_json(atlas_out, json_path)
    print(f"atlas: {sheet_w}x{sheet_h}, {len(frames)} frames -> {ATLAS_DIR}")


def _atomic_save_json(obj, dest: str) -> None:
    tmp = dest + ".__tmp__"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)
    for attempt in range(12):
        try:
            os.replace(tmp, dest)
            return
        except OSError:
            if attempt == 11:
                raise
            time.sleep(0.4)


def swap_single(gen_file: str, dest_name: str, grade: str = "mono") -> None:
    dest = os.path.join(MIRROR_DIR, dest_name)
    bak = dest + ".bak_new"
    if os.path.exists(dest) and not os.path.exists(bak):
        shutil.copy2(dest, bak)
    card = shape_card(Image.open(os.path.join(GEN_DIR, gen_file)), grade)
    _atomic_save(card, dest)
    print(f"  {gen_file:32s} -> mirror/{dest_name}")


def wire_wild_and_scatter() -> None:
    wild_path = os.path.join(GEN_DIR, WILD_SRC)
    if os.path.exists(wild_path):
        swap_single(WILD_SRC, "wr_wild.png", grade="none")
    else:
        print(f"  (skip wild: {WILD_SRC} not generated yet)")

    scatter_path = os.path.join(GEN_DIR, SCATTER_SRC)
    if not os.path.exists(scatter_path):
        print(f"  (skip scatter: {SCATTER_SRC} not generated yet)")
        return
    scatter = shape_card(Image.open(scatter_path))
    for n in range(1, 6):
        dest = os.path.join(MIRROR_DIR, f"wr_scatter_{n}.png")
        bak = dest + ".bak_new"
        if os.path.exists(dest) and not os.path.exists(bak):
            shutil.copy2(dest, bak)
        _atomic_save(scatter, dest)
    blur_dest = os.path.join(MIRROR_DIR, "wr_scatter_blur.png")
    bak = blur_dest + ".bak_new"
    if os.path.exists(blur_dest) and not os.path.exists(bak):
        shutil.copy2(blur_dest, bak)
    _atomic_save(vertical_smear(scatter), blur_dest)
    print("  scatter -> wr_scatter_1..5.png + wr_scatter_blur.png")


if __name__ == "__main__":
    print("Reshaping + repacking symbol atlas...")
    rebuild_atlas()
    print("Swapping wild + scatter sprites...")
    wire_wild_and_scatter()
    print("done")
