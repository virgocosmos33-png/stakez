"""Install generated HUD nameplate pallets (WAYS / MULTI / WIN / FREE SPINS).

Sources (first hit wins):
  ~/.cursor/projects/.../assets/wood_pallet_{stem}.png
  assets-raw/hud_wood/wood_pallet_{stem}.png

Keys the near-white studio pad, crops to the plank, downsamples, and writes
wood_pallet_*.png into assets-src + static/assets. Base plus small/super
bonus grades for WAYS / MULTI / WIN.

    Run:  python tools/install_hud_pallets.py
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

TARGET_W = 720

STEMS = (
	"ways",
	"multi",
	"win",
	"spins",
	"ways_small",
	"multi_small",
	"win_small",
	"ways_super",
	"multi_super",
	"win_super",
)


def find_src(stem: str) -> str:
    name = f"wood_pallet_{stem}.png"
    for folder in (GEN_DIR, RAW_DIR):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            return path
    raise SystemExit(f"missing generated pallet: {name}")


def key_white(src: str) -> Image.Image:
    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    chroma = np.max(rgb, axis=2) - np.min(rgb, axis=2)
    # studio pad is ~245–254 grey; branded bone letters sit ~150–220 and warm
    pad = (lum > 232.0) & (chroma < 16.0)
    alpha = np.where(pad, 0.0, 255.0)
    rgba = np.dstack([rgb, alpha]).astype(np.uint8)
    img = Image.fromarray(rgba, "RGBA")
    box = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if not box:
        raise SystemExit(f"keyed empty: {src}")
    pad_px = 8
    img = img.crop(
        (
            max(0, box[0] - pad_px),
            max(0, box[1] - pad_px),
            min(img.width, box[2] + pad_px),
            min(img.height, box[3] + pad_px),
        )
    )
    if img.width > TARGET_W:
        h = max(1, round(img.height * (TARGET_W / img.width)))
        img = img.resize((TARGET_W, h), Image.LANCZOS)
    return img


def main() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    for stem in STEMS:
        src = find_src(stem)
        raw_copy = os.path.join(RAW_DIR, f"wood_pallet_{stem}.png")
        if os.path.abspath(src) != os.path.abspath(raw_copy):
            shutil.copy2(src, raw_copy)
        img = key_white(src)
        name = f"wood_pallet_{stem}.png"
        for tree in TREES:
            os.makedirs(tree, exist_ok=True)
            path = os.path.join(tree, name)
            tmp = path + ".tmp.png"
            img.save(tmp)
            os.replace(tmp, path)
            print(f"wrote {os.path.relpath(path, APP)} {img.size}")


if __name__ == "__main__":
    main()
