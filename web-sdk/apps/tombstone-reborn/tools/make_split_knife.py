"""Cut the generated split knife + slash onto true alpha.

Masters live in assets-raw/split_knife/ (copied from the Cursor gen folder
the first time this runs). The knife is a white-studio plate; the slash is a
black-void streak. Outputs go to assets-src/sprites/fx/ and static/assets/
sprites/fx/ — never an app-root assets/ folder.

Run:  python tools/make_split_knife.py
"""

from __future__ import annotations

import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW = os.path.join(APP, "assets-raw", "split_knife")
GEN = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
OUT_DIRS = [
	os.path.join(APP, "assets-src", "sprites", "fx"),
	os.path.join(APP, "static", "assets", "sprites", "fx"),
]

SENTINEL = (255, 0, 255)
FLOOD_THRESH = 26
PAD = 18

sys.path.insert(0, HERE)
from alpha_key import (  # noqa: E402
	ALPHA_FLOOR,
	alpha_crop,
	bleed_alpha,
	fit_longest,
	key_black,
)


def ensure_masters() -> None:
	os.makedirs(RAW, exist_ok=True)
	for name in ("tr_split_knife.png", "tr_split_slash.png"):
		dest = os.path.join(RAW, name)
		if os.path.exists(dest):
			continue
		src = os.path.join(GEN, name)
		if not os.path.exists(src):
			raise SystemExit(f"missing master {src}")
		shutil.copy2(src, dest)
		print(f"copied master {name}")


def key_white_flood(img: Image.Image, thresh: int = FLOOD_THRESH) -> Image.Image:
	"""Flood near-white studio pad from the border. Steel highlights stay."""
	work = img.convert("RGB")
	flood = work.copy()
	w, h = flood.size
	seeds = [
		(0, 0),
		(w - 1, 0),
		(0, h - 1),
		(w - 1, h - 1),
		(w // 2, 0),
		(w // 2, h - 1),
		(0, h // 2),
		(w - 1, h // 2),
	]
	for seed in seeds:
		if flood.getpixel(seed) != SENTINEL:
			ImageDraw.floodfill(flood, seed, SENTINEL, thresh=thresh)

	marked = np.asarray(flood)
	is_bg = (
		(marked[..., 0] == SENTINEL[0])
		& (marked[..., 1] == SENTINEL[1])
		& (marked[..., 2] == SENTINEL[2])
	)
	alpha = np.where(is_bg, 0, 255).astype(np.uint8)
	alpha_img = Image.fromarray(alpha, "L")
	alpha_img = alpha_img.filter(ImageFilter.MinFilter(3))
	alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(0.7))

	out = work.convert("RGBA")
	out.putalpha(alpha_img)
	out = bleed_alpha(out)
	data = np.array(out)
	data[data[..., 3] <= ALPHA_FLOOR] = (0, 0, 0, 0)
	return Image.fromarray(data, "RGBA")


def pad_rgba(img: Image.Image, pad: int) -> Image.Image:
	canvas = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
	canvas.paste(img, (pad, pad))
	return canvas


def write(name: str, img: Image.Image) -> None:
	for folder in OUT_DIRS:
		os.makedirs(folder, exist_ok=True)
		path = os.path.join(folder, name)
		img.save(path)
		print(f"wrote {path}  {img.size[0]}x{img.size[1]}")


def main() -> int:
	ensure_masters()

	knife = key_white_flood(Image.open(os.path.join(RAW, "tr_split_knife.png")))
	knife = pad_rgba(alpha_crop(knife), PAD)
	knife = fit_longest(knife, 1024)
	write("tr_split_knife.png", knife)

	slash = key_black(Image.open(os.path.join(RAW, "tr_split_slash.png")), 0.045, 0.16)
	slash = bleed_alpha(slash)
	slash = pad_rgba(alpha_crop(slash), 8)
	slash = fit_longest(slash, 1280)
	write("tr_split_slash.png", slash)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
