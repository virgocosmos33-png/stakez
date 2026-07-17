"""Repack the Madam Mirror (ways app) symbolsStatic atlas with the horror icons.

- Keys out the flat light background of generated icons via border flood-fill
  (icons all have thick dark outlines, so interior lights are preserved), also
  detecting enclosed checkerboard holes.
- Fits each icon into a 200x200 cell (same sourceSize as the original atlas).
- Carries the legacy frames the game still needs (explodedW.png used by the
  wild post-win state, h5.webp kept alive for the leftover ways sample stories)
  out of the original atlas unchanged.
- Writes symbolsStatic.png / .webp / .json (TexturePacker JSON-hash format,
  untrimmed, unrotated) next to the originals, backing the originals up first.

Run:  python tools/repack_symbols.py
"""

import json
import os
import shutil
from collections import deque

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic"))
BACKUP_DIR = os.path.join(ATLAS_DIR, "backup_original")
ICON_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"

CELL = 300          # cell size; full-bleed card art benefits from the extra resolution
CONTENT = 292       # max icon size inside the cell for keyed (cut-out) icons
PADDING = 2         # spacing between packed frames
COLUMNS = 4

# generated icon file -> frame name expected by SYMBOL_INFO_MAP / atlas json
# card_* art is full-bleed (fills the whole square, Mental-style plates):
# no keying, just resize to the cell.
FULL_BLEED_ICONS = {
    "card_h1_madam.png": "h1.webp",
    "card_h2_twins.png": "h2.webp",
    "card_h3_client.png": "h3.webp",
    "card_h4_cat.png": "h4.webp",
    "card_l1_tower.png": "l1.webp",
    "card_l2_candelabra.png": "l2.webp",
    "card_l3_crystalball.png": "l3.webp",
    "card_l4_locket.png": "l4.webp",
    "card_l5_absinthe.png": "l5.webp",
    "card_w_wild.png": "w.png",
    "card_s_scatter.png": "s.png",
    "card_hm_intact.png": "hm_intact.png",
    "card_hm_cracked.png": "hm_cracked.png",
}
NEW_ICONS: dict[str, str] = {}

# frames not being replaced, carried over from the original atlas unchanged
LEGACY_FRAMES = ["explodedW.png", "h5.webp"]


def is_background(px):
    r, g, b = px[:3]
    lo, hi = min(r, g, b), max(r, g, b)
    return lo >= 205 and (hi - lo) <= 18


def key_out_background(im: Image.Image) -> Image.Image:
    """Flood-fill neutral light pixels reachable from the border into transparency."""
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    background = bytearray(w * h)

    queue = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_background(px[x, y]) and not background[y * w + x]:
                background[y * w + x] = 1
                queue.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_background(px[x, y]) and not background[y * w + x]:
                background[y * w + x] = 1
                queue.append((x, y))

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                idx = ny * w + nx
                if not background[idx] and is_background(px[nx, ny]):
                    background[idx] = 1
                    queue.append((nx, ny))

    # enclosed holes (e.g. a ring's centre) that still show the baked checkerboard:
    # find leftover background-like components and key the ones showing the
    # checkerboard's two-plateau signature (~229 and ~253 in similar amounts)
    visited = bytearray(background)
    for sy in range(h):
        for sx in range(w):
            if visited[sy * w + sx] or not is_background(px[sx, sy]):
                continue
            component = []
            dark = light = 0
            queue = deque([(sx, sy)])
            visited[sy * w + sx] = 1
            while queue:
                x, y = queue.popleft()
                component.append(y * w + x)
                lum = min(px[x, y][:3])
                if lum <= 240:
                    dark += 1
                elif lum >= 246:
                    light += 1
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and not visited[ny * w + nx] and is_background(px[nx, ny]):
                        visited[ny * w + nx] = 1
                        queue.append((nx, ny))
            n = len(component)
            if n >= 200 and 0.2 <= dark / n <= 0.8 and 0.2 <= light / n <= 0.8:
                for idx in component:
                    background[idx] = 1

    alpha = Image.frombytes("L", (w, h), bytes(255 if not b else 0 for b in background))
    # erode 1px to eat the light halo left at the silhouette, then soften
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))

    out = im.convert("RGBA")
    out.putalpha(alpha)
    return out


def to_cell(im: Image.Image) -> Image.Image:
    """Trim to the opaque bounding box, then fit centered into a CELLxCELL canvas."""
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im = im.crop(bbox)
    scale = min(CONTENT / im.width, CONTENT / im.height)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.paste(im, ((CELL - im.width) // 2, (CELL - im.height) // 2), im)
    return cell


def extract_legacy(original: Image.Image, frame: dict) -> Image.Image:
    """Rebuild a legacy frame from the original atlas onto a full sourceSize canvas."""
    f = frame["frame"]
    if frame.get("rotated"):
        region = original.crop((f["x"], f["y"], f["x"] + f["h"], f["y"] + f["w"]))
        region = region.transpose(Image.ROTATE_90)  # undo TexturePacker's 90 CW packing
    else:
        region = original.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
    src = frame["spriteSourceSize"]
    cell = Image.new("RGBA", (frame["sourceSize"]["w"], frame["sourceSize"]["h"]), (0, 0, 0, 0))
    cell.paste(region, (src["x"], src["y"]))
    return cell


if __name__ == "__main__":
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for name in ("symbolsStatic.json", "symbolsStatic.webp", "symbolsStatic.png"):
        src = os.path.join(ATLAS_DIR, name)
        dst = os.path.join(BACKUP_DIR, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

    with open(os.path.join(BACKUP_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        original_json = json.load(f)
    original_img = Image.open(os.path.join(BACKUP_DIR, "symbolsStatic.webp")).convert("RGBA")

    cells: dict[str, Image.Image] = {}
    for icon_file, frame_name in NEW_ICONS.items():
        im = Image.open(os.path.join(ICON_DIR, icon_file))
        cells[frame_name] = to_cell(key_out_background(im))
        print(f"processed {icon_file} -> {frame_name}")
    for icon_file, frame_name in FULL_BLEED_ICONS.items():
        im = Image.open(os.path.join(ICON_DIR, icon_file)).convert("RGBA")
        cells[frame_name] = im.resize((CELL, CELL), Image.LANCZOS)
        print(f"processed full-bleed {icon_file} -> {frame_name}")
    for frame_name in LEGACY_FRAMES:
        legacy = extract_legacy(original_img, original_json["frames"][frame_name])
        cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
        cell.paste(legacy, ((CELL - legacy.width) // 2, (CELL - legacy.height) // 2))
        cells[frame_name] = cell
        print(f"carried over {frame_name}")

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
            "app": "repack_symbols.py",
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
