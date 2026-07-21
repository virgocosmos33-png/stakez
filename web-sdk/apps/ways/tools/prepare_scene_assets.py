"""Prepare the Lady-Mirror scene background + character stills for the game.

Source stills (generated earlier) live in the Cursor project assets folder; this
copies/optimises them into the game's static asset tree:

  static/assets/sprites/scene/scene_bg.webp   <- full-scene ambient background
  static/assets/sprites/scene/scene_bg.png    <- PNG poster / video source
  static/assets/sprites/scene/lady_character.png <- trimmed transparent cutout

Run from web-sdk/apps/ways:  python tools/prepare_scene_assets.py
"""
from __future__ import annotations

import os
import cv2
import numpy as np
from PIL import Image, ImageFilter

PROJECT_ASSETS = (
    r"C:\Users\xheih\.cursor\projects"
    r"\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios\assets"
)
SRC_BG = os.path.join(PROJECT_ASSETS, "mirror_bg_scene.png")
SRC_CHAR = os.path.join(PROJECT_ASSETS, "mirror_lady_character.png")
SRC_CHAR_BONUS = os.path.join(PROJECT_ASSETS, "mirror_lady_bonus.png")

OUT_DIR = os.path.join("static", "assets", "sprites", "scene")
os.makedirs(OUT_DIR, exist_ok=True)


def prep_background() -> None:
    im = Image.open(SRC_BG).convert("RGB")
    print(f"[bg] source size = {im.size}  ratio = {im.size[0] / im.size[1]:.3f}")
    # PNG poster (kept as the i2v source + potential <video> poster)
    im.save(os.path.join(OUT_DIR, "scene_bg.png"), optimize=True)
    # web-friendly still used by the Pixi sprite fallback
    im.save(os.path.join(OUT_DIR, "scene_bg.webp"), quality=90, method=6)
    print(f"[bg] wrote scene_bg.png + scene_bg.webp -> {OUT_DIR}")


def prep_character(src_path: str, out_name: str, tag: str) -> None:
    """The 'transparent cutout' is actually RGB on a near-white background.
    Key out ONLY the border-connected white (flood fill) so light interior
    pixels (pale face, veil highlights, the glowing mirror) are preserved, then
    feather + defringe. Also mirrors the PNG so she FACES the reels (faces left).
    """
    src = Image.open(src_path).convert("RGB")
    print(f"[{tag}] source size = {src.size}  mode(orig)=RGB (white bg)")
    rgb = np.asarray(src)
    h, w = rgb.shape[:2]

    # flood fill the background from a ring of border seeds. FIXED_RANGE keeps
    # the fill within `tol` of the seed colour (white), so it stops at the gown.
    ff_mask = np.zeros((h + 2, w + 2), np.uint8)
    tol = 22
    flags = 8 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
    work = rgb.copy()
    step = 16
    seeds = (
        [(x, 0) for x in range(0, w, step)]
        + [(x, h - 1) for x in range(0, w, step)]
        + [(0, y) for y in range(0, h, step)]
        + [(w - 1, y) for y in range(0, h, step)]
    )
    for (sx, sy) in seeds:
        if ff_mask[sy + 1, sx + 1] != 0:
            continue  # already flooded
        px = rgb[sy, sx]
        if int(px.min()) < 210:
            continue  # not background here (e.g. veil touches the edge)
        cv2.floodFill(
            work, ff_mask, (sx, sy), 0,
            (tol, tol, tol), (tol, tol, tol), flags,
        )

    bg = ff_mask[1:-1, 1:-1].astype(bool)  # True = background
    alpha = np.where(bg, 0, 255).astype(np.uint8)

    # clean specks / fill pinholes inside the figure
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, k)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, k)
    # pull the matte 1px inside the silhouette to drop the white rim, then feather
    alpha = cv2.erode(alpha, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    alpha = cv2.GaussianBlur(alpha, (0, 0), 1.1)

    out_rgba = np.dstack([rgb, alpha])
    im = Image.fromarray(out_rgba, "RGBA")

    # She stands on the RIGHT of the board and must FACE the reels (i.e. face
    # LEFT). The source cutout faces right/outward, so mirror the PNG itself.
    # Baking the flip into the file (not a negative sprite scale) keeps the
    # component's right-side anchoring math intact, and the video step applies
    # the matching ffmpeg `hflip` so the animated version faces left too.
    im = im.transpose(Image.FLIP_LEFT_RIGHT)

    # trim to visible content (+ small pad)
    bbox = im.getbbox()
    if bbox:
        pad = 6
        bbox = (
            max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
            min(bbox[2] + pad, w), min(bbox[3] + pad, h),
        )
        im = im.crop(bbox)

    out = os.path.join(OUT_DIR, out_name)
    im.save(out, optimize=True)
    cw, ch = im.size
    print(f"[{tag}] cutout size = {cw}x{ch}  aspect(W/H) = {cw / ch:.4f}")
    print(f"[{tag}] opaque coverage = {(np.asarray(im)[:, :, 3] > 128).mean() * 100:.1f}%")

    # QA composite over magenta so any halo/holes are obvious when read back
    qa = Image.new("RGBA", im.size, (255, 0, 255, 255))
    qa.alpha_composite(im)
    qa.convert("RGB").save(os.path.join(OUT_DIR, f"_qa_{tag}_on_magenta.png"))
    print(f"[{tag}] wrote {out} + _qa_{tag}_on_magenta.png")


if __name__ == "__main__":
    prep_background()
    prep_character(SRC_CHAR, "lady_character.png", "char")
    prep_character(SRC_CHAR_BONUS, "lady_bonus.png", "bonus")
    print("done.")
