"""Install the wood / bloody cell plates as a second Spine layer under H/L faces.

LOW  (L1-L5) sit on cells backplate.png
HIGH (H1-H5) sit on bloody cells backplate.png

The live faces stay the desktop vector idles (kit idle.png). The plate is its
own atlas region + slot on the card bone, so land / win / postWin move both
layers without the old mm_symbols face-swap. Sprite states (spin smear,
postWinStatic, paytable) get the same stack baked so SplitPanes / stories match.

Run: python tools/install_cell_backplates.py
"""

from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path

from PIL import Image, ImageFilter

import _symbol_faces as faces_lib

HERE = Path(__file__).resolve().parent
APP = HERE.parent
REPO = APP.parent.parent.parent

SRC_LOW = REPO / "cells backplate.png"
SRC_HIGH = REPO / "bloody cells backplate.png"
RAW_DIR = APP / "assets-raw" / "cell_backplates"

KIT = REPO / "VFXPACKSHEETS" / "tombstone-reborn-symbols"
READY = {
    "h1.webp": KIT / "h1-gunslinger" / "idle.png",
    "h2.webp": KIT / "h2-duchess" / "idle.png",
    "h3.webp": KIT / "h3-butcher" / "idle.png",
    "h4.webp": KIT / "h4-card-shark" / "idle.png",
    "h5.webp": KIT / "h5-preacher" / "idle.png",
    "l1.webp": KIT / "l1-bullet" / "idle.png",
    "l2.webp": KIT / "l2-whiskey" / "idle.png",
    "l3.webp": KIT / "l3-spur" / "idle.png",
    "l4.webp": KIT / "l4-horseshoe" / "idle.png",
    "l5.webp": KIT / "l5-dead-mans-hand" / "idle.png",
}

CELL = 300
CARD_H = 292
CARD_W = round(CARD_H * 0.775)
ATLAS_NAME = "symbolsStatic.v13"

# Empty cells on the existing 1210x1674 mm_symbols page (row under hm).
PLATE_BOUNDS = {
    "plate_high": (606, 908, 300, 300),
    "plate_low": (908, 908, 300, 300),
}

HIGHS = {"h1", "h2", "h3", "h4", "h5"}
LOWS = {"l1", "l2", "l3", "l4", "l5"}
PAYING = tuple(sorted(HIGHS | LOWS))

ATLAS_DIRS = [
    APP / "assets" / "sprites" / "symbolsStatic",
    APP / "static" / "assets" / "sprites" / "symbolsStatic",
    APP / "assets-src" / "assets" / "sprites" / "symbolsStatic",
    APP / "assets-src" / "sprites" / "symbolsStatic",
]
PAYTABLE_DIRS = [
    APP / "assets" / "paytable",
    APP / "static" / "assets" / "paytable",
    APP / "assets-src" / "paytable",
    APP / "assets-src" / "assets" / "paytable",
]
SPINE_DIRS = [
    APP / "assets" / "spines" / "mm_symbols",
    APP / "static" / "assets" / "spines" / "mm_symbols",
    APP / "assets-src" / "spines" / "mm_symbols",
    APP / "assets-src" / "assets" / "spines" / "mm_symbols",
]


def _atomic_save(img: Image.Image, dest: Path, **kwargs) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(f"{dest.stem}.__tmp__{dest.suffix}")
    img.save(tmp, **kwargs)
    for attempt in range(12):
        try:
            os.replace(tmp, dest)
            return
        except OSError:
            if attempt == 11:
                raise
            time.sleep(0.4)


