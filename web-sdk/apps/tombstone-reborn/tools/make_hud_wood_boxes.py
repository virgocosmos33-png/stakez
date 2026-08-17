"""Bake WAYS / MULTI / WIN / FREE SPINS from the SAME wood as the staircase.

Uses tr_frame_planks_v2.png + tr_frame_scraps.png through the frame baker's
own load_plank_bands / load_scrap_pieces / plank_segment. Grey-match to
board_frame.png, then the same grade_small / grade_super the staircase uses
so super boxes get the orange rim on grain. The well is left open
so the plank lips sit on a runtime black plate. The top rail is
omitted — HudReadout draws one labeled pallet there.

Run:  python tools/make_hud_wood_boxes.py
"""

from __future__ import annotations

import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import make_board_frame_image as bf
from grade_board_rip import grade_image

BOARD = os.path.join(APP, "static", "assets", "sprites", "board")
TREES = (
    os.path.join(APP, "assets-src", "sprites", "tombstone"),
    os.path.join(APP, "assets-src", "assets", "sprites", "tombstone"),
    os.path.join(APP, "static", "assets", "sprites", "tombstone"),
)

W, H = 640, 400
WELL = (128, 112, 512, 288)
WELL_PAD = 10
OVER = int(bf.PLANK_OVERHANG * bf.SCALE)

BOXES = (
    ("wood_readout_ways", 1901),
    ("wood_readout_multi", 1907),
    ("wood_readout_win", 1913),
    ("wood_readout_spins", 1919),
)


def _wood_mask(arr: np.ndarray) -> np.ndarray:
    rgb, alpha = arr[..., :3], arr[..., 3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    rust = (r - g > 0.10) & (r > 0.28) & (lum < 0.62)
    paper = (lum > 0.42) & (r > g) & ((r - b) < 0.28)
    blood = (r > g + 0.08) & (r > b + 0.08) & (g < 0.28) & (lum < 0.45)
    return (alpha > 0.35) & (lum > 0.10) & (lum < 0.62) & ~(rust | paper | blood)


def body_mean(im: Image.Image) -> np.ndarray:
    arr = np.asarray(im).astype(np.float32) / 255.0
    lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    mask = _wood_mask(arr)
    if mask.any():
        mask = mask & (lum <= np.percentile(lum[mask], 85))
    if not mask.any():
        mask = arr[..., 3] > 0.35
    return arr[..., :3][mask].mean(axis=0)


def match_frame(wood: Image.Image, frame: Image.Image) -> Image.Image:
    src = body_mean(wood)
    dst = body_mean(frame)
    scale = np.clip(dst / np.maximum(src, 1e-3), 0.35, 2.8)
    arr = np.asarray(wood).astype(np.float32) / 255.0
    mask = _wood_mask(arr)
    arr[..., :3][mask] = np.clip(arr[..., :3][mask] * scale, 0.0, 1.0)
    return Image.fromarray(np.round(arr * 255.0).astype(np.uint8), "RGBA")


def lay(dst: Image.Image, shadow: Image.Image, piece: Image.Image, cx: float, cy: float) -> None:
    px = int(round(cx - piece.width / 2))
    py = int(round(cy - piece.height / 2))
    sh = Image.new("RGBA", piece.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 160), (0, 0), piece.getchannel("A"))
    shadow.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)), (px + 4, py + 5))
    dst.alpha_composite(piece, (px, py))


