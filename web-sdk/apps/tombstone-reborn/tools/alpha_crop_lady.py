"""Alpha-crop THE WHITE ROOM host masters → transparent cutouts + part PNGs.

Pipeline step 2 (after gen_lady_character.py):
  1. Load masters from assets-raw/lady_masters/ (or scene fallbacks)
  2. Key magenta (#FF00FF) OR flood-fill near-black/near-white border BG
  3. Fill enclosed alpha holes + inpaint RGB so lap/sleeve gaps are solid
  4. Mirror so she faces the reels (LEFT)
  5. Trim + write:
       static/assets/sprites/scene/lady_character.png
       static/assets/sprites/scene/lady_bonus.png
       static/assets/sprites/scene/lady_parts/{base,bonus}/*.png

Part boxes match gen_lady_spine.py asylum host cut layout (NOT Victorian
veil/skirt). Run:  python tools/alpha_crop_lady.py
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "lady_masters"
SCENE = APP / "static" / "assets" / "sprites" / "scene"
PARTS = SCENE / "lady_parts"
SCENE.mkdir(parents=True, exist_ok=True)
PARTS.mkdir(parents=True, exist_ok=True)

MAGENTA = np.array([255, 0, 255], dtype=np.int16)

# Fractions of trimmed figure bbox — must stay in sync with gen_lady_spine.py
BASE_PARTS = [
    ("chair", (0.18, 0.28, 0.82, 0.95)),
    ("gownLower", (0.10, 0.55, 0.90, 1.00)),
    ("torso", (0.22, 0.18, 0.78, 0.62)),
    ("straps", (0.20, 0.32, 0.80, 0.58)),
    ("arms", (0.28, 0.38, 0.72, 0.68)),
    ("hair", (0.18, 0.00, 0.82, 0.45)),
    ("head", (0.28, 0.00, 0.72, 0.28)),
]
BONUS_PARTS = [
    ("chair", (0.16, 0.26, 0.84, 0.96)),
    ("gownLower", (0.10, 0.52, 0.90, 1.00)),
    ("torso", (0.22, 0.16, 0.78, 0.60)),
    ("straps", (0.20, 0.30, 0.80, 0.56)),
    ("arms", (0.28, 0.36, 0.72, 0.66)),
    ("hair", (0.16, 0.00, 0.84, 0.48)),
    ("head", (0.28, 0.00, 0.72, 0.28)),
]

VARIANTS = {
    "base": {
        "masters": [
            RAW / "white_room_character_base.png",
            SCENE / "lady_character.png",
        ],
        "out": "lady_character.png",
        "parts": BASE_PARTS,
        "tag": "base",
    },
    "bonus": {
        "masters": [
            RAW / "white_room_character_bonus.png",
            SCENE / "lady_bonus.png",
        ],
        "out": "lady_bonus.png",
        "parts": BONUS_PARTS,
        "tag": "bonus",
    },
}


def robust_write_png(path: Path, im: Image.Image, attempts: int = 8) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    for i in range(attempts):
        try:
            im.save(tmp, "PNG", optimize=True)
            os.replace(tmp, path)
            return
        except OSError:
            time.sleep(0.6 * (i + 1))
    raise SystemExit(f"could not write {path}")


def _magenta_frac(rgb: np.ndarray) -> float:
    d = np.abs(rgb.astype(np.int16) - MAGENTA).sum(axis=2)
    return float((d < 90).mean())


def key_background(rgb: np.ndarray, alpha_in: np.ndarray | None) -> np.ndarray:
    """Return uint8 alpha (0=BG, 255=figure). Prefers magenta key when present."""
    h, w = rgb.shape[:2]
    if _magenta_frac(rgb) > 0.08:
        dist = np.abs(rgb.astype(np.int16) - MAGENTA).sum(axis=2)
        alpha = np.where(dist < 110, 0, 255).astype(np.uint8)
        # soft fringe: near-magenta → partial
        soft = (dist >= 110) & (dist < 180)
        alpha = alpha.astype(np.float32)
        alpha[soft] = np.clip((dist[soft] - 110) / 70.0, 0, 1) * 255
        alpha = alpha.astype(np.uint8)
        print("  key=magenta", flush=True)
    else:
        # Border flood-fill on near-black OR near-white BG; preserve pale gown.
        border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
        dark = float(border.mean()) < 80
        if alpha_in is not None and (alpha_in < 16).mean() > 0.15:
            seed_bg = (alpha_in < 16) | (rgb.max(axis=2) < 22)
            mode = "alpha+dark" if dark else "alpha+light"
        elif dark:
            seed_bg = rgb.max(axis=2) < 28
            mode = "dark"
        else:
            seed_bg = rgb.min(axis=2) > 210
            mode = "light"
        work = rgb.copy()
        ff_mask = np.zeros((h + 2, w + 2), np.uint8)
        tol = 28 if dark else 22
        flags = 8 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
        step = 12
        seeds = (
            [(x, 0) for x in range(0, w, step)]
            + [(x, h - 1) for x in range(0, w, step)]
            + [(0, y) for y in range(0, h, step)]
            + [(w - 1, y) for y in range(0, h, step)]
        )
        for sx, sy in seeds:
            if ff_mask[sy + 1, sx + 1] != 0:
                continue
            if not seed_bg[sy, sx]:
                continue
            cv2.floodFill(work, ff_mask, (sx, sy), 0, (tol, tol, tol), (tol, tol, tol), flags)
        bg = ff_mask[1:-1, 1:-1].astype(bool)
        alpha = np.where(bg, 0, 255).astype(np.uint8)
        print(f"  key=flood({mode})", flush=True)

    # Close pinholes, open speckles
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, k)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, k)
    return alpha


def fill_enclosed_holes(rgb: np.ndarray, alpha: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Fill enclosed transparent/black voids inside the figure; inpaint RGB."""
    h, w = alpha.shape
    # exterior = low-alpha connected to image border
    ff = (alpha < 128).astype(np.uint8) * 255
    for sx, sy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if ff[sy, sx] == 0:
            continue
        m = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(ff, m, (sx, sy), 128)
    exterior = ff == 128

    # Transparent pockets not reachable from border
    alpha_holes = (alpha < 128) & (~exterior)
    # Opaque-but-black voids inside pale fabric (NOT black hair).
    # Keep a component only if it is sizable AND its ring of neighbors is bright
    # (straitjacket / gown), so matted hair is left alone.
    black_void = (alpha >= 128) & (~exterior) & (rgb.max(axis=2) < 28)
    void_u8 = black_void.astype(np.uint8) * 255
    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(void_u8, 8)
    keep_void = np.zeros_like(black_void)
    lum = rgb.mean(axis=2)
    for i in range(1, n_labels):
        area = int(stats[i, cv2.CC_STAT_AREA])
        if area < 120:
            continue
        comp = labels == i
        ring = cv2.dilate(comp.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool) & (~comp) & (~exterior)
        if ring.sum() < 20:
            continue
        if float(lum[ring].mean()) < 90:
            continue  # dark neighbors → hair / shadow, skip
        keep_void |= comp
    holes = alpha_holes | keep_void
    n = int(holes.sum())
    if n == 0:
        print("  holes=0", flush=True)
        return rgb, alpha
    print(f"  holes={n} px (alpha={int(alpha_holes.sum())} black={int(keep_void.sum())}) — inpainting", flush=True)
    new_alpha = alpha.copy()
    new_alpha[holes] = 255
    new_alpha[exterior] = 0
    mask = holes.astype(np.uint8) * 255
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    # Don't inpaint into true exterior
    mask[exterior] = 0
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    fixed = cv2.inpaint(bgr, mask, 8, cv2.INPAINT_TELEA)
    out_rgb = cv2.cvtColor(fixed, cv2.COLOR_BGR2RGB)
    return out_rgb, new_alpha


