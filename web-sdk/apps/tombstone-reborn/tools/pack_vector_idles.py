"""Stamp the desktop TR2 symbol sheet onto the live v13 atlas in place.

Does not invent a new atlas name. Same frame boxes, same asset keys.
Copies Desktop/new symbols into VFXPACKSHEETS/tombstone-reborn-symbols, then
stamps atlas + spine + paytable + feature PNGs.

Run: python tools/pack_vector_idles.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time

import shutil

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
REPO = os.path.normpath(os.path.join(APP, "..", "..", ".."))
KIT = os.path.join(REPO, "VFXPACKSHEETS", "tombstone-reborn-symbols")
NEW = os.path.join(
	os.path.expanduser("~"),
	"Desktop",
	"TR2 FInal symbopls sheet",
	"TR2 FInal symbopls sheet for TR2 Symbols",
	"new symbols",
)

CELL = 300
CARD_H = 292
CARD_W = round(CARD_H * 0.775)
ATLAS = "symbolsStatic.v13"

# Sheet row1 LTR = H1-H5, row2 LTR = L1-L5, row3 LTR = W / SU / S / GS / SH.
# Island names are not left-to-right; this map is from the art.
PROP = {
	"h1-gunslinger": "prop_03.png",
	"h2-duchess": "prop_02.png",
	"h3-butcher": "prop_04.png",
	"h4-card-shark": "prop_05.png",
	"h5-preacher": "prop_01.png",
	"l1-bullet": "prop_08.png",
	"l2-whiskey": "prop_06.png",
	"l3-spur": "prop_09.png",
	"l4-horseshoe": "prop_10.png",
	"l5-dead-mans-hand": "prop_07.png",
	"w-revolver": "prop_13.png",
	"s-tombstone": "prop_12.png",
	"su-super-scatter": "prop_15.png",
	"gs-gunsmoke": "prop_14.png",
	"sh-mark": "prop_11.png",
}

READY = {
	"h1.webp": os.path.join(KIT, "h1-gunslinger", "idle.png"),
	"h2.webp": os.path.join(KIT, "h2-duchess", "idle.png"),
	"h3.webp": os.path.join(KIT, "h3-butcher", "idle.png"),
	"h4.webp": os.path.join(KIT, "h4-card-shark", "idle.png"),
	"h5.webp": os.path.join(KIT, "h5-preacher", "idle.png"),
	"l1.webp": os.path.join(KIT, "l1-bullet", "idle.png"),
	"l2.webp": os.path.join(KIT, "l2-whiskey", "idle.png"),
	"l3.webp": os.path.join(KIT, "l3-spur", "idle.png"),
	"l4.webp": os.path.join(KIT, "l4-horseshoe", "idle.png"),
	"l5.webp": os.path.join(KIT, "l5-dead-mans-hand", "idle.png"),
	"w.png": os.path.join(KIT, "w-revolver", "idle.png"),
	"s.png": os.path.join(KIT, "s-tombstone", "idle.png"),
}

FEATURE_PNGS = {
	"wr_wild.png": os.path.join(KIT, "w-revolver", "idle.png"),
	"tr_scatter.png": os.path.join(KIT, "s-tombstone", "idle.png"),
	"tr_scatter_super.png": os.path.join(KIT, "su-super-scatter", "idle.png"),
	"tr_gs.png": os.path.join(KIT, "gs-gunsmoke", "idle.png"),
	"tr_sh.png": os.path.join(KIT, "sh-mark", "idle.png"),
}

MIRROR_DIRS = [
	os.path.join(APP, "assets", "sprites", "mirror"),
	os.path.join(APP, "static", "assets", "sprites", "mirror"),
	os.path.join(APP, "assets-src", "sprites", "mirror"),
	os.path.join(APP, "assets-src", "assets", "sprites", "mirror"),
]

ATLAS_DIRS = [
    os.path.join(APP, "assets", "sprites", "symbolsStatic"),
    os.path.join(APP, "static", "assets", "sprites", "symbolsStatic"),
    os.path.join(APP, "assets-src", "assets", "sprites", "symbolsStatic"),
    os.path.join(APP, "assets-src", "sprites", "symbolsStatic"),
]
PAYTABLE_DIRS = [
    os.path.join(APP, "assets", "paytable"),
    os.path.join(APP, "static", "assets", "paytable"),
    os.path.join(APP, "assets-src", "paytable"),
    os.path.join(APP, "assets-src", "assets", "paytable"),
]
SPINE_DIRS = [
    os.path.join(APP, "assets", "spines", "mm_symbols"),
    os.path.join(APP, "static", "assets", "spines", "mm_symbols"),
    os.path.join(APP, "assets-src", "spines", "mm_symbols"),
    os.path.join(APP, "assets-src", "assets", "spines", "mm_symbols"),
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


def alpha_crop(im: Image.Image) -> Image.Image:
    bbox = im.getchannel("A").getbbox()
    return im.crop(bbox) if bbox else im


def fit_cell(src: Image.Image, w: int = CELL, h: int = CELL) -> Image.Image:
    src = alpha_crop(src.convert("RGBA"))
    box_w = max(1, CARD_W - 12)
    box_h = max(1, CARD_H - 12)
    scale = min(box_w / src.width, box_h / src.height)
    nw = max(1, round(src.width * scale))
    nh = max(1, round(src.height * scale))
    fitted = src.resize((nw, nh), Image.LANCZOS)
    cell = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cell.paste(fitted, ((w - nw) // 2, (h - nh) // 2), fitted)
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


def load_ready() -> dict[str, Image.Image]:
    cards: dict[str, Image.Image] = {}
    for frame, path in READY.items():
        if not os.path.isfile(path):
            print(f"  skip missing {path}")
            continue
        src = Image.open(path).convert("RGBA")
        cards[frame] = fit_cell(src)
        print(f"  {os.path.basename(os.path.dirname(path)):18s} {src.size} -> {frame}")
    return cards


def stamp_atlas(dest_dir: str, cards: dict[str, Image.Image]) -> None:
    json_path = os.path.join(dest_dir, f"{ATLAS}.json")
    webp_path = os.path.join(dest_dir, f"{ATLAS}.webp")
    png_path = os.path.join(dest_dir, f"{ATLAS}.png")
    if not os.path.isfile(json_path) or not os.path.isfile(webp_path):
        print(f"  skip atlas: {dest_dir}")
        return
    with open(json_path, encoding="utf-8") as handle:
        atlas = json.load(handle)
    sheet = Image.open(webp_path).convert("RGBA")
    n = 0
    for frame, card in cards.items():
        meta = atlas["frames"].get(frame)
        if not meta:
            continue
        box = meta["frame"]
        fitted = card if (card.width, card.height) == (box["w"], box["h"]) else card.resize(
            (box["w"], box["h"]), Image.LANCZOS
        )
        sheet.paste(fitted, (box["x"], box["y"]))
        n += 1
        blur_name = frame.replace(".", "_blur.")
        blur_meta = atlas["frames"].get(blur_name)
        if blur_meta:
            b = blur_meta["frame"]
            smear = vertical_smear(fitted)
            if smear.size != (b["w"], b["h"]):
                smear = smear.resize((b["w"], b["h"]), Image.LANCZOS)
            sheet.paste(smear, (b["x"], b["y"]))
            n += 1
    _atomic_save(sheet, webp_path, lossless=True)
    if os.path.isfile(png_path):
        _atomic_save(sheet, png_path)
    print(f"  stamped {n} frames -> {dest_dir}")


def write_paytable(cards: dict[str, Image.Image]) -> None:
    for dest in PAYTABLE_DIRS:
        if not os.path.isdir(dest) and dest != PAYTABLE_DIRS[0]:
            continue
        os.makedirs(dest, exist_ok=True)
        for frame, card in cards.items():
            _atomic_save(card, os.path.join(dest, f"{frame.split('.')[0]}.png"))
        print(f"  paytable -> {dest}")


def patch_spine(spine_dir: str, cards: dict[str, Image.Image]) -> None:
    atlas_path = os.path.join(spine_dir, "mm_symbols.atlas")
    png_path = os.path.join(spine_dir, "mm_symbols.png")
    if not os.path.isfile(atlas_path) or not os.path.isfile(png_path):
        return
    lines = open(atlas_path, encoding="utf-8").read().splitlines()
    sheet = Image.open(png_path).convert("RGBA")
    n = 0
    for i, line in enumerate(lines):
        if not line.strip().startswith("bounds:"):
            continue
        name = lines[i - 1].strip()
        frame = f"{name}.webp" if f"{name}.webp" in cards else f"{name}.png"
        if frame not in cards:
            continue
        x, y, w, h = (int(v) for v in line.split(":")[1].split(","))
        sheet.paste(cards[frame].resize((w, h), Image.LANCZOS), (x, y))
        n += 1
    if n:
        _atomic_save(sheet, png_path)
        webp = os.path.join(spine_dir, "mm_symbols.webp")
        if os.path.isfile(webp):
            _atomic_save(sheet, webp, lossless=True)
        print(f"  spine patched {n} -> {spine_dir}")


def install_kit() -> None:
    if not os.path.isdir(NEW):
        raise SystemExit(f"missing new symbols: {NEW}")
    for slug, filename in PROP.items():
        src = os.path.join(NEW, filename)
        if not os.path.isfile(src):
            print(f"  skip missing {filename}")
            continue
        dest_dir = os.path.join(KIT, slug)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "idle.png")
        shutil.copy2(src, dest)
        print(f"  kit {filename} -> {slug}/idle.png")


def write_features() -> None:
    for name, path in FEATURE_PNGS.items():
        if not os.path.isfile(path):
            print(f"  skip feature {name}")
            continue
        card = fit_cell(Image.open(path).convert("RGBA"))
        for dest in MIRROR_DIRS:
            if not os.path.isdir(dest) and dest != MIRROR_DIRS[0]:
                continue
            os.makedirs(dest, exist_ok=True)
            _atomic_save(card, os.path.join(dest, name))
        print(f"  feature {name}")


def write_expanding_wild() -> None:
    script = os.path.join(HERE, "make_expanding_wild.py")
    subprocess.check_call([sys.executable, script], cwd=APP)
    src = os.path.join(APP, "assets", "sprites", "mirror", "wr_wild_expand.png")
    if not os.path.isfile(src):
        return
    card = Image.open(src).convert("RGBA")
    for dest in MIRROR_DIRS:
        os.makedirs(dest, exist_ok=True)
        _atomic_save(card, os.path.join(dest, "wr_wild_expand.png"))
    pay = os.path.join(APP, "static", "assets", "paytable", "wexpand.png")
    if os.path.isfile(pay):
        tile = Image.open(pay).convert("RGBA")
        for dest in PAYTABLE_DIRS:
            os.makedirs(dest, exist_ok=True)
            _atomic_save(tile, os.path.join(dest, "wexpand.png"))
    print("  feature wr_wild_expand.png")


if __name__ == "__main__":
    print("Installing desktop sheet symbols onto live v13...")
    install_kit()
    cards = load_ready()
    if not cards:
        raise SystemExit("no ready idles")
    for dest in ATLAS_DIRS:
        stamp_atlas(dest, cards)
    for dest in SPINE_DIRS:
        patch_spine(dest, cards)
    write_paytable(cards)
    write_features()
    write_expanding_wild()
    print("done")
