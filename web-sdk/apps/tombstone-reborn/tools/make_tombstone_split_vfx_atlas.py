"""Bake the SPLIT / target-lock VFX atlas for Tombstone Reborn.

Inputs:
  assets-raw/scenario_western_vfx/*.png   hero plates from the Scenario library
  assets-raw/kenney_haul_western/*/*.png  Kenney supporting particles + smoke
Outputs:
  static/assets/sprites/fx/tombstone_split_vfx.png + .json

Frame order is the contract for `VFX` in src/game/tombstoneVfx.ts.

Two things this bake exists to prevent, both of which shipped before:

* **Sticker smoke.** The gunsmoke frames were Kenney *White puff*, which are
  near-solid blobs (~180 average alpha). Blown up to ~150px over a card they
  buried the symbol under a cream disc. Every frame is now alpha-normalised to a
  per-role peak, so smoke physically cannot come out denser than `PEAK["smoke"]`.
* **A gold ring reticle.** The atlas carried a bright brass `scope` circle, i.e.
  the yellow-circle lock the reskin was supposed to remove. There is no ring
  frame any more; TargetLock draws iron sights instead.
"""

from __future__ import annotations

import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SCENARIO = os.path.normpath(os.path.join(HERE, "..", "assets-raw", "scenario_western_vfx"))
KENNEY = os.path.normpath(os.path.join(HERE, "..", "assets-raw", "kenney_haul_western"))
OUT = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "fx"))
CELL = 128
ALPHA_FLOOR = 8

# Ceiling on each role's 99th-percentile alpha. Soft roles stay atmospheric no
# matter how dense the source plate is.
PEAK = {
	"spark": 235,
	"muzzle": 250,
	"dirt": 190,
	"scorch": 200,
	"smoke": 150,
	"puff": 150,
	"dust": 185,
	"line": 190,
	"burst": 225,
}

# name, source path, role, tint RGB (None = keep source colour), isolate flash
# The Scenario plates come out of ideogram-v3-generate-transparent, so they
# already carry real alpha — they need no background keying, only the muzzle
# renders need the revolver cut away from the blast.
FRAMES: list[tuple[str, str, str, tuple[int, int, int] | None, bool]] = [
	("sparkA", f"{KENNEY}/particles/spark_01.png", "spark", (232, 196, 110), False),
	("sparkB", f"{KENNEY}/particles/spark_03.png", "spark", (210, 168, 78), False),
	("sparkC", f"{KENNEY}/particles/spark_05.png", "spark", (196, 140, 64), False),
	("muzzleA", f"{SCENARIO}/muzzle_flash_wood.png", "muzzle", None, True),
	("muzzleB", f"{SCENARIO}/muzzle_flash_chrome.png", "muzzle", None, True),
	("dirtA", f"{KENNEY}/particles/dirt_01.png", "dirt", (140, 108, 72), False),
	("dirtB", f"{KENNEY}/particles/dirt_02.png", "dirt", (120, 92, 58), False),
	("scorchA", f"{KENNEY}/particles/scorch_01.png", "scorch", (72, 42, 28), False),
	("scorchB", f"{KENNEY}/particles/scorch_02.png", "scorch", (96, 48, 32), False),
	("smokeA", f"{KENNEY}/particles/smoke_04.png", "smoke", (126, 118, 106), False),
	("smokeB", f"{KENNEY}/particles/smoke_08.png", "smoke", (104, 98, 90), False),
	("dustPlume", f"{SCENARIO}/dust_plume.png", "dust", (166, 130, 86), False),
	("scratch", f"{KENNEY}/particles/scratch_01.png", "line", (86, 58, 36), False),
	("slash", f"{KENNEY}/particles/slash_02.png", "line", (160, 112, 54), False),
	("puffA", f"{KENNEY}/smoke_black/blackSmoke08.png", "puff", (118, 110, 100), False),
	("puffB", f"{KENNEY}/smoke_black/blackSmoke16.png", "puff", (98, 92, 84), False),
	("starburst", f"{SCENARIO}/starburst_gold.png", "burst", (201, 163, 74), False),
	("sparkStreak", f"{SCENARIO}/spark_streak_gold.png", "burst", None, False),
	# already a dark plate — tinting it just erases the shape
	("burstDark", f"{SCENARIO}/burst_dark.png", "burst", None, False),
]

# A muzzle flash render is a whole revolver; only the hot warm core is wanted.
FLASH_MIN_R = 150
FLASH_MIN_WARMTH = 45


