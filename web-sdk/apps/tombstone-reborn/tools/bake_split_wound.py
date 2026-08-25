"""Bake Kenney split-wound plates (CC0, copy-only haul).

Source: assets-raw/kenney/split-wound/
  splat00-35, slash 01-04, scratch 01, trace 01-07,
  dirt 01-03, scorch 01-03, muzzle 01-05, flash00-08

Outputs wired plates into assets + static + assets-src sprites/fx.
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW = os.path.join(APP, "assets-raw", "kenney", "split-wound")
OUT_DIRS = [
	os.path.join(APP, "assets-src", "sprites", "fx"),
	os.path.join(APP, "static", "assets", "sprites", "fx"),
	os.path.join(APP, "assets", "sprites", "fx"),
]
BLOOD = (138, 16, 22)


def luma_blood(image: Image.Image) -> Image.Image:
	data = np.asarray(image.convert("RGBA")).astype(np.float32)
	luma = data[..., :3].max(axis=2)
	alpha = np.maximum(data[..., 3], luma)
	out = np.zeros_like(data)
	out[..., 0] = BLOOD[0]
	out[..., 1] = BLOOD[1]
	out[..., 2] = BLOOD[2]
	out[..., 3] = alpha
	return Image.fromarray(out.astype(np.uint8), "RGBA")


def splat_blood(image: Image.Image) -> Image.Image:
	data = np.asarray(image.convert("RGBA")).astype(np.float32)
	alpha = data[..., 3]
	out = np.zeros_like(data)
	out[..., 0] = BLOOD[0]
	out[..., 1] = BLOOD[1]
	out[..., 2] = BLOOD[2]
	out[..., 3] = alpha * (0.55 + 0.45 * np.clip(alpha / 255.0, 0.0, 1.0))
	return Image.fromarray(out.astype(np.uint8), "RGBA")


def crop(image: Image.Image) -> Image.Image:
	alpha = image.getchannel("A")
	box = alpha.getbbox()
	return image.crop(box) if box else image


def save_all(image: Image.Image, name: str) -> None:
	for folder in OUT_DIRS:
		os.makedirs(folder, exist_ok=True)
		path = os.path.join(folder, name)
		image.save(path, "PNG")
		print(f"wrote {path}")


def open_raw(*parts: str) -> Image.Image:
	return Image.open(os.path.join(RAW, *parts))


def main() -> None:
	scratch = open_raw("scratch", "scratch_01.png")
	save_all(crop(luma_blood(scratch.rotate(-45, expand=True, resample=Image.BICUBIC))), "split_cut_scratch.png")

	slash = open_raw("slash", "slash_02.png")
	save_all(crop(luma_blood(slash)), "split_cut_smear.png")

	trace = open_raw("trace", "trace_07.png")
	save_all(crop(luma_blood(trace.rotate(-90, expand=True, resample=Image.BICUBIC))), "split_cut_line.png")

	drips = (
		"splat02.png",
		"splat16.png",
		"splat19.png",
		"splat20.png",
		"splat26.png",
		"splat33.png",
		"splat34.png",
		"splat35.png",
	)
	for index, name in enumerate(drips, start=1):
		save_all(crop(splat_blood(open_raw("splat", name))), f"split_drip_{index}.png")

	for index in range(1, 6):
		save_all(crop(luma_blood(open_raw("muzzle", f"muzzle_{index:02d}.png"))), f"split_splash_{index}.png")

	for index, frame in enumerate(("flash00.png", "flash03.png", "flash06.png"), start=1):
		save_all(crop(luma_blood(open_raw("flash", frame))), f"split_burst_{index}.png")


if __name__ == "__main__":
	main()
