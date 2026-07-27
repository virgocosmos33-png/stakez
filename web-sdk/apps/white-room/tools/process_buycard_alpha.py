"""Remove the baked OUTER-BLACK background from the buy-bonus card art, leaving a
clean transparent PNG/WebP while preserving the (very dark) interior artwork.

Method per card (border-connected flood-fill with an art-protect guard):
  1. L = per-pixel max-channel luminance.
  2. cand    = (L <= T_LO) that is connected to the image border  -> outer black.
  3. protect = dilate(L >= T_HI, R)  -> a guard halo around genuine bright art so
     the dark portions of flames/smoke/frames adjacent to bright art are NOT eaten.
  4. bg = cand & ~protect, then binary_opening to snap thin speckle tendrils, then
     re-keep only the border-connected part (drops isolated interior specks).
  5. alpha = 0 on bg else 255; feather ~1px (Gaussian) to anti-alias the cut.
This removes ONLY black connected to the border; interior dark art stays opaque.

Usage:
  python tools/process_buycard_alpha.py --stage    # write previews to _stage, no overwrite
  python tools/process_buycard_alpha.py --apply     # back up *_orig + overwrite in place
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

DIR = Path("static/assets/sprites/mirror")
STAGE = Path("tools/_buycard_stage")

CARDS = [
    "buy_ante.webp", "buy_feature1.webp", "buy_feature2.webp",
    "buy_feature3.webp", "buy_seance.webp", "buy_otherside.webp",
    "buy_bloodmoon.webp",
]

# Tuned params. Menu bg is dark (#10161d) so a faint dark rim is invisible; we
# bias toward preserving art (larger protect radius) over squeezing every pixel.
T_LO = 18     # <= this max-channel value counts as removable black
T_HI = 72     # >= this seeds the art-protect guard
R = 7         # protect dilation radius (px)
OPEN_IT = 2   # binary opening iterations to kill thin speckle tendrils
FEATHER = 1.0 # gaussian sigma for alpha anti-alias

CROSS = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)


def border_connected(mask: np.ndarray) -> np.ndarray:
    lbl, _ = ndimage.label(mask, structure=CROSS)
    bl = set(lbl[0, :]) | set(lbl[-1, :]) | set(lbl[:, 0]) | set(lbl[:, -1])
    bl.discard(0)
    return np.isin(lbl, list(bl))


def key_outer_black(im: Image.Image) -> Image.Image:
    arr = np.asarray(im.convert("RGBA"))
    rgb = arr[..., :3].astype(np.int32)
    L = rgb.max(axis=2)

    cand = border_connected(L <= T_LO)
    protect = ndimage.binary_dilation(L >= T_HI, iterations=R)
    bg = cand & ~protect
    if OPEN_IT:
        bg = ndimage.binary_opening(bg, structure=CROSS, iterations=OPEN_IT)
    bg = border_connected(bg)

    alpha = np.where(bg, 0, 255).astype(np.uint8)
    a_im = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(FEATHER))
    out = arr.copy()
    out[..., 3] = np.asarray(a_im)
    return Image.fromarray(out, "RGBA")


def bbox_of(im: Image.Image):
    return im.split()[3].getbbox()


def comp(im: Image.Image, bg_color) -> Image.Image:
    base = Image.new("RGBA", im.size, bg_color + (255,))
    base.alpha_composite(im)
    return base.convert("RGB")


def contact_sheet(results, bg_color, cols=4, cell=380, pad=16):
    n = len(results)
    rows = (n + cols - 1) // cols
    W = cols * cell + pad * (cols + 1)
    H = rows * cell + pad * (rows + 1)
    sheet = Image.new("RGB", (W, H), bg_color)
    for i, (name, im) in enumerate(results):
        r, c = divmod(i, cols)
        thumb = im.copy()
        thumb.thumbnail((cell, cell), Image.LANCZOS)
        cx = pad + c * (cell + pad) + (cell - thumb.width) // 2
        cy = pad + r * (cell + pad) + (cell - thumb.height) // 2
        tile = Image.new("RGBA", (thumb.width, thumb.height), bg_color + (255,))
        tile.alpha_composite(thumb)
        sheet.paste(tile.convert("RGB"), (cx, cy))
    return sheet


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="overwrite in place (with _orig backup)")
    args = ap.parse_args()

    STAGE.mkdir(parents=True, exist_ok=True)
    results = []
    for name in CARDS:
        src = DIR / name
        orig = DIR / (src.stem + "_orig" + src.suffix)
        # Re-key from the pristine backup when present so re-runs are idempotent.
        source = orig if orig.exists() else src
        if not source.exists():
            print(f"[MISS] {name}")
            continue
        im = Image.open(source)
        keyed = key_outer_black(im)
        bb = bbox_of(keyed)
        tr = (np.asarray(keyed)[..., 3] == 0).mean()
        print(f"{name:20s} size={keyed.size} bbox={bb} transp={tr:5.1%} src={source.name}")
        results.append((name, keyed))

        if args.apply:
            if not orig.exists():
                shutil.copy2(src, orig)
            # High-quality lossy WebP WITH alpha: keeps file weight close to the
            # originals (which were lossy) while staying visually lossless.
            keyed.save(src, "WEBP", quality=92, method=6, exact=True)
            print(f"  applied -> {src}  ({src.stat().st_size//1024} KB, backup {orig.name})")
        else:
            keyed.save(STAGE / (src.stem + ".png"))

    # contact sheets over the actual menu dark bg and a light bg
    menu = contact_sheet(results, (16, 22, 29))   # #10161d
    light = contact_sheet(results, (225, 225, 230))
    menu.save(STAGE / "_sheet_menu.png")
    light.save(STAGE / "_sheet_light.png")
    print(f"\nsheets -> {STAGE/'_sheet_menu.png'} , {STAGE/'_sheet_light.png'}")


if __name__ == "__main__":
    main()