def refine_matte(alpha: np.ndarray) -> np.ndarray:
    alpha = cv2.erode(alpha, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    alpha = cv2.GaussianBlur(alpha, (0, 0), 1.0)
    return alpha


def process_variant(key: str, cfg: dict) -> Path:
    src_path = next((p for p in cfg["masters"] if p.is_file()), None)
    if src_path is None:
        raise SystemExit(f"[{key}] no master found in {cfg['masters']}")
    print(f"[{key}] src={src_path}", flush=True)
    src = Image.open(src_path).convert("RGBA")
    arr = np.asarray(src)
    rgb, a_in = arr[:, :, :3].copy(), arr[:, :, 3].copy()
    alpha = key_background(rgb, a_in)
    rgb, alpha = fill_enclosed_holes(rgb, alpha)
    alpha = refine_matte(alpha)
    out = np.dstack([rgb, alpha])
    im = Image.fromarray(out, "RGBA")
    # Face the reels (LEFT). Only flip Scenario masters from assets-raw —
    # scene cutouts are already oriented for the board.
    from_raw = RAW in src_path.parents or src_path.parent == RAW
    if from_raw:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        print("  flipped raw master → faces LEFT", flush=True)
    else:
        print("  keep orientation (scene cutout)", flush=True)
    bbox = im.getbbox()
    if bbox:
        pad = 8
        w, h = im.size
        bbox = (
            max(bbox[0] - pad, 0),
            max(bbox[1] - pad, 0),
            min(bbox[2] + pad, w),
            min(bbox[3] + pad, h),
        )
        im = im.crop(bbox)
    dest = SCENE / cfg["out"]
    robust_write_png(dest, im)
    opaque = (np.asarray(im)[:, :, 3] > 128).mean() * 100
    print(f"[{key}] wrote {dest.name} {im.size} opaque={opaque:.1f}%", flush=True)

    # QA on magenta
    qa = Image.new("RGBA", im.size, (255, 0, 255, 255))
    qa.alpha_composite(im)
    robust_write_png(SCENE / f"_qa_{cfg['tag']}_on_magenta.png", qa.convert("RGB").convert("RGBA"))

    # Part separation — transparent PNGs for atlas build / QA
    part_dir = PARTS / cfg["tag"]
    part_dir.mkdir(parents=True, exist_ok=True)
    fig = np.asarray(im)
    Ht, Wt = fig.shape[:2]
    for name, (bx0, by0, bx1, by1) in cfg["parts"]:
        box = (int(bx0 * Wt), int(by0 * Ht), int(bx1 * Wt), int(by1 * Ht))
        tile = im.crop(box)
        sub = tile.split()[3].getbbox()
        if sub is None:
            print(f"  part {name}: EMPTY", flush=True)
            continue
        tile = tile.crop(sub)
        robust_write_png(part_dir / f"{name}.png", tile)
        print(f"  part {name}: {tile.size}", flush=True)
    return dest


def main() -> None:
    for key, cfg in VARIANTS.items():
        process_variant(key, cfg)
    print("done.", flush=True)


if __name__ == "__main__":
    main()
