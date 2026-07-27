"""Key + trim the generated counter frames into transparent HUD sprites.

The two counter frames (ways / free-spins) were generated as ornate amethyst
plaques on a PURE BLACK background with an empty dark-glass display window in
the centre. This tool:

  1. flood-fills the black background from the borders -> alpha 0 (the inner
     glass window is fully enclosed by the frame, so it is preserved),
  2. trims to the frame's content bounds,
  3. detects the inner glass window rectangle (the large dark region in the
     centre) and prints it as a fraction of the trimmed image so the Svelte
     counters can place their text exactly inside it,
  4. saves RGBA PNGs into static/assets/sprites/mirror/.

Run:  python tools/process_counter_frames.py
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
# the built-in image generator drops files under the user's ~/.cursor project
# assets folder, not the repo; allow an override via env for portability.
GEN_DIR = Path(
    os.environ.get(
        "COUNTER_FRAME_SRC",
        Path.home()
        / ".cursor"
        / "projects"
        / "c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
        / "assets",
    )
)
OUT_DIR = HERE.parent / "static" / "assets" / "sprites" / "mirror"

JOBS = {
    "ways_frame": "ways_frame_gen.png",
    "fs_frame": "fs_frame_gen.png",
}

BG_THRESH = 60      # flood-fill tolerance for the near-black background
WINDOW_LUMA = 120   # a pixel darker than this (inside the frame) is glass


def key_background(rgb: Image.Image) -> np.ndarray:
    """Return an alpha array (0 = background) by flood-filling the border black."""
    w, h = rgb.size
    work = rgb.copy()
    sentinel = (255, 0, 255)
    seeds = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
        (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2),
    ]
    for seed in seeds:
        ImageDraw.floodfill(work, seed, sentinel, thresh=BG_THRESH)
    arr = np.asarray(work)
    is_bg = np.all(arr == np.array(sentinel), axis=-1)
    alpha = np.where(is_bg, 0, 255).astype(np.uint8)
    return alpha


def detect_window(rgb: np.ndarray, alpha: np.ndarray) -> tuple[float, float, float, float]:
    """Find the central dark glass rectangle; return (cx, cy, w, h) as fractions."""
    h, w, _ = rgb.shape
    luma = rgb[..., :3].max(axis=-1)
    dark = (luma < WINDOW_LUMA) & (alpha > 0)
    cy0, cx0 = h // 2, w // 2

    def span(mask_line: np.ndarray, center: int) -> tuple[int, int]:
        lo = center
        while lo > 0 and mask_line[lo - 1]:
            lo -= 1
        hi = center
        while hi < len(mask_line) - 1 and mask_line[hi + 1]:
            hi += 1
        return lo, hi

    # sample a few rows/cols around centre and take the median span (robust)
    lefts, rights, tops, bots = [], [], [], []
    for dy in (-h // 12, 0, h // 12):
        row = dark[np.clip(cy0 + dy, 0, h - 1)]
        lo, hi = span(row, cx0)
        lefts.append(lo)
        rights.append(hi)
    for dx in (-w // 12, 0, w // 12):
        col = dark[:, np.clip(cx0 + dx, 0, w - 1)]
        lo, hi = span(col, cy0)
        tops.append(lo)
        bots.append(hi)
    left, right = np.median(lefts), np.median(rights)
    top, bot = np.median(tops), np.median(bots)
    cx = (left + right) / 2 / w
    cy = (top + bot) / 2 / h
    ww = (right - left) / w
    hh = (bot - top) / h
    return cx, cy, ww, hh


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, src in JOBS.items():
        path = GEN_DIR / src
        rgb = Image.open(path).convert("RGB")
        alpha = key_background(rgb)
        rgba = np.dstack([np.asarray(rgb), alpha])
        img = Image.fromarray(rgba, "RGBA")

        # trim to opaque content
        bbox = img.getbbox()
        img = img.crop(bbox)
        arr = np.asarray(img)
        cx, cy, ww, hh = detect_window(arr[..., :3], arr[..., 3])

        dest = OUT_DIR / f"{name}.png"
        img.save(dest)
        print(
            f"{name}: {img.width}x{img.height}  window cx={cx:.3f} cy={cy:.3f} "
            f"w={ww:.3f} h={hh:.3f}  -> {dest.name} ({dest.stat().st_size} bytes)",
            flush=True,
        )


if __name__ == "__main__":
    main()
