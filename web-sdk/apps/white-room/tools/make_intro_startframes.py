"""Compose the image-to-video START FRAMES for the 'enter the mirror' intro.

Crops the Madam Mirror loading painting around the ornate oval mirror (where
Madam Mirror herself sits behind the cracked violet glass) so the mirror is the
dominant subject the camera will dive into. Adds a faint violet portal bloom on
the glass to hint the mirror is a doorway. Landscape (16:9) + portrait (9:16).

Output: qa-shots/intro/intro_start_land.png + intro_start_port.png
Run:    python tools/make_intro_startframes.py
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "mirror"))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "qa-shots", "intro"))
os.makedirs(OUT, exist_ok=True)

SRC = os.path.join(MIRROR, "loading.webp")  # 1536x1024

# mirror-oval centre in the loading painting (normalised)
CX, CY = 0.66, 0.48


def crop_ratio(img: Image.Image, ratio: float, cx: float, cy: float) -> Image.Image:
    """Crop the widest window of aspect `ratio` (w/h) centred on (cx,cy)."""
    w, h = img.size
    # try full height first
    cw, ch = int(h * ratio), h
    if cw > w:
        cw, ch = w, int(w / ratio)
    px, py = cx * w, cy * h
    x0 = int(min(max(px - cw / 2, 0), w - cw))
    y0 = int(min(max(py - ch / 2, 0), h - ch))
    return img.crop((x0, y0, x0 + cw, y0 + ch))


def add_portal_bloom(img: Image.Image, cx: float, cy: float, strength: float) -> Image.Image:
    """Soft violet radial bloom centred on the mirror glass."""
    w, h = img.size
    ys, xs = np.mgrid[0:h, 0:w]
    nx = (xs - cx * w) / (w * 0.32)
    ny = (ys - cy * h) / (h * 0.32)
    d = np.sqrt(nx**2 + ny**2)
    bloom = np.clip(1.0 - d, 0, 1) ** 2.2
    base = np.asarray(img.convert("RGB"), np.float32)
    violet = np.array([150, 92, 235], np.float32)
    out = base + bloom[..., None] * violet * strength
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def build(ratio: float, size: tuple[int, int], name: str) -> None:
    img = Image.open(SRC).convert("RGB")
    crop = crop_ratio(img, ratio, CX, CY)
    crop = crop.resize(size, Image.LANCZOS)
    # where is the mirror centre inside the crop? (roughly centre for both)
    crop = add_portal_bloom(crop, 0.5, 0.46, strength=0.28)
    # gentle vignette to draw the eye inward
    w, h = size
    ys, xs = np.mgrid[0:h, 0:w]
    nx, ny = (xs / w - 0.5) * 2, (ys / h - 0.5) * 2
    vig = np.clip(np.sqrt(nx**2 + ny**2) / 1.414, 0, 1) ** 2.0
    arr = np.asarray(crop, np.float32) * (1 - vig[..., None] * 0.35)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(os.path.join(OUT, name))
    print("wrote", os.path.join(OUT, name), size)


if __name__ == "__main__":
    build(16 / 9, (1280, 720), "intro_start_land.png")
    build(9 / 16, (720, 1280), "intro_start_port.png")
    print("done")