def bake_wood(planks: list[Image.Image], scraps: list[Image.Image], seed: int) -> Image.Image:
    rng = random.Random(seed)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    l, t, r, b = WELL
    cx, cy = (l + r) / 2, (t + b) / 2
    well_w, well_h = r - l, b - t
    thick = int(bf.PLANK_THICK * bf.SCALE)

    def board(length: int) -> Image.Image:
        h = int(thick * rng.uniform(0.82, 1.12))
        return bf.plank_segment(planks, rng, length + 2 * OVER, h)

    bot = board(well_w).rotate(rng.uniform(-1.6, 1.6), expand=True, resample=Image.BICUBIC)
    left = board(well_h).transpose(Image.ROTATE_90)
    right = board(well_h).transpose(Image.ROTATE_90)
    left = left.rotate(rng.uniform(-1.6, 1.6), expand=True, resample=Image.BICUBIC)
    right = right.rotate(rng.uniform(-1.6, 1.6), expand=True, resample=Image.BICUBIC)
    bot2 = board(int(well_w * 0.62)).rotate(rng.uniform(-2.4, 2.4), expand=True, resample=Image.BICUBIC)

    # No baked top rail — HudReadout draws one labeled pallet there.
    lay(out, shadow, bot, cx + rng.uniform(-6, 6), b + rng.uniform(-4, 4))
    lay(out, shadow, bot2, cx + rng.uniform(-40, 40), b + rng.uniform(-8, 8))
    lay(out, shadow, left, l + rng.uniform(-4, 4), cy + rng.uniform(-6, 6))
    lay(out, shadow, right, r + rng.uniform(-4, 4), cy + rng.uniform(-6, 6))

    order = list(range(len(scraps)))
    rng.shuffle(order)
    for i, (px, py) in enumerate(((l, b), (r, b))):
        scrap = scraps[order[i % len(order)]]
        if rng.random() < 0.5:
            scrap = scrap.transpose(Image.FLIP_LEFT_RIGHT)
        target_w = rng.uniform(64, 104) * bf.SCALE
        f = target_w / scrap.width
        scrap = scrap.resize((int(scrap.width * f), int(scrap.height * f)), Image.LANCZOS)
        scrap = scrap.rotate(rng.uniform(-16, 16), expand=True, resample=Image.BICUBIC)
        lay(out, shadow, scrap, px + rng.uniform(-8, 8), py + rng.uniform(-8, 8))

    return Image.alpha_composite(shadow, out)


def open_well(wood: Image.Image) -> Image.Image:
    """Cut the text well out of the timber so the black plate shows through."""
    hole = Image.new("L", wood.size, 255)
    d = ImageDraw.Draw(hole)
    l, t, r, b = WELL
    d.rounded_rectangle(
        [l + WELL_PAD, t + WELL_PAD, r - WELL_PAD, b - WELL_PAD],
        radius=8,
        fill=0,
    )
    hole = hole.filter(ImageFilter.GaussianBlur(0.6))
    arr = np.asarray(wood).copy()
    arr[..., 3] = (
        arr[..., 3].astype(np.float32) * (np.asarray(hole).astype(np.float32) / 255.0)
    ).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def write_all(stem: str, base: Image.Image, small: Image.Image, super_: Image.Image) -> None:
    names = (f"{stem}.png", f"{stem}_small.png", f"{stem}_super.png")
    images = (base, small, super_)
    for tree in TREES:
        os.makedirs(tree, exist_ok=True)
        for name, im in zip(names, images):
            path = os.path.join(tree, name)
            tmp = path + ".tmp.png"
            im.save(tmp)
            os.replace(tmp, path)
            print(f"wrote {os.path.relpath(path, APP)} {im.size}")


def main() -> None:
    planks = bf.load_plank_bands()
    scraps = bf.load_scrap_pieces()
    print(f"frame wood: planks={len(planks)} scraps={len(scraps)} from {os.path.basename(bf.PLANK_SHEET)}")

    frame = Image.open(os.path.join(BOARD, "board_frame.png")).convert("RGBA")

    l, t, r, b = WELL
    opening = {
        "x0": round((l + WELL_PAD) / W, 4),
        "x1": round((r - WELL_PAD) / W, 4),
        "y0": round((t + WELL_PAD) / H, 4),
        "y1": round((b - WELL_PAD) / H, 4),
    }

    for stem, seed in BOXES:
        wood = match_frame(bake_wood(planks, scraps, seed), frame)
        small, super_ = grade_image(wood)
        write_all(stem, wood, small, super_)

    print(f"opening={opening} aspect={W / H:.3f}")


if __name__ == "__main__":
    main()
