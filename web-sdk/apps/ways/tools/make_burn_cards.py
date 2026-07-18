"""Bake POSTWIN 'burning card' sprites from the user's reference art.

The art-direction reference (tools/burn_ref.png) is the l1 ace card engulfed
in a ring of green plasma fire around its circular medallion. This tool:

1. extracts the green flame layer from the reference (green-dominance key,
   letter rim-light suppressed in the center so no ghost 'A' leaks onto
   other symbols),
2. measures the reference ring radius and the radius of OUR card medallion,
3. composites the flame ring (scaled + seeded rotation/flip per symbol, plus
   a soft inner ambient glow) onto every paying/reel symbol, and
4. repacks the symbolsStatic atlas with the new `<name>_burn` frames
   (originals and `_blur` smear frames preserved byte-for-byte).

postWin routes at these sprites: after the win animation the symbol rests as
a burned, plasma-marked card - the main postwin theme for ALL symbols.

Run:  python tools/make_burn_cards.py
"""

from __future__ import annotations

import json
import math
import os
import shutil

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(
    os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic")
)
BACKUP_DIR = os.path.join(ATLAS_DIR, "backup_pre_burn")
REF_PATH = os.path.join(HERE, "burn_ref.png")

CELL = 300
PADDING = 2
COLUMNS = 4
SMEAR_H = 480

# symbols that get a burn frame (postWin resting look); hm resolves to its
# revealed symbol before wins so the mirror itself never rests in postWin
BURN_SOURCES = [
    "h1.webp", "h2.webp", "h3.webp", "h4.webp", "h5.webp",
    "l1.webp", "l2.webp", "l3.webp", "l4.webp", "l5.webp",
    "w.png", "s.png",
]


def burn_name(frame_name: str) -> str:
    stem, ext = frame_name.rsplit(".", 1)
    return f"{stem}_burn.{ext}"


def extract_frame(atlas_img: Image.Image, frame: dict) -> Image.Image:
    f = frame["frame"]
    return atlas_img.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))


def extract_flame_layer(ref: Image.Image) -> tuple[np.ndarray, float]:
    """Green-dominance key of the reference. Returns premultiplied float RGB
    flame layer (H, W, 3, 0..1) and the measured ring radius in ref pixels."""
    rgb = np.asarray(ref.convert("RGB"), dtype=np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    # green dominance: catches deep green bodies, yellow-green tongues and
    # white-green cores while rejecting the gold frame and olive card art
    dominance = g - np.maximum(r, b)
    alpha = np.clip((dominance - 12.0) / 70.0, 0.0, 1.0)
    # weight by brightness so dim green noise fades out
    alpha *= np.clip(g / 255.0, 0.0, 1.0) ** 0.7

    h, w = alpha.shape
    cy, cx = (h - 1) / 2, (w - 1) / 2
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    radius = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)

    # ring radius = peak of the alpha-weighted radial histogram
    bins = np.arange(0, int(radius.max()) + 2)
    hist, _ = np.histogram(radius.ravel(), bins=bins, weights=alpha.ravel())
    ring_radius = float(np.argmax(hist))

    # suppress the letter rim-light in the middle (would ghost an 'A' onto
    # every other symbol); keep the glow that hugs the ring from inside
    inner_kill = np.clip((radius - ring_radius * 0.52) / (ring_radius * 0.14), 0.0, 1.0)
    alpha *= inner_kill

    flame = (rgb / 255.0) * alpha[..., None]
    return flame.astype(np.float32), ring_radius


def measure_medallion_radius(card: Image.Image) -> float:
    """Radius of the circular plate: peak of the angular-averaged luminance
    gradient in the outer half of the card."""
    lum = np.asarray(card.convert("L"), dtype=np.float32)
    h, w = lum.shape
    cy, cx = (h - 1) / 2, (w - 1) / 2
    samples = []
    for radius in range(int(w * 0.30), int(w * 0.50)):
        acc = 0.0
        n = 64
        for k in range(n):
            angle = 2 * math.pi * k / n
            x = int(cx + math.cos(angle) * radius)
            y = int(cy + math.sin(angle) * radius)
            if 0 <= x < w and 0 <= y < h:
                acc += lum[y, x]
        samples.append(acc / n)
    profile = np.asarray(samples)
    grad = np.abs(np.diff(profile))
    return float(int(w * 0.30) + int(np.argmax(grad)))


