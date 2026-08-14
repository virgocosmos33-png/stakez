"""Regrade board timber + pocket stone to the saloon wall.

The live staircase (`boardWoodField`) and cell pockets (`boardStoneField`) were
bleached grey for the old desert / clinical rooms. Against the dark amber
saloon they read as white. This keeps the grain and blood, maps luminance onto
the saloon wall, and writes the same filenames the loader already uses.

Run:  python tools/grade_board_to_saloon.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

APP = Path(__file__).resolve().parents[1]
SALOON = APP / "static" / "assets" / "sprites" / "scene" / "scene_bg_v2.webp"
WOOD_NAME = "board_wood_grey.webp"
STONE_NAME = "board_stone_grey.webp"
RAW = APP / "assets-raw" / "board"

TREES = (
	APP / "static" / "assets" / "sprites" / "board",
	APP / "assets-src" / "assets" / "sprites" / "board",
	APP / "assets" / "sprites" / "board",
)


def lum(rgb: np.ndarray) -> np.ndarray:
	return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def wall_tint() -> tuple[np.ndarray, float]:
	saloon = np.asarray(Image.open(SALOON).convert("RGB"), dtype=np.float32)
	h, w = saloon.shape[:2]
	wall = saloon[int(h * 0.18) : int(h * 0.62), int(w * 0.28) : int(w * 0.72)]
	mean = wall.mean(axis=(0, 1))
	l_mean = float(lum(mean.reshape(1, 1, 3))[0, 0])
	return mean, l_mean


def colorize(src: np.ndarray, l_lo: float, l_hi: float, tint: np.ndarray, tint_l: float) -> np.ndarray:
	L = lum(src)
	p5, p95 = np.percentile(L, (5, 95))
	span = max(8.0, float(p95 - p5))
	t = np.clip((L - p5) / span, 0.0, 1.0)
	l_new = l_lo + t * (l_hi - l_lo)
	scale = tint / max(tint_l, 1.0)
	out = l_new[..., None] * scale
	return np.clip(out, 0, 255)


def restore_blood(src: np.ndarray, graded: np.ndarray) -> np.ndarray:
	r, g = src[..., 0], src[..., 1]
	mask = np.clip((r - g - 12.0) / 22.0, 0.0, 1.0)[..., None]
	L01 = np.clip(lum(src) / 180.0, 0.15, 1.0)[..., None]
	blood = np.array([78.0, 16.0, 10.0], dtype=np.float32) * (0.35 + 0.65 * L01)
	return graded * (1.0 - mask) + blood * mask


def write(name: str, image: Image.Image) -> None:
	for tree in TREES:
		tree.mkdir(parents=True, exist_ok=True)
		path = tree / name
		image.save(path, format="WEBP", quality=90, method=6)
		print(f"[saloon-grade] {path.relative_to(APP)} {image.size}")


def main() -> None:
	wood_src = APP / "static" / "assets" / "sprites" / "board" / WOOD_NAME
	stone_src = APP / "static" / "assets" / "sprites" / "board" / STONE_NAME
	if not wood_src.exists() or not stone_src.exists():
		raise SystemExit("missing board_wood_grey.webp or board_stone_grey.webp")

	RAW.mkdir(parents=True, exist_ok=True)
	wood_bak = RAW / "board_wood_grey_pre_saloon.webp"
	stone_bak = RAW / "board_stone_grey_pre_saloon.webp"
	if not wood_bak.exists():
		Image.open(wood_src).save(wood_bak, format="WEBP", quality=92, method=6)
	if not stone_bak.exists():
		Image.open(stone_src).save(stone_bak, format="WEBP", quality=92, method=6)

	tint, tint_l = wall_tint()
	print(f"[saloon-grade] wall tint RGB={tint.round(1)} L={tint_l:.1f}")

	wood = np.asarray(Image.open(wood_bak).convert("RGB"), dtype=np.float32)
	stone = np.asarray(Image.open(stone_bak).convert("RGB"), dtype=np.float32)

	# Timber a touch lighter than the wall so the staircase still has a rim.
	wood_out = restore_blood(wood, colorize(wood, 14.0, 58.0, tint, tint_l))
	# Pocket darker than the rim so cards sit in a recess, not a white slab.
	stone_out = colorize(stone, 8.0, 26.0, tint, tint_l)

	write(WOOD_NAME, Image.fromarray(np.clip(wood_out, 0, 255).astype(np.uint8)))
	write(STONE_NAME, Image.fromarray(np.clip(stone_out, 0, 255).astype(np.uint8)))


if __name__ == "__main__":
	main()
