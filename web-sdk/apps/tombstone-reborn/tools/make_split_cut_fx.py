"""Key the 3D split knife poses + blood frames onto transparent plates.

Masters are the Cursor gens in ~/.cursor/projects/.../assets/. Outputs go to
assets-src/sprites/fx and static/assets/sprites/fx — never an app-root assets/
folder.

Blood frames pack into one horizontal atlas (split_blood.png + .json) so
SplitPanes can flip them like splitExplosion.

Run:  python tools/make_split_cut_fx.py
"""

from __future__ import annotations

import json
import os
import shutil
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW = os.path.join(APP, "assets-raw", "split_cut")
GEN = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
OUT_DIRS = [
	os.path.join(APP, "assets-src", "sprites", "fx"),
	os.path.join(APP, "static", "assets", "sprites", "fx"),
	os.path.join(APP, "assets-src", "assets", "sprites", "fx"),
]

KNIVES = {
	"split_knife_embed.png": "tr_split_knife.png",
	"split_knife_stab.png": "tr_split_knife_stab.png",
	"split_knife_slice.png": "tr_split_knife_slice.png",
}
BLOOD_FRAMES = [f"split_blood_{i:02d}.png" for i in range(1, 9)]
GASH = "split_blood_gash.png"
BLOOD_FRAME = (640, 360)

sys.path.insert(0, HERE)
from alpha_key import (  # noqa: E402
	alpha_crop,
	bleed_alpha,
	fit_longest,
	key_plate,
)


def _flood_white(img: Image.Image, thresh: int = 28) -> Image.Image:
	work = img.convert("RGB")
	flood = work.copy()
	w, h = flood.size
	sentinel = (255, 0, 255)
	for seed in (
		(0, 0),
		(w - 1, 0),
		(0, h - 1),
		(w - 1, h - 1),
		(w // 2, 0),
		(w // 2, h - 1),
		(0, h // 2),
		(w - 1, h // 2),
	):
		if flood.getpixel(seed) != sentinel:
			ImageDraw.floodfill(flood, seed, sentinel, thresh=thresh)
	import numpy as np

	marked = np.asarray(flood)
	is_bg = (
		(marked[..., 0] == sentinel[0])
		& (marked[..., 1] == sentinel[1])
		& (marked[..., 2] == sentinel[2])
	)
	alpha = np.where(is_bg, 0, 255).astype(np.uint8)
	out = work.convert("RGBA")
	out.putalpha(Image.fromarray(alpha, "L"))
	return bleed_alpha(out)


def _pad(img: Image.Image, pad: int) -> Image.Image:
	canvas = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
	canvas.paste(img, (pad, pad))
	return canvas


def write(name: str, img: Image.Image) -> None:
	for folder in OUT_DIRS:
		os.makedirs(folder, exist_ok=True)
		path = os.path.join(folder, name)
		img.save(path)
		print(f"wrote {path}  {img.size[0]}x{img.size[1]}")


def ensure_masters() -> None:
	os.makedirs(RAW, exist_ok=True)
	needed = list(KNIVES) + BLOOD_FRAMES + [GASH]
	for name in needed:
		dest = os.path.join(RAW, name)
		if os.path.exists(dest):
			continue
		src = os.path.join(GEN, name)
		if not os.path.exists(src):
			raise SystemExit(f"missing master {src}")
		shutil.copy2(src, dest)
		print(f"copied master {name}")


def pack_blood(frames: list[Image.Image]) -> tuple[Image.Image, dict]:
	fw, fh = BLOOD_FRAME
	atlas = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
	meta_frames: dict = {}
	for i, frame in enumerate(frames):
		fitted = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
		src = frame.convert("RGBA")
		scale = min(fw / src.width, fh / src.height)
		nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
		src = src.resize((nw, nh), Image.LANCZOS)
		fitted.paste(src, ((fw - nw) // 2, (fh - nh) // 2), src)
		atlas.paste(fitted, (i * fw, 0), fitted)
		key = f"blood_{i:02d}.png"
		meta_frames[key] = {
			"frame": {"x": i * fw, "y": 0, "w": fw, "h": fh},
			"rotated": False,
			"trimmed": False,
			"spriteSourceSize": {"x": 0, "y": 0, "w": fw, "h": fh},
			"sourceSize": {"w": fw, "h": fh},
		}
	sheet = {
		"frames": meta_frames,
		"meta": {
			"image": "split_blood.png",
			"format": "RGBA8888",
			"size": {"w": atlas.width, "h": atlas.height},
			"scale": "1",
		},
	}
	return atlas, sheet


def main() -> int:
	ensure_masters()

	for src_name, dest_name in KNIVES.items():
		knife = _flood_white(Image.open(os.path.join(RAW, src_name)))
		knife = _pad(alpha_crop(knife), 16)
		knife = fit_longest(knife, 1024)
		write(dest_name, knife)

	blood_plates = []
	for name in BLOOD_FRAMES:
		plate = key_plate(Image.open(os.path.join(RAW, name)), 0.06, 0.16)
		plate = bleed_alpha(plate)
		plate = _pad(alpha_crop(plate), 8)
		blood_plates.append(plate)

	atlas, sheet = pack_blood(blood_plates)
	write("split_blood.png", atlas)
	for folder in OUT_DIRS:
		path = os.path.join(folder, "split_blood.json")
		with open(path, "w", encoding="utf-8") as handle:
			json.dump(sheet, handle, indent=1)
		print(f"wrote {path}")

	gash = key_plate(Image.open(os.path.join(RAW, GASH)), 0.06, 0.16)
	gash = bleed_alpha(gash)
	gash = _pad(alpha_crop(gash), 8)
	gash = fit_longest(gash, 1024)
	write("split_blood_gash.png", gash)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