def key_flash(image: Image.Image) -> Image.Image:
	"""Drop everything that is not the hot warm blast (i.e. drop the gun)."""
	pixels = image.load()
	for y in range(image.height):
		for x in range(image.width):
			r, g, b, a = pixels[x, y]
			if a <= ALPHA_FLOOR:
				pixels[x, y] = (0, 0, 0, 0)
				continue
			if r < FLASH_MIN_R or (r - b) < FLASH_MIN_WARMTH:
				pixels[x, y] = (0, 0, 0, 0)
	return image


def tint_luma(image: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
	pixels = image.load()
	tr, tg, tb = rgb
	for y in range(image.height):
		for x in range(image.width):
			r, g, b, a = pixels[x, y]
			if a <= ALPHA_FLOOR:
				continue
			luma = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
			# keep a whisper of source chroma so particles don't go flat
			pixels[x, y] = (
				int(min(255, tr * luma * 0.88 + r * 0.12)),
				int(min(255, tg * luma * 0.88 + g * 0.12)),
				int(min(255, tb * luma * 0.88 + b * 0.12)),
				a,
			)
	return image


def normalise_alpha(image: Image.Image, peak: int) -> Image.Image:
	"""Scale alpha so the frame's 99th percentile lands on `peak`.

	This is the guard against sticker-dense smoke: a plate that is already solid
	gets pushed down, a plate that is nearly invisible gets lifted.
	"""
	values = sorted(a for a in image.getchannel("A").getdata() if a > ALPHA_FLOOR)
	if not values:
		raise SystemExit("frame fully transparent")
	p99 = values[int(len(values) * 0.99) - 1] or 1
	scale = peak / p99
	if abs(scale - 1.0) < 0.02:
		return image
	lut = [min(255, int(round(i * scale))) for i in range(256)]
	alpha = image.getchannel("A").point(lut)
	image.putalpha(alpha)
	return image


def alpha_crop(image: Image.Image) -> Image.Image:
	alpha = image.getchannel("A").point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	box = alpha.getbbox()
	if box is None:
		raise SystemExit("frame fully transparent after keying")
	return image.crop(box)


def fit_square(image: Image.Image, size: int) -> Image.Image:
	scale = min(size / image.width, size / image.height) * 0.94
	nw = max(1, round(image.width * scale))
	nh = max(1, round(image.height * scale))
	resized = image.resize((nw, nh), Image.LANCZOS)
	canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2), resized)
	return canvas


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
	"""Zero colour under fully transparent pixels — clean alpha, no dark fringe."""
	pixels = image.load()
	for y in range(image.height):
		for x in range(image.width):
			if pixels[x, y][3] == 0:
				pixels[x, y] = (0, 0, 0, 0)
	return image


def build(path: str, role: str, tint: tuple[int, int, int] | None, flash: bool) -> Image.Image:
	if not os.path.isfile(path):
		raise SystemExit(f"missing source: {path}")
	art = Image.open(path).convert("RGBA")
	if flash:
		art = key_flash(art)
	if tint is not None:
		art = tint_luma(art, tint)
	art = normalise_alpha(alpha_crop(art), PEAK[role])
	return clear_transparent_rgb(fit_square(art, CELL))


def main() -> None:
	os.makedirs(OUT, exist_ok=True)
	baked: list[Image.Image] = []
	for name, path, role, tint, flash in FRAMES:
		art = build(path, role, tint, flash)
		baked.append(art)
		peak = max(art.getchannel("A").getdata())
		print(f"[tombstone_vfx] {name:12s} role={role:7s} peakA={peak:3d}  {os.path.basename(path)}")

	atlas = Image.new("RGBA", (CELL * len(baked), CELL), (0, 0, 0, 0))
	meta_frames: dict[str, dict] = {}
	for index, frame in enumerate(baked):
		atlas.paste(frame, (index * CELL, 0), frame)
		meta_frames[f"vfx_{index:02d}.png"] = {
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
			"frame_order": [name for name, _, _, _, _ in FRAMES],
			"scenario_sources": [
				"muzzle_flash_wood", "muzzle_flash_chrome", "dust_plume",
				"starburst_gold", "spark_streak_gold", "burst_dark",
			],
			"kenney_sources": [
				"kenney_particle-pack/PNG (Transparent)",
				"kenney_smoke-particles/PNG/Black smoke",
			],
		},
	}
	with open(json_path, "w", encoding="utf-8") as handle:
		json.dump(meta, handle, indent=1)
	print(f"[tombstone_vfx] wrote {png_path} ({os.path.getsize(png_path):,} B)")
	print(f"[tombstone_vfx] wrote {json_path}")


if __name__ == "__main__":
	main()
