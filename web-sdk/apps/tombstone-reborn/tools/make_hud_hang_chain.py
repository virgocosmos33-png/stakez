"""Key the generated hanging-chain sheet (black pad) to a transparent sprite.

Run:  python tools/make_hud_hang_chain.py
"""

from __future__ import annotations

import os
import shutil

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW = os.path.join(APP, "assets-raw", "hud_wood", "tr_hud_hang_chain.png")
GEN = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
        "tr_hud_hang_chain.png",
    )
)
REL = os.path.join("sprites", "tombstone", "hud_hang_chain.png")


def main() -> None:
    src = RAW if os.path.isfile(RAW) else GEN
    if not os.path.isfile(src):
        raise SystemExit(f"missing chain sheet: {src}")
    os.makedirs(os.path.dirname(RAW), exist_ok=True)
    if src != RAW:
        shutil.copy2(src, RAW)

    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    lum = rgb.mean(axis=2)
    alpha = np.clip((lum - 10.0) / 22.0, 0.0, 1.0)
    rgba = np.dstack([rgb, alpha * 255.0]).astype(np.uint8)
    img = Image.fromarray(rgba, "RGBA")
    box = img.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    if box:
        pad = 8
        img = img.crop(
            (
                max(0, box[0] - pad),
                max(0, box[1] - pad),
                min(img.width, box[2] + pad),
                min(img.height, box[3] + pad),
            )
        )

    for base in ("assets-src", os.path.join("static", "assets")):
        path = os.path.join(APP, base, REL)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path, optimize=True)
        print(f"wrote {path} {img.size}")


if __name__ == "__main__":
    main()
