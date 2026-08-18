"""Bake Kenney cut + drip plates for the knife split.

Haul (CC0, copy-only from the Kenney library):
  kenney_particle-pack/PNG (Transparent)/trace/trace_07  → horizontal cut
  kenney_particle-pack/PNG (Transparent)/scratch/scratch_01
  kenney_particle-pack/PNG (Transparent)/slash/slash_01
  kenney_splat-pack/PNG/Default (256px)/splat16,26,02,20,34,35 → drips

Outputs: assets-src + static + assets sprites/fx/split_cut_*.png split_drip_*.png
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW = os.path.join(APP, "assets-raw", "kenney", "gunsmoke-wounds")
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


def main() -> None:
	trace = Image.open(os.path.join(RAW, "trace", "trace_07.png"))
	save_all(crop(luma_blood(trace.rotate(-90, expand=True, resample=Image.BICUBIC))), "split_cut_line.png")

	scratch = Image.open(os.path.join(RAW, "scratch", "scratch_01.png"))
	save_all(crop(luma_blood(scratch.rotate(-45, expand=True, resample=Image.BICUBIC))), "split_cut_scratch.png")

	slash = Image.open(os.path.join(RAW, "slash", "slash_01.png"))
	save_all(crop(luma_blood(slash)), "split_cut_smear.png")

	for index, src in enumerate(("splat16.png", "splat26.png", "splat02.png", "splat20.png"), start=1):
		plate = crop(splat_blood(Image.open(os.path.join(RAW, "splat", src))))
		save_all(plate, f"split_drip_{index}.png")


if __name__ == "__main__":
	main()
