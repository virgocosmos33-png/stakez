"""Bake Kenney-sourced SPLIT / lock VFX into a Tombstone-tinted atlas.

Inputs:  assets-raw/tombstone_vfx/*.png  (copied from Kenney library)
Outputs: static/assets/sprites/fx/tombstone_split_vfx.png + .json

Recolor map (role -> RGB tint applied over luminance):
  brass sparks / muzzle / flash  -> spent brass / dusty amber
  gunsmoke puffs                 -> gunsmoke grey
  dirt / scorch / scratch        -> powder-burn brown + rust
  scope circle                   -> brass ring
"""

from __future__ import annotations

import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "assets-raw", "tombstone_vfx"))
OUT = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "fx"))
CELL = 128
ALPHA_FLOOR = 8

# Frame order is the contract for src/game/tombstoneVfx.ts FRAME_* indices.
FRAMES: list[tuple[str, tuple[int, int, int], float]] = [
	# name, tint RGB, contrast boost
	("spark_01.png", (232, 196, 110), 1.15),
	("spark_03.png", (210, 168, 78), 1.2),
	("spark_05.png", (196, 140, 64), 1.15),
	("muzzle_01.png", (255, 214, 140), 1.25),
	("muzzle_03.png", (240, 180, 90), 1.2),
	("dirt_01.png", (140, 108, 72), 1.05),
	("dirt_02.png", (120, 92, 58), 1.05),
	("scorch_01.png", (72, 42, 28), 1.1),
	("scorch_02.png", (96, 48, 32), 1.1),
	("smoke_04.png", (120, 112, 100), 0.95),
	("smoke_08.png", (98, 92, 84), 0.95),
	("circle_03.png", (198, 156, 72), 1.1),
	("scratch_01.png", (86, 58, 36), 1.15),
	("slash_02.png", (160, 112, 54), 1.2),
	("puff_00.png", (110, 104, 94), 0.9),
	("puff_08.png", (92, 86, 78), 0.9),
	("flash_02.png", (255, 200, 120), 1.3),
]


def tint_luma(image: Image.Image, rgb: tuple[int, int, int], contrast: float) -> Image.Image:
	pixels = image.load()
	w, h = image.size
	tr, tg, tb = rgb
	for y in range(h):
		for x in range(w):
			r, g, b, a = pixels[x, y]
			if a <= ALPHA_FLOOR:
				pixels[x, y] = (0, 0, 0, 0)
				continue
			luma = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
			# lift midtones slightly so soft particles stay visible after tint
			luma = max(0.0, min(1.0, (luma - 0.5) * contrast + 0.5))
			# keep a whisper of original chroma so sparks don't go flat
			nr = int(min(255, tr * luma * 0.88 + r * 0.12))
			ng = int(min(255, tg * luma * 0.88 + g * 0.12))
			nb = int(min(255, tb * luma * 0.88 + b * 0.12))
			pixels[x, y] = (nr, ng, nb, a)
	return image


def alpha_crop(image: Image.Image) -> Image.Image:
	alpha = image.getchannel("A").point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	box = alpha.getbbox()
	if box is None:
		raise SystemExit(f"fully transparent: {image}")
	return image.crop(box)


def fit_square(image: Image.Image, size: int) -> Image.Image:
	scale = min(size / image.width, size / image.height) * 0.92
	nw = max(1, round(image.width * scale))
	nh = max(1, round(image.height * scale))
	resized = image.resize((nw, nh), Image.LANCZOS)
	canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2), resized)
	return canvas


def main() -> None:
	os.makedirs(OUT, exist_ok=True)
	baked: list[Image.Image] = []
	for name, tint, contrast in FRAMES:
		path = os.path.join(RAW, name)
		if not os.path.isfile(path):
			raise SystemExit(f"missing Kenney copy: {path}")
		art = fit_square(
			tint_luma(alpha_crop(Image.open(path).convert("RGBA")), tint, contrast),
			CELL,
		)
		baked.append(art)
		print(f"[tombstone_vfx] {name} -> {CELL}x{CELL} tint={tint}")

	cols = len(baked)
	atlas = Image.new("RGBA", (CELL * cols, CELL), (0, 0, 0, 0))
	meta_frames: dict[str, dict] = {}
	for index, frame in enumerate(baked):
		atlas.paste(frame, (index * CELL, 0), frame)
		key = f"vfx_{index:02d}.png"
		meta_frames[key] = {
			"frame": {"x": index * CELL, "y": 0, "w": CELL, "h": CELL},
			"rotated": False,
			"trimmed": False,
			"spriteSourceSize": {"x": 0, "y": 0, "w": CELL, "h": CELL},
			"sourceSize": {"w": CELL, "h": CELL},
		}

	png_path = os.path.join(OUT, "tombstone_split_vfx.png")
	json_path = os.path.join(OUT, "tombstone_split_vfx.json")
	atlas.save(png_path, optimize=True)
	meta = {
		"frames": meta_frames,
		"meta": {
			"image": "tombstone_split_vfx.png",
			"format": "RGBA8888",
			"size": {"w": atlas.width, "h": atlas.height},
			"scale": "1",
			"kenney_sources": [
				"kenney_particle-pack/PNG (Transparent)",
				"kenney_smoke-particles/PNG/White puff",
				"kenney_smoke-particles/PNG/Flash",
			],
		},
	}
	with open(json_path, "w", encoding="utf-8") as handle:
		json.dump(meta, handle, indent=1)
	print(f"[tombstone_vfx] wrote {png_path} ({os.path.getsize(png_path):,} B)")
	print(f"[tombstone_vfx] wrote {json_path}")


if __name__ == "__main__":
	main()
