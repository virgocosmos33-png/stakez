# STRETCH chains — key the magenta-background sources into transparent PNGs:
#   chain_tile.png  vertical chain strip (cropped horizontally only, so it
#                   still tiles top-to-bottom)
#   clamp.png       the two-jaw grabber that grips the reel edge
# Usage: python make_stretch_chain.py <chain_src> <clamp_src>
import sys
from pathlib import Path

import numpy as np
from PIL import Image

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "sprites" / "stretch"


def key_magenta(img: Image.Image) -> Image.Image:
    """Magenta (#FF00FF) -> alpha, with despill so edges don't glow pink."""
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    # how magenta a pixel is: both R and B far above G
    mag = np.minimum(r, b) - g
    alpha = np.clip((60.0 - mag) / 60.0, 0.0, 1.0)
    alpha = np.where(mag < 0, 1.0, alpha)
    # despill: pull R/B down toward G where magenta bleeds into kept pixels
    spill = np.clip(np.minimum(r, b) - g, 0, None) * (alpha < 1.0)
    out = rgb.copy()
    out[..., 0] = np.clip(r - spill * 0.7, 0, 255)
    out[..., 2] = np.clip(b - spill * 0.7, 0, 255)
    rgba = np.dstack([out, alpha * 255.0]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def content_box(img: Image.Image, thresh: int = 8):
    a = np.asarray(img)[..., 3]
    ys, xs = np.nonzero(a > thresh)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def main() -> None:
    chain_src, clamp_src = sys.argv[1], sys.argv[2]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    chain = key_magenta(Image.open(chain_src))
    x0, _, x1, _ = content_box(chain)
    pad = 6
    chain = chain.crop((max(0, x0 - pad), 0, min(chain.width, x1 + pad), chain.height))
    chain.save(OUT_DIR / "chain_tile.png")

    clamp = key_magenta(Image.open(clamp_src))
    x0, y0, x1, y1 = content_box(clamp)
    pad = 8
    clamp = clamp.crop(
        (max(0, x0 - pad), max(0, y0 - pad), min(clamp.width, x1 + pad), min(clamp.height, y1 + pad))
    )
    clamp.save(OUT_DIR / "clamp.png")

    for name in ("chain_tile.png", "clamp.png"):
        img = Image.open(OUT_DIR / name)
        print(name, img.size)


if __name__ == "__main__":
    main()