def compose_burn(card: Image.Image, flame: np.ndarray, ring_radius: float,
                 target_radius: float, seed: int) -> Image.Image:
    """Additively burn the flame layer onto a card with a seeded orientation
    and an inner ambient glow."""
    base = np.asarray(card.convert("RGB"), dtype=np.float32) / 255.0

    # seeded orientation: rotate in 90deg steps + optional mirror
    layer = flame
    for _ in range(seed % 4):
        layer = np.rot90(layer)
    if (seed // 4) % 2:
        layer = layer[:, ::-1, :]

    # scale so the reference ring lands just inside OUR medallion edge
    scale = (target_radius * 0.97) / ring_radius
    src = Image.fromarray((np.clip(layer, 0, 1) * 255).astype(np.uint8), "RGB")
    new_size = (int(src.width * scale), int(src.height * scale))
    src = src.resize(new_size, Image.LANCZOS)

    canvas = np.zeros((CELL, CELL, 3), dtype=np.float32)
    arr = np.asarray(src, dtype=np.float32) / 255.0
    ox = (CELL - src.width) // 2
    oy = (CELL - src.height) // 2
    x0, y0 = max(0, ox), max(0, oy)
    x1 = min(CELL, ox + src.width)
    y1 = min(CELL, oy + src.height)
    canvas[y0:y1, x0:x1] = arr[y0 - oy : y1 - oy, x0 - ox : x1 - ox]

    # bloom: blurred copy of the flames doubles as the fire's own light
    from PIL import ImageFilter

    bloom_img = Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8), "RGB").filter(
        ImageFilter.GaussianBlur(9)
    )
    bloom = np.asarray(bloom_img, dtype=np.float32) / 255.0

    # soft green ambience inside the ring so the emblem sits in the glow
    yy, xx = np.mgrid[0:CELL, 0:CELL].astype(np.float32)
    radius = np.sqrt((xx - CELL / 2) ** 2 + (yy - CELL / 2) ** 2)
    ambience = np.clip(1 - radius / target_radius, 0, 1) ** 1.6 * 0.19
    glow = np.zeros_like(canvas)
    glow[..., 0] = ambience * 0.25
    glow[..., 1] = ambience
    glow[..., 2] = ambience * 0.45

    fire = np.clip(canvas * 1.4 + bloom * 0.7 + glow, 0, 1)
    out = 1.0 - (1.0 - base) * (1.0 - fire)  # screen
    out8 = (np.clip(out, 0, 1) * 255).astype(np.uint8)
    result = Image.fromarray(out8, "RGB").convert("RGBA")
    # preserve original alpha (cards are full-bleed opaque, but keep exact)
    result.putalpha(card.convert("RGBA").split()[3])
    return result


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

    # carry every existing frame at its native size (drop stale _burn frames)
    frames_by_name: dict[str, Image.Image] = {
        name: extract_frame(current_img, frame)
        for name, frame in current_json["frames"].items()
        if "_burn." not in name
    }

    ref = Image.open(REF_PATH)
    flame, ring_radius = extract_flame_layer(ref)
    print(f"reference ring radius: {ring_radius:.0f}px of {ref.size[0]}")

    medallion = measure_medallion_radius(frames_by_name["l1.webp"])
    print(f"card medallion radius: {medallion:.0f}px of {CELL}")

    burns: dict[str, Image.Image] = {}
    for i, name in enumerate(BURN_SOURCES):
        if name not in frames_by_name:
            print(f"  (skip {name}: not in atlas)")
            continue
        burns[burn_name(name)] = compose_burn(
            frames_by_name[name], flame, ring_radius, medallion, seed=i * 3 + 1
        )
        print(f"burned {name} -> {burn_name(name)}")

    # sheet layout: originals (300x300) | smears (300x480) | burns (300x300)
    originals = sorted(n for n in frames_by_name if "_blur." not in n)
    smears = sorted(n for n in frames_by_name if "_blur." in n)
    burn_names = sorted(burns.keys())

    sheet_w = COLUMNS * (CELL + PADDING) + PADDING

    def grid_height(count: int, cell_h: int) -> int:
        rows = (count + COLUMNS - 1) // COLUMNS
        return rows * (cell_h + PADDING)

    originals_h = grid_height(len(originals), CELL) + PADDING
    smears_h = grid_height(len(smears), SMEAR_H)
    burns_h = grid_height(len(burn_names), CELL)
    sheet_h = originals_h + smears_h + burns_h + PADDING
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

    def pack(names: list[str], images: dict[str, Image.Image], y_base: int, cell_h: int) -> int:
        for i, name in enumerate(names):
            col, row = i % COLUMNS, i // COLUMNS
            x = PADDING + col * (CELL + PADDING)
            y = y_base + row * (cell_h + PADDING)
            sheet.paste(images[name], (x, y))
            frames[name] = frame_entry(x, y, images[name].width, images[name].height)
        return y_base + grid_height(len(names), cell_h)

    y_next = pack(originals, frames_by_name, PADDING, CELL)
    y_next = pack(smears, frames_by_name, y_next, SMEAR_H)
    pack(burn_names, burns, y_next, CELL)

    atlas = {
        "frames": frames,
        "meta": {
            "app": "make_burn_cards.py",
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
