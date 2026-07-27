"""Restore White Room host from a known Scenario cutout (not GodMode).

Downloads asset_uAf7XA89QjaNCkUVrKT81Tm3 (seated Patient, white BG),
corner-floods only near-pure-white background, mirrors to face LEFT,
writes masters + scene stills + parts, then caller runs gen_lady_spine.py.
"""

from __future__ import annotations

import os
import time
import urllib.request
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

APP = Path(__file__).resolve().parents[1]
MASTERS = APP / "assets-raw" / "lady_masters"
SCENE = APP / "static" / "assets" / "sprites" / "scene"
PARTS = SCENE / "lady_parts"
ASSET_ID = "asset_uAf7XA89QjaNCkUVrKT81Tm3"

# Fractions match gen_lady_spine / alpha_crop_lady asylum layout
BASE_PARTS = [
    ("chair", (0.18, 0.28, 0.82, 0.95)),
    ("gownLower", (0.10, 0.55, 0.90, 1.00)),
    ("torso", (0.22, 0.18, 0.78, 0.62)),
    ("straps", (0.20, 0.32, 0.80, 0.58)),
    ("arms", (0.28, 0.38, 0.72, 0.68)),
    ("hair", (0.18, 0.00, 0.82, 0.45)),
    ("head", (0.28, 0.00, 0.72, 0.28)),
]


def robust_write_png(path: Path, im: Image.Image, attempts: int = 8) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    for i in range(attempts):
        try:
            im.save(tmp, "PNG", optimize=True)
            os.replace(tmp, path)
            return
        except OSError:
            time.sleep(0.6 * (i + 1))
    raise SystemExit(f"could not write {path}")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    print(f"[dl] {dest.name} {dest.stat().st_size}", flush=True)


def corner_flood_alpha(rgb: np.ndarray, thr: int = 248, tol: int = 12) -> np.ndarray:
    """Alpha=0 only for near-white pixels reachable from image borders."""
    h, w = rgb.shape[:2]
    is_bg = (
        (rgb[:, :, 0] >= thr)
        & (rgb[:, :, 1] >= thr)
        & (rgb[:, :, 2] >= thr)
        & ((rgb.max(axis=2) - rgb.min(axis=2)) <= tol)
    )
    mask = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_bg[y, x] and not mask[y, x]:
                mask[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg[y, x] and not mask[y, x]:
                mask[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and not mask[ny, nx] and is_bg[ny, nx]:
                mask[ny, nx] = True
                q.append((ny, nx))
    alpha = np.where(mask, 0, 255).astype(np.uint8)
    return alpha


def trim_rgba(im: Image.Image) -> Image.Image:
    bbox = im.getbbox()
    return im.crop(bbox) if bbox else im


def slice_parts(fig: Image.Image, tag: str) -> None:
    out = PARTS / tag
    out.mkdir(parents=True, exist_ok=True)
    w, h = fig.size
    for name, (x0, y0, x1, y1) in BASE_PARTS:
        box = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        part = fig.crop(box)
        # keep only opaque pixels from parent
        robust_write_png(out / f"{name}.png", part)


def main() -> None:
    import json
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    # Prefer URL from CLI / env; else require ASSET_URL
    url = (os.environ.get("LADY_RESTORE_URL") or "").strip()
    if not url:
        # Fallback: read last URL file if present
        url_file = MASTERS / "last_download_url.txt"
        if url_file.is_file():
            url = url_file.read_text(encoding="utf-8").strip()
    if not url:
        raise SystemExit(
            "Set LADY_RESTORE_URL to the Scenario CDN png URL for "
            f"{ASSET_ID} (from asset_download)."
        )

    MASTERS.mkdir(parents=True, exist_ok=True)
    (MASTERS / "last_download_url.txt").write_text(url, encoding="utf-8")
    raw_path = MASTERS / "white_room_character_base_raw.png"
    download(url, raw_path)

    im = Image.open(raw_path).convert("RGBA")
    rgb = np.asarray(im)[:, :, :3].copy()
    alpha = corner_flood_alpha(rgb)
    cut = np.dstack([rgb, alpha])
    cut_im = Image.fromarray(cut, "RGBA")
    # Face LEFT toward reels
    cut_im = cut_im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    cut_im = trim_rgba(cut_im)

    # Magenta master for pipeline visibility (alpha already correct)
    master = cut_im.copy()
    arr = np.asarray(master).copy()
    arr[arr[:, :, 3] == 0, :3] = (255, 0, 255)
    arr[arr[:, :, 3] == 0, 3] = 255
    master_m = Image.fromarray(arr, "RGBA")
    robust_write_png(MASTERS / "white_room_character_base.png", master_m)
    robust_write_png(MASTERS / "white_room_character_bonus.png", master_m)

    robust_write_png(SCENE / "lady_character.png", cut_im)
    robust_write_png(SCENE / "lady_bonus.png", cut_im)
    slice_parts(cut_im, "base")
    slice_parts(cut_im, "bonus")

    qa = Image.new("RGBA", cut_im.size, (255, 0, 255, 255))
    qa.alpha_composite(cut_im)
    robust_write_png(SCENE / "_qa_base_on_magenta.png", qa)

    meta = {
        "sourceAssetId": ASSET_ID,
        "note": "Restored seated Patient cutout; GodMode sequence quarantined.",
        "size": list(cut_im.size),
    }
    (MASTERS / "restore_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"[ok] lady_character.png {cut_im.size} bg_kill={float((alpha == 0).mean()):.3f}", flush=True)


if __name__ == "__main__":
    main()
