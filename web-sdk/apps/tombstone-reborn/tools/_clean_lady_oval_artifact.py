"""Remove Patient 'magnifying glass' oval + harden matte for idle rebuild.

Root cause:
  - Idle webm chromakey leaves a soft detached oval near lap/chair (visible
    mid-loop, e.g. t≈0.25) — warp + soft fringe + blue key garbage.
  - Stills may carry a faint greasy smear on the gown from prior hole-fill.

This script:
  1. Backs up masters
  2. Inpaints faint gown smear (left lap)
  3. Hardens alpha (kill soft fringe that becomes floating ovals after key)
  4. Despills purple edge
  5. Writes static/ + assets/ lady_character.png + lady_bonus.png

Then run:  python tools/_local_lady_idle_from_png.py
           python tools/_post_lady_idle_alpha.py
"""
from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

APP = Path(__file__).resolve().parents[1]
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
QA = APP / "assets-raw" / "lady_video" / "_qa"
QA.mkdir(parents=True, exist_ok=True)

TARGETS = ("lady_character.png", "lady_bonus.png")


def robust_write_png(path: Path, im: Image.Image, attempts: int = 8) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    for i in range(attempts):
        try:
            im.save(tmp, "PNG", optimize=True)
            os.replace(tmp, path)
            return
        except OSError:
            time.sleep(0.5 * (i + 1))
    raise SystemExit(f"could not write {path}")


def harden_alpha(alpha: np.ndarray) -> np.ndarray:
    """Binary-ish matte: kill soft fringe that becomes floating ovals after key."""
    a = alpha.astype(np.float32)
    # Crush mid-alpha fringe to 0 or 255
    hard = np.where(a >= 140, 255, 0).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    hard = cv2.morphologyEx(hard, cv2.MORPH_OPEN, k)
    hard = cv2.morphologyEx(hard, cv2.MORPH_CLOSE, k)
    # Tiny edge soften (1px) so hair isn't jaggy, but no big soft halo
    soft = cv2.GaussianBlur(hard, (0, 0), 0.6)
    return soft


def despill(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    out = rgb.astype(np.float32)
    a = alpha.astype(np.float32) / 255.0
    edge = (a > 0.08) & (a < 0.95)
    solid = (alpha > 200).astype(np.uint8)
    ring = cv2.dilate(solid, np.ones((3, 3), np.uint8)).astype(bool) & (~solid.astype(bool))
    band = edge | ring
    r, g, b = out[:, :, 0], out[:, :, 1], out[:, :, 2]
    magenta = band & (r > g + 10) & (b > g + 6)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    out[magenta, 0] = np.minimum(r[magenta], lum[magenta] * 0.96)
    out[magenta, 2] = np.minimum(b[magenta], lum[magenta] * 0.92)
    # near-black fringe outside figure → leave for alpha
    return np.clip(out, 0, 255).astype(np.uint8)


def inpaint_gown_smear(bgr: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Remove faint greasy vertical smear on left gown / lap."""
    h, w = alpha.shape
    mask = np.zeros((h, w), np.uint8)
    # Primary soft oval on gown (viewer-left lap)
    cv2.ellipse(mask, (300, 795), (42, 72), -10, 0, 360, 255, -1)
    # Secondary near chair seat / hip (viewer-right) if greasy
    cv2.ellipse(mask, (455, 720), (28, 40), 15, 0, 360, 255, -1)
    mask = cv2.GaussianBlur(mask, (0, 0), 5)
    mask = np.where(mask > 35, 255, 0).astype(np.uint8)
    mask[alpha < 160] = 0
    if mask.sum() == 0:
        return bgr
    fixed = cv2.inpaint(bgr, mask, 11, cv2.INPAINT_TELEA)
    fixed = cv2.inpaint(fixed, mask, 7, cv2.INPAINT_NS)
    return fixed


def clean_one(src: Path) -> Image.Image:
    # Prefer bak if present so re-runs are idempotent from original
    bak = src.with_suffix(src.suffix + ".pre_oval_clean.bak")
    load = bak if bak.is_file() else src
    im = Image.open(load).convert("RGBA")
    arr = np.array(im)
    rgb, alpha = arr[:, :, :3].copy(), arr[:, :, 3].copy()
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    bgr = inpaint_gown_smear(bgr, alpha)
    out_rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    alpha2 = harden_alpha(alpha)
    out_rgb = despill(out_rgb, alpha2)
    # zero RGB where fully transparent
    out_rgb[alpha2 < 8] = 0
    return Image.fromarray(np.dstack([out_rgb, alpha2]), "RGBA")


def main() -> None:
    for name in TARGETS:
        src = STATIC / name
        if not src.is_file():
            src = VITE / name
        bak = src.with_suffix(src.suffix + ".pre_oval_clean.bak")
        if not bak.is_file() and src.is_file():
            shutil.copy2(src, bak)
            print(f"[bak] {bak.name}", flush=True)
        cleaned = clean_one(src)
        for dest_dir in (STATIC, VITE):
            dest_dir.mkdir(parents=True, exist_ok=True)
            robust_write_png(dest_dir / name, cleaned)
            print(f"[ok] {dest_dir.name}/{name}", flush=True)
        cleaned.crop((200, 650, 520, 980)).save(QA / f"{Path(name).stem}_clean_crop.png")
        # alpha proof on white
        white = Image.new("RGBA", cleaned.size, (245, 245, 240, 255))
        white.alpha_composite(cleaned)
        white.save(QA / f"{Path(name).stem}_on_white.png")
    print("[done] stills cleaned + matte hardened", flush=True)


if __name__ == "__main__":
    main()
