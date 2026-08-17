"""Key generated HUD chain columns (black pad) and install mode variants.

Sources (first hit wins):
  assets-raw/hud_wood/hud_chain_{base,small,super}_gen.png
  ~/.cursor/projects/.../assets/hud_chain_{base,small,super}_gen.png

Writes hud_chain.png / hud_chain_small.png / hud_chain_super.png,
downsampled to TARGET_W so the HUD (11–18px columns) does not squash
a 300px-wide gen.

    Run:  python tools/install_hud_chains.py
"""

from __future__ import annotations

import os
import shutil

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW_DIR = os.path.join(APP, "assets-raw", "hud_wood")
GEN_DIR = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
    )
)
TREES = (
    os.path.join(APP, "assets-src", "sprites", "tombstone"),
    os.path.join(APP, "assets-src", "assets", "sprites", "tombstone"),
    os.path.join(APP, "static", "assets", "sprites", "tombstone"),
)

# On-screen chain columns are 11–18px. Keep a little headroom for dpr.
TARGET_W = 56

VARIANTS = (
    ("base", "hud_chain.png"),
    ("small", "hud_chain_small.png"),
    ("super", "hud_chain_super.png"),
)


def find_src(kind: str) -> str:
    names = (f"hud_chain_{kind}_gen.png", f"hud_chain_{kind}.png")
    for folder in (RAW_DIR, GEN_DIR):
        for name in names:
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                return path
    raise SystemExit(f"missing generated chain: hud_chain_{kind}_gen.png")


def key_black(src: str) -> Image.Image:
    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    # keep dark iron; only the empty pad dies
    alpha = np.clip((lum - 8.0) / 18.0, 0.0, 1.0)
    # super ember sits in pits — don't eat near-black metal that still has chroma
    chroma = np.max(rgb, axis=2) - np.min(rgb, axis=2)
    alpha = np.clip(np.maximum(alpha, np.clip((chroma - 12.0) / 28.0, 0.0, 1.0)), 0.0, 1.0)
    rgba = np.dstack([rgb, alpha * 255.0]).astype(np.uint8)
    img = Image.fromarray(rgba, "RGBA")
    box = img.getchannel("A").point(lambda v: 255 if v > 14 else 0).getbbox()
    if not box:
        raise SystemExit(f"keyed empty: {src}")
    pad = 10
    img = img.crop(
        (
            max(0, box[0] - pad),
            max(0, box[1] - pad),
            min(img.width, box[2] + pad),
            min(img.height, box[3] + pad),
        )
    )
    if img.width > TARGET_W:
        h = max(1, round(img.height * TARGET_W / img.width))
        img = img.resize((TARGET_W, h), Image.LANCZOS)
    return img


def main() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    for kind, out_name in VARIANTS:
        src = find_src(kind)
        raw_keep = os.path.join(RAW_DIR, f"hud_chain_{kind}_gen.png")
        if os.path.abspath(src) != os.path.abspath(raw_keep):
            shutil.copy2(src, raw_keep)
        img = key_black(src)
        for tree in TREES:
            os.makedirs(tree, exist_ok=True)
            path = os.path.join(tree, out_name)
            img.save(path, optimize=True)
            print(f"wrote {os.path.relpath(path, APP)} {img.size}")


if __name__ == "__main__":
    main()
