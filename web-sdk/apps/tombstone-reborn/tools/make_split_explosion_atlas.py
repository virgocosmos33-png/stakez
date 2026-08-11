"""Bake the BULLET-EXPLOSION atlas for high-multiplier split cells.

Outputs (written to BOTH asset trees so neither drifts):
    assets/sprites/fx/split_explosion.png + .json          (key `splitExplosion`)
    static/assets/sprites/fx/split_explosion.png + .json

Source
------
Kenney-style `explosions` pack, folder `Explosion_1` — the fiery orange/amber
blast with a dark smoky core (frames Explosion_1..10.png, 550x550). Every one of
the pack's ten styles was reviewed frame by frame: 5/6 are crystal-cyan, 9 is
toxic-green, 3/7/8/10 are cool or cartoon-flat. Only `Explosion_1` reads as a
gunpowder/dynamite detonation — orange fire, brown smoke — which is exactly the
western bullet-impact language this game wants, so its full 10-frame run is used.

Why a flipbook and not particles
--------------------------------
A big multiplier (>10x) is the payoff beat: the cell should visibly DETONATE, not
just gain more holes. A hand-drawn explosion loop gives real frame-to-frame
turbulence a particle spray cannot, and matches how cellFire / splitHoles are
already baked (single-band atlas, textures handed back in JSON order).
"""

from __future__ import annotations

import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
SRC_DIR = r"C:\Users\Emex33\Documents\kenney assets\kenney assets\explosions\PNG\Explosion_1"

# Two destinations: the loaded tree (assets/) and the served tree (static/assets/).
OUT_DIRS = (
	os.path.join(APP, "assets", "sprites", "fx"),
	os.path.join(APP, "static", "assets", "sprites", "fx"),
)

FRAME_COUNT = 10
# Drawn ~1.6x a card wide on the board; baking far larger than drawn size aliases
# into bright speckle under GPU minification, so keep the tile near drawn size.
TILE = 192
ALPHA_FLOOR = 8
# a source pixel this bright AND this neutral is treated as the white matte, in
# case a frame ships opaque rather than pre-cut
WHITE_LUMA = 244
NEUTRAL_SPREAD = 14


def key_white_if_opaque(image: Image.Image) -> Image.Image:
	"""If a frame has no real transparency, cut its near-white background."""
	alpha = image.getchannel("A")
	lo, _hi = alpha.getextrema()
	if lo < 255:
		return image  # already alpha-cut, trust it
	pixels = image.load()
	w, h = image.size
	for y in range(h):
		for x in range(w):
			r, g, b, _a = pixels[x, y]
			if min(r, g, b) >= WHITE_LUMA and (max(r, g, b) - min(r, g, b)) <= NEUTRAL_SPREAD:
				pixels[x, y] = (r, g, b, 0)
	return image


def alpha_crop(image: Image.Image) -> Image.Image:
	mask = image.getchannel("A").point(lambda v: 255 if v > ALPHA_FLOOR else 0)
	box = mask.getbbox()
	if box is None:
		raise SystemExit("explosion frame fully transparent")
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
	"""Zero colour under transparent pixels so downscaling can't bleed a fringe."""
	pixels = image.load()
	for y in range(image.height):
		for x in range(image.width):
			if pixels[x, y][3] == 0:
				pixels[x, y] = (0, 0, 0, 0)
	return image


def main() -> None:
	frames = []
	for i in range(1, FRAME_COUNT + 1):
		path = os.path.join(SRC_DIR, f"Explosion_{i}.png")
		if not os.path.isfile(path):
			raise SystemExit(f"missing explosion frame: {path}")
		src = Image.open(path).convert("RGBA")
		art = clear_transparent_rgb(fit_square(alpha_crop(key_white_if_opaque(src)), TILE))
		frames.append(art)
		print(f"[explosion] Explosion_1/Explosion_{i} -> {TILE}x{TILE}")

	atlas = Image.new("RGBA", (TILE * len(frames), TILE), (0, 0, 0, 0))
	meta_frames = {}
	for index, frame in enumerate(frames):
		atlas.paste(frame, (index * TILE, 0), frame)
		meta_frames[f"explosion_{index:02d}.png"] = {
			"frame": {"x": index * TILE, "y": 0, "w": TILE, "h": TILE},
			"rotated": False,
			"trimmed": False,
			"spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
			"sourceSize": {"w": TILE, "h": TILE},
		}

	meta = {
		"frames": meta_frames,
		"meta": {
			"image": "split_explosion.png",
			"format": "RGBA8888",
			"size": {"w": atlas.width, "h": atlas.height},
			"scale": "1",
			"kenney_source": "explosions/PNG/Explosion_1 (frames 1-10)",
		},
	}

	for out_dir in OUT_DIRS:
		os.makedirs(out_dir, exist_ok=True)
		png_path = os.path.join(out_dir, "split_explosion.png")
		json_path = os.path.join(out_dir, "split_explosion.json")
		atlas.save(png_path, optimize=True)
		with open(json_path, "w", encoding="utf-8") as handle:
			json.dump(meta, handle, indent=1)
		print(f"[explosion] wrote {png_path} ({os.path.getsize(png_path):,} B)")
		print(f"[explosion] wrote {json_path}")


if __name__ == "__main__":
	main()