def _atomic_write(dest: Path, text: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(f"{dest.stem}.__tmp__{dest.suffix}")
    tmp.write_text(text, encoding="utf-8")
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


def fit_in_cell(src: Image.Image, box_w: int, box_h: int) -> Image.Image:
    src = alpha_crop(src.convert("RGBA"))
    scale = min(box_w / src.width, box_h / src.height)
    nw = max(1, round(src.width * scale))
    nh = max(1, round(src.height * scale))
    fitted = src.resize((nw, nh), Image.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.paste(fitted, ((CELL - nw) // 2, (CELL - nh) // 2), fitted)
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


def process_plate(src: Path) -> Image.Image:
    if not src.is_file():
        raise SystemExit(f"missing plate: {src}")
    # Real alpha already — crop only, never color-key the wood.
    return fit_in_cell(Image.open(src), CARD_W, CARD_H)


def load_faces() -> dict[str, Image.Image]:
    faces: dict[str, Image.Image] = {}
    for frame, path in READY.items():
        if not path.is_file():
            raise SystemExit(f"missing face: {path}")
        src = Image.open(path)
        gid = frame.split(".")[0]
        faces[frame] = faces_lib.card_cell(src) if gid in LOWS else faces_lib.face_cell(src)
        print(f"  face {path.parent.name:18s} -> {frame}")
    return faces


def stack(plate: Image.Image, face: Image.Image) -> Image.Image:
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.alpha_composite(plate)
    cell.alpha_composite(face)
    return cell


def stamp_static(dest_dir: Path, cards: dict[str, Image.Image]) -> None:
    json_path = dest_dir / f"{ATLAS_NAME}.json"
    webp_path = dest_dir / f"{ATLAS_NAME}.webp"
    png_path = dest_dir / f"{ATLAS_NAME}.png"
    if not json_path.is_file() or not webp_path.is_file():
        print(f"  skip atlas: {dest_dir}")
        return
    atlas = json.loads(json_path.read_text(encoding="utf-8"))
    sheet = Image.open(webp_path).convert("RGBA")
    n = 0
    for frame, card in cards.items():
        meta = atlas["frames"].get(frame)
        if not meta:
            continue
        box = meta["frame"]
        fitted = card if card.size == (box["w"], box["h"]) else card.resize((box["w"], box["h"]), Image.LANCZOS)
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
    if png_path.is_file():
        _atomic_save(sheet, png_path)
    print(f"  stamped {n} static frames -> {dest_dir}")


def write_paytable(cards: dict[str, Image.Image]) -> None:
    for dest in PAYTABLE_DIRS:
        if not dest.is_dir() and dest != PAYTABLE_DIRS[0]:
            continue
        dest.mkdir(parents=True, exist_ok=True)
        for frame, card in cards.items():
            _atomic_save(card, dest / f"{frame.split('.')[0]}.png")
        print(f"  paytable -> {dest}")


def _parse_atlas(text: str) -> list[str]:
    return text.splitlines()


def stamp_spine(spine_dir: Path, faces: dict[str, Image.Image], plates: dict[str, Image.Image]) -> None:
    atlas_path = spine_dir / "mm_symbols.atlas"
    png_path = spine_dir / "mm_symbols.png"
    webp_path = spine_dir / "mm_symbols.webp"
    if not atlas_path.is_file() or not png_path.is_file():
        print(f"  skip spine: {spine_dir}")
        return
    lines = _parse_atlas(atlas_path.read_text(encoding="utf-8"))
    sheet = Image.open(png_path).convert("RGBA")

    # Re-stamp live faces into the existing h1..l5 regions (face only).
    n = 0
    for i, line in enumerate(lines):
        if not line.strip().startswith("bounds:"):
            continue
        name = lines[i - 1].strip()
        frame = f"{name}.webp"
        if frame not in faces:
            continue
        x, y, w, h = (int(v) for v in line.split(":")[1].split(","))
        sheet.paste(faces[frame].resize((w, h), Image.LANCZOS), (x, y))
        n += 1

    names = {lines[i - 1].strip() for i, line in enumerate(lines) if line.strip().startswith("bounds:")}
    for region, (x, y, w, h) in PLATE_BOUNDS.items():
        plate = plates[region].resize((w, h), Image.LANCZOS)
        slot = sheet.crop((x, y, x + w, y + h)).getchannel("A")
        occupied = sum(1 for p in slot.getdata() if p > 16)
        if occupied > (w * h * 0.02) and region not in names:
            raise SystemExit(f"mm_symbols {region} slot {x},{y} is not empty in {spine_dir}")
        sheet.paste(plate, (x, y))
        if region not in names:
            lines += [region, f"bounds:{x},{y},{w},{h}"]
        else:
            for i, line in enumerate(lines):
                if line.strip() == region and i + 1 < len(lines) and lines[i + 1].startswith("bounds:"):
                    lines[i + 1] = f"bounds:{x},{y},{w},{h}"
                    break
        n += 1

    _atomic_save(sheet, png_path)
    if webp_path.is_file() or True:
        _atomic_save(sheet, webp_path, lossless=True)
    _atomic_write(atlas_path, "\n".join(lines).rstrip() + "\n")
    print(f"  spine atlas +{n} -> {spine_dir}")


def plate_region_for(gid: str) -> str:
    if gid in HIGHS:
        return "plate_high"
    if gid in LOWS:
        return "plate_low"
    raise ValueError(gid)


def patch_skeleton(path: Path) -> bool:
    gid = path.stem
    if gid not in PAYING:
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    plate = plate_region_for(gid)
    slot_name = f"{gid}_plate"
    slots = data.setdefault("slots", [])
    if not any(slot.get("name") == slot_name for slot in slots):
        slots.insert(0, {"name": slot_name, "bone": "card", "attachment": plate})
    skins = data.get("skins") or []
    if skins:
        atts = skins[0].setdefault("attachments", {})
        atts[slot_name] = {plate: {"x": 0, "y": 0, "width": CELL, "height": CELL}}
    anims = data.setdefault("animations", {})
    anims[f"{gid}_static"] = {
        "bones": {"card": {"scale": [{"x": 1.0, "y": 1.0}]}}
    }
    _atomic_write(path, json.dumps(data, separators=(",", ":")))
    return True


def patch_all_skeletons() -> None:
    src = APP / "assets-src" / "assets" / "spines" / "mm_symbols"
    if not (src / "h1.json").is_file():
        src = APP / "static" / "assets" / "spines" / "mm_symbols"
    n = 0
    for gid in PAYING:
        src_json = src / f"{gid}.json"
        if not src_json.is_file():
            raise SystemExit(f"missing skeleton {src_json}")
        patch_skeleton(src_json)
        n += 1
        for dest in SPINE_DIRS:
            dest.mkdir(parents=True, exist_ok=True)
            target = dest / f"{gid}.json"
            if target.resolve() == src_json.resolve():
                continue
            shutil.copy2(src_json, target)
    print(f"  patched {n} skeletons + copied to spine trees")


def main() -> None:
    print("Installing cell backplates (LOW wood / HIGH blood)...")
    plate_low = process_plate(SRC_LOW)
    plate_high = process_plate(SRC_HIGH)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    _atomic_save(plate_low, RAW_DIR / "plate_low.png")
    _atomic_save(plate_high, RAW_DIR / "plate_high.png")
    print(f"  plates {plate_low.size} -> {RAW_DIR}")

    faces = load_faces()
    stacked = {}
    for frame, face in faces.items():
        gid = frame.split(".")[0]
        plate = plate_high if gid in HIGHS else plate_low
        stacked[frame] = stack(plate, face)

    for dest in ATLAS_DIRS:
        stamp_static(dest, stacked)
    write_paytable(stacked)
    plates = {"plate_high": plate_high, "plate_low": plate_low}
    for dest in SPINE_DIRS:
        stamp_spine(dest, faces, plates)
    patch_all_skeletons()
    preview = APP / "assets-raw" / "cell_backplates" / "preview"
    preview.mkdir(parents=True, exist_ok=True)
    _atomic_save(stacked["h1.webp"], preview / "h1_plated.png")
    _atomic_save(stacked["l1.webp"], preview / "l1_plated.png")
    print("done")
    from verify_cell_backplates import main as verify

    if verify() != 0:
        raise SystemExit("verify_cell_backplates failed")


if __name__ == "__main__":
    main()
