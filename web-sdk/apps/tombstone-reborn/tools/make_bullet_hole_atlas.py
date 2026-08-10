"""Bake the SPLIT bullet-hole atlas from Scenario transparent generations.

Inputs:  assets-raw/split_bullets/hole_{a,b,c}.png
Outputs: static/assets/sprites/fx/split_holes.png + split_holes.json

Each hole is alpha-cropped, black-keyed (Ideogram sometimes leaves a solid
black plate under the splinters), resized to a square, and packed in a row.
"""

from __future__ import annotations

import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "assets-raw", "split_bullets"))
OUT = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "fx"))
CELL = 256
NAMES = ("hole_a.png", "hole_b.png", "hole_c.png")
ALPHA_FLOOR = 10
# pixels darker than this AND near-neutral get keyed out (the black plate)
BLACK_LUMA = 18


def key_black(image: Image.Image) -> Image.Image:
	pixels = image.load()
	w, h = image.size
	for y in range(h):
		for x in range(w):
			r, g, b, a = pixels[x, y]
			if a <= ALPHA_FLOOR:
				continue
			luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
			if luma <= BLACK_LUMA and max(r, g, b) - min(r, g, b) < 12:
				pixels[x, y] = (r, g, b, 0)
	return image


def alpha_crop(image: Image.Image) -> Image.Image:
	alpha = image.getchannel("A").point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	box = alpha.getbbox()
	if box is None:
		raise SystemExit("hole image fully transparent")
	return image.crop(box)


def fit_square(image: Image.Image, size: int) -> Image.Image:
	scale = min(size / image.width, size / image.height)
	nw = max(1, round(image.width * scale))
	nh = max(1, round(image.height * scale))
	resized = image.resize((nw, nh), Image.LANCZOS)
	canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2), resized)
	return canvas


def main() -> None:
	os.makedirs(OUT, exist_ok=True)
	frames = []
	for name in NAMES:
		path = os.path.join(RAW, name)
		art = fit_square(alpha_crop(key_black(Image.open(path).convert("RGBA"))), CELL)
		frames.append(art)
		print(f"[holes] {name} -> {CELL}x{CELL}")

	atlas = Image.new("RGBA", (CELL * len(frames), CELL), (0, 0, 0, 0))
	meta_frames = {}
	for index, frame in enumerate(frames):
		atlas.paste(frame, (index * CELL, 0), frame)
		key = f"hole_{index:02d}.png"
		meta_frames[key] = {
			"frame": {"x": index * CELL, "y": 0, "w": CELL, "h": CELL},
			"rotated": False,
			"trimmed": False,
			"spriteSourceSize": {"x": 0, "y": 0, "w": CELL, "h": CELL},
			"sourceSize": {"w": CELL, "h": CELL},
		}

	png_path = os.path.join(OUT, "split_holes.png")
	json_path = os.path.join(OUT, "split_holes.json")
	atlas.save(png_path, optimize=True)
	meta = {
		"frames": meta_frames,
		"meta": {
			"image": "split_holes.png",
			"format": "RGBA8888",
			"size": {"w": atlas.width, "h": atlas.height},
			"scale": "1",
		},
	}
	with open(json_path, "w", encoding="utf-8") as handle:
		json.dump(meta, handle, indent=1)
	print(f"[holes] wrote {png_path} ({os.path.getsize(png_path):,} B)")
	print(f"[holes] wrote {json_path}")


if __name__ == "__main__":
	main()
