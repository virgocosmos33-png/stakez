"""Key + install THE WHITE ROOM bottom counter rail (WAYS | FREE SPINS | WIN).

Reads a generated master from COUNTER_FRAME_SRC (or the default Cursor assets
folder) named frame_bottom_compartments_gen.png, keys near-black / pure black
background to alpha, trims, and writes:

  static/assets/sprites/mirror/frame_bottom_compartments.png

Invoked by DramaStudioMCP regenerate_assets scope `counters` / `hud`.
Does NOT touch spin-button chrome.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
GEN_DIR = Path(
    os.environ.get(
        "COUNTER_FRAME_SRC",
        Path.home()
        / ".cursor"
        / "projects"
        / "c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
        / "assets",
    )
)
OUT_DIR = HERE.parent / "static" / "assets" / "sprites" / "mirror"
SRC_NAME = "frame_bottom_compartments_gen.png"
OUT_NAME = "frame_bottom_compartments.png"
BG_THRESH = 55


def key_background(rgb: Image.Image) -> np.ndarray:
    w, h = rgb.size
    work = rgb.copy()
    sentinel = (255, 0, 255)
    seeds = [
        (0, 0),
        (w - 1, 0),
        (0, h - 1),
        (w - 1, h - 1),
        (w // 2, 0),
        (w // 2, h - 1),
        (0, h // 2),
        (w - 1, h // 2),
    ]
    for seed in seeds:
        ImageDraw.floodfill(work, seed, sentinel, thresh=BG_THRESH)
    arr = np.asarray(work)
    is_bg = np.all(arr == np.array(sentinel), axis=-1)
    return np.where(is_bg, 0, 255).astype(np.uint8)


def gold_fraction(img: Image.Image) -> float:
    arr = np.asarray(img.convert("RGBA"))
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    mask = (a > 40) & (r > 140) & (g > 90) & (b < 120) & (r > g) & (r > b)
    opaque = int((a > 40).sum()) or 1
    return float(mask.sum()) / opaque


def main() -> None:
    src = GEN_DIR / SRC_NAME
    if not src.is_file():
        raise SystemExit(f"missing generated master: {src}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bak = OUT_DIR / "frame_bottom_compartments_GOLD_BAK.png"
    dest = OUT_DIR / OUT_NAME
    if dest.is_file() and not bak.is_file():
        shutil.copy2(dest, bak)
        print(f"backed up gold original -> {bak.name}", flush=True)

    rgba_in = Image.open(src).convert("RGBA")
    # If already transparent, keep alpha; else key black plate.
    if int(np.asarray(rgba_in)[..., 3].min()) < 10:
        img = rgba_in
        print("source already has transparency; skipping black key", flush=True)
    else:
        rgb = rgba_in.convert("RGB")
        alpha = key_background(rgb)
        img = Image.fromarray(np.dstack([np.asarray(rgb), alpha]), "RGBA")

    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # Lock to working bak pixel size / aspect so FrameMorphHud WELL fractions
    # (measured on GOLD_BAK) stay valid. AI gens that drift in size get resampled.
    target_w, target_h = 1524, 462
    if bak.is_file():
        with Image.open(bak) as bak_im:
            target_w, target_h = bak_im.size
    if img.size != (target_w, target_h):
        print(
            f"resizing {img.width}x{img.height} -> {target_w}x{target_h} "
            f"(bak-locked geometry)",
            flush=True,
        )
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    gf = gold_fraction(img)
    img.save(dest)
    print(
        f"{OUT_NAME}: {img.width}x{img.height} goldish={gf*100:.2f}% "
        f"-> {dest} ({dest.stat().st_size} bytes)",
        flush=True,
    )
    if gf > 0.03:
        raise SystemExit(
            f"FAIL: still looks gold ({gf*100:.1f}% goldish pixels). "
            "Regenerate white/silver master before shipping."
        )
    print("OK: gold chrome below threshold", flush=True)


if __name__ == "__main__":
    main()
