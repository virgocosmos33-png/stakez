"""Bake the SPLIT bullet-hole atlas from the Scenario western generations.

Inputs:  assets-raw/scenario_western_vfx/holes_sheet_{a,b,c}.png
Outputs: static/assets/sprites/fx/split_holes.png + split_holes.json

Each sheet is a 2x2 grid of holes, so the sheets are quartered and the good
tiles picked by index (the plank-backed quarters are skipped — they carry their
own wood panel, which would paste a second card over the symbol).

This used to be baked from `assets-raw/split_bullets/hole_{a,b,c}.png`, which
were the *starburst* generations, not holes: every hit stamped a pale radial
sparkle onto the card. The rim is now pulled down to weathered-wood brown so the
splinters read as torn timber rather than white glitter.
"""

from __future__ import annotations

import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "assets-raw", "scenario_western_vfx"))
OUT = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "fx"))
CELL = 256
ALPHA_FLOOR = 10
# pixels darker than this AND near-neutral get keyed out (Ideogram's black plate)
BLACK_LUMA = 18

# (sheet, quarter index) — quarter order is TL, TR, BL, BR.
TILES: tuple[tuple[str, int], ...] = (
	("holes_sheet_a", 0),
	("holes_sheet_a", 1),
	("holes_sheet_a", 2),
	("holes_sheet_b", 0),
	("holes_sheet_b", 2),
	("holes_sheet_c", 2),
)

# Weathered-timber rim. The raw splinters are bone-white, which reads as a
# sparkle decal on the dark board — so they are pulled to brown and then dimmed
# outright, because a merely-tinted highlight still comes out bright enough to
# glitter against the near-black cards.
RIM_TINT = (132, 100, 62)
RIM_MIX = 0.88
RIM_GAIN = 0.72


def quarter(image: Image.Image, index: int) -> Image.Image:
	w, h = image.size
	hw, hh = w // 2, h // 2
	boxes = ((0, 0, hw, hh), (hw, 0, w, hh), (0, hh, hw, h), (hw, hh, w, h))
	return image.crop(boxes[index])


def key_black(image: Image.Image) -> Image.Image:
	pixels = image.load()
	w, h = image.size
	for y in range(h):
		for x in range(w):
			r, g, b, a = pixels[x, y]
			if a <= ALPHA_FLOOR:
				pixels[x, y] = (0, 0, 0, 0)
				continue
			luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
			if luma <= BLACK_LUMA and max(r, g, b) - min(r, g, b) < 12:
				pixels[x, y] = (r, g, b, 0)
	return image


def tint_rim(image: Image.Image) -> Image.Image:
	"""Pull the bright splinter ring toward weathered wood, leave the core dark."""
	pixels = image.load()
	w, h = image.size
	tr, tg, tb = RIM_TINT
	for y in range(h):
		for x in range(w):
			r, g, b, a = pixels[x, y]
			if a <= ALPHA_FLOOR:
				continue
			luma = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
			# only the lit splinters get pulled; the punched core stays black
			mix = RIM_MIX * luma
			pixels[x, y] = (
				int((r * (1 - mix) + tr * luma * mix) * RIM_GAIN),
				int((g * (1 - mix) + tg * luma * mix) * RIM_GAIN),
				int((b * (1 - mix) + tb * luma * mix) * RIM_GAIN),
				a,
			)
	return image


def alpha_crop(image: Image.Image) -> Image.Image:
	alpha = image.getchannel("A").point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	box = alpha.getbbox()
	if box is None:
		raise SystemExit("hole tile fully transparent")
	return image.crop(box)


def fit_square(image: Image.Image, size: int) -> Image.Image:
	scale = min(size / image.width, size / image.height)
	nw = max(1, round(image.width * scale))
	nh = max(1, round(image.height * scale))
	resized = image.resize((nw, nh), Image.LANCZOS)
	canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2), resized)
	return canvas


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
	"""Zero the colour under fully transparent pixels so scaling can't bleed it."""
	pixels = image.load()
	for y in range(image.height):
		for x in range(image.width):
			if pixels[x, y][3] == 0:
				pixels[x, y] = (0, 0, 0, 0)
	return image


def main() -> None:
	os.makedirs(OUT, exist_ok=True)
	frames = []
	for sheet, index in TILES:
		path = os.path.join(RAW, f"{sheet}.png")
		if not os.path.isfile(path):
			raise SystemExit(f"missing Scenario pull: {path} (run fetch_scenario_western_vfx.py)")
		tile = quarter(Image.open(path).convert("RGBA"), index)
		art = clear_transparent_rgb(fit_square(alpha_crop(tint_rim(key_black(tile))), CELL))
		frames.append(art)
		print(f"[holes] {sheet}#{index} -> {CELL}x{CELL}")

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
			"scenario_sources": [f"{sheet}#{index}" for sheet, index in TILES],
		},
	}
	with open(json_path, "w", encoding="utf-8") as handle:
		json.dump(meta, handle, indent=1)
	print(f"[holes] wrote {png_path} ({os.path.getsize(png_path):,} B)")
	print(f"[holes] wrote {json_path}")


if __name__ == "__main__":
	main()
