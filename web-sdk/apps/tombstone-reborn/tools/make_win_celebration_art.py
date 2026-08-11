"""Bake the Tombstone Reborn WIN CELEBRATION art set.

This is the source of truth for the whole win ladder's shipping art. It replaces
the Madam Mirror "White Room" celebration media (celeb_t2..t7 webp/mp4 — a
straitjacketed woman in a padded asylum cell, tier 7 a literal white-out) and the
Samurai Dogs 2 template coin sheet (SD2_Coin.json) that supplied the old generic
gold-coin confetti.

Inputs
  assets-raw/layer_win/*.png            per-tier hero plates + coin/cartridge
                                        sheet, generated on Layer AI
                                        (tools/fetch_layer_win_tiers.py)
  assets-raw/kenney_haul_win/*/*.png    Kenney CC0 lights / particles / smoke /
                                        splat / gradient families
  assets-raw/scenario_western_vfx/*.png pre-existing Scenario library renders,
                                        downloaded only (never regenerated)

Outputs
  static/assets/sprites/celeb/win_tier_<slug>.webp   6 graded hero plates
  static/assets/sprites/celeb/win_frame.png          branded-iron / timber frame
  static/assets/sprites/fx/win_celeb_vfx.png/.json   celebration VFX atlas
  static/assets/sprites/fx/win_scatter.png/.json     coin + cartridge particles

Frame order in win_celeb_vfx.json is the binding contract for `WIN_VFX` in
src/game/winCelebrationArt.ts — keep the two in sync.

Alpha discipline (the thing that broke previous bakes): every transparent pixel
is forced to RGB 0,0,0 so Pixi's premultiply step cannot bleed a dark fringe, and
each particle role is alpha-normalised to a ceiling so no layer can come out as a
sticker-dense blob over the reels.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
LAYER = os.path.join(APP, "assets-raw", "layer_win")
KENNEY = os.path.join(APP, "assets-raw", "kenney_haul_win")
SCENARIO = os.path.join(APP, "assets-raw", "scenario_western_vfx")
OUT_CELEB = os.path.join(APP, "static", "assets", "sprites", "celeb")
OUT_FX = os.path.join(APP, "static", "assets", "sprites", "fx")

ALPHA_FLOOR = 8
# Two atlases, two cell sizes. Soft god-ray / glow shapes are drawn full-screen,
# so packing them at particle resolution turned them to mush; they get their own
# 512px sheet while the small particles stay at 256px.
CELL = 256
LIGHT_CELL = 512
PLATE_W, PLATE_H = 1280, 720

# ---------------------------------------------------------------------------
# tier hero plates
# ---------------------------------------------------------------------------
# slug -> chosen Layer AI variant. Escalation is baked into the grade: the low
# tiers sit deeper in shadow, the top tiers get more gold lift, so the ladder
# reads as "brighter payoff" even before the runtime VFX layers.
TIER_PLATES: list[tuple[str, str, float, float]] = [
	# slug,        source,           shadow_crush, gold_lift
	("bounty", "bounty_1.png", 0.86, 0.06),
	("showdown", "showdown_0.png", 0.88, 0.10),
	("highnoon", "highnoon_1.png", 0.92, 0.14),
	("laststand", "laststand_1.png", 0.94, 0.18),
	("bloodmoney", "bloodmoney_1.png", 0.96, 0.22),
	("boothill", "boothill_0.png", 1.00, 0.28),
]

# Nothing in the celebration may read as clinical white: highlights are pulled
# toward warm gold and hard-capped below pure white.
HIGHLIGHT_CAP = 244
GOLD = (201, 163, 74)
BRASS = (138, 104, 48)


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
	data = np.array(image)
	data[data[:, :, 3] == 0] = (0, 0, 0, 0)
	return Image.fromarray(data, "RGBA")


def grade_plate(image: Image.Image, shadow_crush: float, gold_lift: float) -> Image.Image:
	"""Warm dusty western grade: deepen shadows, warm the highlights, cap white."""
	art = image.convert("RGB").resize((PLATE_W, PLATE_H), Image.LANCZOS)
	data = np.asarray(art).astype(np.float32) / 255.0

	luma = data @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
	# desaturate slightly toward dusty, then push warmth back in via gold
	data = data * 0.82 + luma[:, :, None] * 0.18

	# shadow crush: gamma up the darks so blacks go truly black
	data = np.clip(data, 0.0, 1.0) ** (1.0 + (1.0 - shadow_crush) * 0.9)

	# gold lift on the highlights only
	weight = np.clip((luma - 0.45) / 0.55, 0.0, 1.0)[:, :, None]
	gold = np.array(GOLD, dtype=np.float32) / 255.0
	data = data * (1.0 - weight * gold_lift) + gold * weight * gold_lift

	# hard cap so no pixel reads as clinical white
	data = np.clip(data, 0.0, HIGHLIGHT_CAP / 255.0)

	art = Image.fromarray((data * 255.0).astype(np.uint8), "RGB")

	# heavy cinematic vignette — keeps the title/amount legible over the plate
	vignette = Image.new("L", (PLATE_W, PLATE_H), 0)
	draw = ImageDraw.Draw(vignette)
	draw.ellipse(
		(-PLATE_W * 0.22, -PLATE_H * 0.30, PLATE_W * 1.22, PLATE_H * 1.30), fill=255
	)
	vignette = vignette.filter(ImageFilter.GaussianBlur(PLATE_W * 0.10))
	dark = Image.new("RGB", (PLATE_W, PLATE_H), (6, 5, 4))
	art = Image.composite(art, Image.blend(art, dark, 0.62), vignette)
	return art


# ---------------------------------------------------------------------------
# branded-iron / weathered-timber win frame
# ---------------------------------------------------------------------------
FRAME_PAD = 74  # timber + iron border thickness around the hero window
IRON = (34, 30, 27)
IRON_LIT = (96, 82, 66)
TIMBER = (46, 33, 23)
TIMBER_HI = (86, 62, 40)
# warm amber the window spills onto the timber — the frame's only edge cue
GLOW_WARM = (198, 150, 78)

# NO THIN OUTLINES ANYWHERE IN THIS FRAME. A 1-3px bright stroke baked at 1428px
# and drawn at ~560px logical is minified ~2.5x, samples a single bright texel and
# comes back as a crisp hairline tracing the panel — the stray-vector-outline look
# the cloned game shipped and the thing the player asked to have removed. So the
# frame is built from broad forms (>= 8px) and wide soft gradients only, and the
# panel edge is carried by light: the rim spill below, plus the runtime god-rays
# and lantern bloom in WinCelebration.svelte.


def linear_ramp(width: int, height: int, top: int, bottom: int) -> Image.Image:
	ramp = np.linspace(top, bottom, height, dtype=np.float32)
	return Image.fromarray(
		np.repeat(ramp[:, None], width, axis=1).astype(np.uint8), "L"
	)


def iron_piece(
	frame: Image.Image,
	box: tuple[float, float, float, float],
	fill: tuple[int, int, int] = IRON,
	alpha: int = 238,
	lit: int = 70,
) -> None:
	"""A raised iron strap: flat fill plus a soft top-lit gradient, no outline."""
	x0, y0, x1, y1 = (int(round(value)) for value in box)
	width, height = max(1, x1 - x0), max(1, y1 - y0)
	piece = Image.new("RGBA", (width, height), (*fill, alpha))
	highlight = Image.new("RGBA", (width, height), (*IRON_LIT, 255))
	highlight.putalpha(
		linear_ramp(width, height, lit, 0).filter(
			ImageFilter.GaussianBlur(max(3.0, height * 0.16))
		)
	)
	piece.alpha_composite(highlight)
	frame.alpha_composite(piece, (x0, y0))


def soft_nails(frame: Image.Image, spots: list[tuple[float, float]], size: int) -> None:
	"""Square-head nails: dark head with warm light caught on it, never a rim."""
	glow = Image.new("RGBA", frame.size, (0, 0, 0, 0))
	glow_draw = ImageDraw.Draw(glow)
	heads = Image.new("RGBA", frame.size, (0, 0, 0, 0))
	head_draw = ImageDraw.Draw(heads)
	for px, py in spots:
		glow_draw.ellipse(
			(px - size * 2.1, py - size * 2.4, px + size * 2.1, py + size * 1.8),
			fill=(*GLOW_WARM, 92),
		)
		head_draw.rectangle((px - size, py - size, px + size, py + size), fill=(18, 16, 14, 255))
	frame.alpha_composite(glow.filter(ImageFilter.GaussianBlur(size * 0.9)))
	frame.alpha_composite(heads)


def rim_light(width: int, height: int, pad: int, reach: float, peak: int) -> Image.Image:
	"""Warm light spilling out of the hero window onto the surrounding timber.

	A wide blurred gradient, so minification only makes it softer — the opposite
	of a baked hairline. This is what separates the takeover from the graveyard
	behind it now that nothing is stroked.
	"""
	window = Image.new("L", (width, height), 0)
	ImageDraw.Draw(window).rectangle(
		(pad, pad, width - 1 - pad, height - 1 - pad), fill=255
	)
	spread = np.asarray(window.filter(ImageFilter.GaussianBlur(reach))).astype(np.float32)
	# keep only the spill on the timber; the window itself is punched out later
	spill = spread * (1.0 - np.asarray(window).astype(np.float32) / 255.0)
	glow = Image.new("RGBA", (width, height), (*GLOW_WARM, 255))
	glow.putalpha(
		Image.fromarray(np.clip(spill * (peak / 255.0), 0, 255).astype(np.uint8), "L")
	)
	return glow


def wood_grain(width: int, height: int) -> Image.Image:
	"""Weathered plank field: perlin noise stretched into horizontal grain."""
	noise_path = os.path.join(KENNEY, "dev", "perlin-noise.png")
	noise = Image.open(noise_path).convert("L").resize((width // 8, height), Image.BICUBIC)
	noise = noise.resize((width, height), Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.6))
	grain = np.asarray(noise).astype(np.float32) / 255.0
	base = np.array(TIMBER, dtype=np.float32)
	high = np.array(TIMBER_HI, dtype=np.float32)
	field = base[None, None, :] + (high - base)[None, None, :] * grain[:, :, None] * 0.85
	art = np.concatenate(
		[field, np.full((height, width, 1), 255.0, dtype=np.float32)], axis=2
	)
	return Image.fromarray(np.clip(art, 0, 255).astype(np.uint8), "RGBA")


def build_frame() -> Image.Image:
	"""Wanted-poster timber frame banded with branded iron straps, lit not lined."""
	width = PLATE_W + FRAME_PAD * 2
	height = PLATE_H + FRAME_PAD * 2
	frame = wood_grain(width, height)
	draw = ImageDraw.Draw(frame, "RGBA")

	# iron outer band — one broad band, no thin edge line inside it
	draw.rectangle((0, 0, width - 1, height - 1), outline=IRON, width=14)

	# warm spill from the hero window onto the timber, in place of the gold inlay
	# hairline this frame used to carry
	frame.alpha_composite(rim_light(width, height, FRAME_PAD, 24.0, 132))

	# iron corner straps with square-head nails
	strap = 150
	for cx, cy in ((0, 0), (width, 0), (0, height), (width, height)):
		sx = 0 if cx == 0 else width - strap
		sy = 0 if cy == 0 else height - strap
		iron_piece(frame, (sx + 8, sy + 8, sx + strap - 8, sy + strap - 8), alpha=235)
		soft_nails(
			frame,
			[
				(sx + strap * nx, sy + strap * ny)
				for nx, ny in ((0.28, 0.28), (0.72, 0.28), (0.28, 0.72), (0.72, 0.72))
			],
			7,
		)

	# mid-edge branded plaques top and bottom. Flat iron read as a grey TV
	# mounting tab on screen, so these are warm-lit brass-toned blocks.
	for sy in (0, height - 62):
		iron_piece(
			frame,
			(width // 2 - 120, sy + 8, width // 2 + 120, sy + 54),
			fill=(48, 37, 27),
			alpha=235,
			lit=104,
		)

	# weathering: Kenney splats scattered over the timber, multiplied down
	for index, name in enumerate(("splat04", "splat12", "splat20", "splat28")):
		path = os.path.join(KENNEY, "splat", f"{name}.png")
		if not os.path.isfile(path):
			continue
		splat = Image.open(path).convert("RGBA").resize((240, 240), Image.LANCZOS)
		alpha = splat.getchannel("A").point(lambda value: int(value * 0.22))
		stain = Image.new("RGBA", splat.size, (12, 9, 7, 255))
		stain.putalpha(alpha)
		spot = ((index % 2) * (width - 260) + 14, (index // 2) * (height - 260) + 14)
		frame.alpha_composite(stain, spot)

	# punch the hero window out — the plate shows through this hole
	hole = Image.new("L", (width, height), 255)
	ImageDraw.Draw(hole).rectangle(
		(FRAME_PAD, FRAME_PAD, width - 1 - FRAME_PAD, height - 1 - FRAME_PAD), fill=0
	)
	existing = frame.getchannel("A")
	frame.putalpha(Image.fromarray(np.minimum(np.asarray(existing), np.asarray(hole))))
	return clear_transparent_rgb(frame)


# ---------------------------------------------------------------------------
# celebration VFX atlas
# ---------------------------------------------------------------------------
PEAK = {
	"ray": 170,
	"glow": 200,
	"burst": 240,
	"star": 235,
	"muzzle": 250,
	"dust": 165,
	"smoke": 150,
	"flash": 235,
	"grime": 120,
	"line": 195,
}

# name, source path, role, tint (None keeps source colour)
def _k(sub: str, name: str) -> str:
	return os.path.join(KENNEY, sub, f"{name}.png")


def _s(name: str) -> str:
	return os.path.join(SCENARIO, f"{name}.png")


# Big soft light shapes, drawn full-screen behind / over the hero panel.
LIGHT_FRAMES: list[tuple[str, str, str, tuple[int, int, int] | None]] = [
	("rayFan", _k("lights", "cone_composed_a"), "ray", (206, 166, 82)),
	("rayStreaks", _k("lights", "streaks_composed_c"), "ray", (198, 158, 76)),
	("rayWide", _k("lights", "fan_b"), "ray", (188, 148, 72)),
	("rayCone", _k("lights", "cone_composed_d"), "ray", (210, 170, 88)),
	("glowWarm", _k("lights", "circle_b"), "glow", (196, 142, 62)),
	("glowCore", _k("lights", "circle_a"), "glow", (224, 190, 116)),
	("ringSoft", _k("lights", "ring_b"), "glow", (206, 166, 82)),
	("ringHard", _k("lights", "circle_rings_b"), "glow", (214, 176, 88)),
]

# Small particles. The Scenario entries are pre-existing library renders that are
# only downloaded and re-keyed here — nothing is generated in Scenario.
# `dust_kick_outlaw` is deliberately NOT used: it is a full prospector figure, so
# compositing it over a finished hero plate would read as a sticker.
VFX_FRAMES: list[tuple[str, str, str, tuple[int, int, int] | None]] = [
	("starburst", _s("starburst_gold"), "burst", (214, 176, 88)),
	("sparkStreak", _s("spark_streak_gold"), "burst", None),
	# the library emblem is blue-and-gold; tinted hard to gold so no cold blue
	# survives into a dark western celebration
	("starEmblem", _s("star_spiked_iron"), "burst", (198, 158, 78)),
	# The library "muzzle flash" renders are whole revolvers whose extractable
	# blast is only a few pixels wide, so the wood-grip render is kept intact as
	# a revolver emblem flanking the tier title instead. Kenney muzzle cones
	# below carry the actual muzzle-flare particle role.
	("revolverEmblem", _s("muzzle_flash_wood"), "burst", (206, 168, 96)),
	("dustPlume", _s("dust_plume"), "dust", (162, 128, 86)),
	("starBig", _k("particles", "star_04"), "star", (222, 184, 96)),
	("starSmall", _k("particles", "star_07"), "star", (214, 172, 84)),
	("starPoint", _k("particles", "star_01"), "star", (232, 200, 128)),
	("muzzleFlare", _k("particles", "muzzle_01"), "muzzle", (238, 192, 104)),
	("muzzleWide", _k("particles", "muzzle_04"), "muzzle", (230, 178, 92)),
	("dustPuffA", _k("smoke_white", "whitePuff08"), "dust", (150, 118, 78)),
	("dustPuffB", _k("smoke_white", "whitePuff16"), "dust", (132, 104, 68)),
	("smokeA", _k("particles", "smoke_04"), "smoke", (118, 110, 100)),
	("smokeB", _k("particles", "smoke_08"), "smoke", (98, 92, 84)),
	("dirtA", _k("particles", "dirt_01"), "dust", (140, 108, 72)),
	("flashPop", _k("flash", "flash04"), "flash", (240, 200, 118)),
	("emberMote", _k("particles", "circle_05"), "star", (226, 176, 88)),
	("traceLine", _k("particles", "trace_03"), "line", (208, 166, 80)),
	("grimeSplat", _k("splat", "splat12"), "grime", (26, 20, 15)),
]

FLASH_SOURCES: set[str] = set()


def tint_luma(image: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
	data = np.array(image).astype(np.float32)
	alpha = data[:, :, 3]
	luma = (data[:, :, :3] @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)) / 255.0
	target = np.array(rgb, dtype=np.float32)
	tinted = target[None, None, :] * luma[:, :, None] * 0.88 + data[:, :, :3] * 0.12
	mask = (alpha > ALPHA_FLOOR)[:, :, None]
	data[:, :, :3] = np.where(mask, np.clip(tinted, 0, 255), data[:, :, :3])
	return Image.fromarray(data.astype(np.uint8), "RGBA")


def normalise_alpha(image: Image.Image, peak: int) -> Image.Image:
	alpha = np.asarray(image.getchannel("A"))
	values = alpha[alpha > ALPHA_FLOOR]
	if values.size == 0:
		raise SystemExit("frame fully transparent")
	p99 = float(np.percentile(values, 99)) or 1.0
	scale = peak / p99
	if abs(scale - 1.0) < 0.02:
		return image
	lut = [min(255, int(round(i * scale))) for i in range(256)]
	image.putalpha(image.getchannel("A").point(lut))
	return image


def key_black(image: Image.Image) -> Image.Image:
	"""Key a solid black plate to alpha, keeping warm glow intact.

	Alpha comes from luminance so soft flare edges fade out instead of leaving a
	hard matte line, and the RGB is unpremultiplied back up so the sprite is not
	darkened by its own key.
	"""
	data = np.array(image.convert("RGBA")).astype(np.float32)
	luma = data[:, :, :3] @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
	alpha = np.clip((luma - 6.0) / 46.0, 0.0, 1.0)
	safe = np.maximum(alpha, 1e-3)[:, :, None]
	rgb = np.clip(data[:, :, :3] / safe, 0, 255)
	out = np.concatenate([rgb, (alpha * 255.0)[:, :, None]], axis=2)
	return Image.fromarray(out.astype(np.uint8), "RGBA")


def alpha_crop(image: Image.Image) -> Image.Image:
	mask = image.getchannel("A").point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	box = mask.getbbox()
	if box is None:
		raise SystemExit("frame fully transparent after keying")
	return image.crop(box)


def fit_square(image: Image.Image, size: int, fill: float = 0.94) -> Image.Image:
	scale = min(size / image.width, size / image.height) * fill
	nw = max(1, round(image.width * scale))
	nh = max(1, round(image.height * scale))
	resized = image.resize((nw, nh), Image.LANCZOS)
	canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2), resized)
	return canvas


def build_vfx_frame(
	name: str, path: str, role: str, tint: tuple[int, int, int] | None, cell: int
) -> Image.Image:
	art = Image.open(path).convert("RGBA")
	# a fully opaque source is a black-plate render — key it before anything else
	if int(np.asarray(art.getchannel("A")).min()) > 250:
		art = key_black(art)
	if tint is not None:
		art = tint_luma(art, tint)
	art = normalise_alpha(alpha_crop(art), PEAK[role])
	return clear_transparent_rgb(fit_square(art, cell))


def write_atlas(
	frames: list[tuple[str, Image.Image]], stem: str, cell: int, extra_meta: dict
) -> None:
	atlas = Image.new("RGBA", (cell * len(frames), cell), (0, 0, 0, 0))
	meta_frames: dict[str, dict] = {}
	for index, (_, art) in enumerate(frames):
		atlas.paste(art, (index * cell, 0), art)
		meta_frames[f"{stem}_{index:02d}.png"] = {
			"frame": {"x": index * cell, "y": 0, "w": cell, "h": cell},
			"rotated": False,
			"trimmed": False,
			"spriteSourceSize": {"x": 0, "y": 0, "w": cell, "h": cell},
			"sourceSize": {"w": cell, "h": cell},
		}
	png_path = os.path.join(OUT_FX, f"{stem}.png")
	atlas.save(png_path, optimize=True)
	meta = {
		"frames": meta_frames,
		"meta": {
			"image": f"{stem}.png",
			"format": "RGBA8888",
			"size": {"w": atlas.width, "h": atlas.height},
			"scale": "1",
			"frame_order": [name for name, _ in frames],
			**extra_meta,
		},
	}
	with open(os.path.join(OUT_FX, f"{stem}.json"), "w", encoding="utf-8") as handle:
		json.dump(meta, handle, indent=1)
	print(f"[win] wrote {png_path} ({os.path.getsize(png_path):,} B, {len(frames)} frames)")


# ---------------------------------------------------------------------------
# coin + cartridge scatter particles (replaces the SD2_Coin template sheet)
# ---------------------------------------------------------------------------
SCATTER_SOURCE = "scatter_1.png"
SCATTER_CELL = 96
SCATTER_MIN_AREA = 1400
SCATTER_MAX = 16


def label_blobs(mask: np.ndarray) -> list[tuple[int, int, int, int]]:
	"""Bounding boxes of connected non-zero regions (4-neighbour BFS)."""
	height, width = mask.shape
	seen = np.zeros_like(mask, dtype=bool)
	boxes: list[tuple[int, int, int, int]] = []
	for y in range(height):
		row = mask[y]
		for x in range(width):
			if not row[x] or seen[y, x]:
				continue
			queue = deque([(y, x)])
			seen[y, x] = True
			min_x = max_x = x
			min_y = max_y = y
			area = 0
			while queue:
				cy, cx = queue.popleft()
				area += 1
				min_x = min(min_x, cx)
				max_x = max(max_x, cx)
				min_y = min(min_y, cy)
				max_y = max(max_y, cy)
				for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
					if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not seen[ny, nx]:
						seen[ny, nx] = True
						queue.append((ny, nx))
			if area >= SCATTER_MIN_AREA:
				boxes.append((min_x, min_y, max_x + 1, max_y + 1))
	boxes.sort(key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True)
	return boxes[:SCATTER_MAX]


def build_scatter() -> list[tuple[str, Image.Image]]:
	source = os.path.join(LAYER, SCATTER_SOURCE)
	keyed = key_black(Image.open(source).convert("RGBA"))
	mask = np.asarray(keyed.getchannel("A")) > 40
	boxes = label_blobs(mask)
	if not boxes:
		raise SystemExit("no coin/cartridge blobs found in the scatter sheet")
	frames: list[tuple[str, Image.Image]] = []
	for index, (x0, y0, x1, y1) in enumerate(boxes):
		art = keyed.crop((x0, y0, x1, y1))
		art = normalise_alpha(alpha_crop(art), 250)
		frames.append((f"scatter{index:02d}", clear_transparent_rgb(fit_square(art, SCATTER_CELL, 0.92))))
	print(f"[win] scatter: cut {len(frames)} coin/cartridge blobs from {SCATTER_SOURCE}")
	return frames


def write_scatter_atlas(frames: list[tuple[str, Image.Image]]) -> None:
	atlas = Image.new("RGBA", (SCATTER_CELL * len(frames), SCATTER_CELL), (0, 0, 0, 0))
	meta_frames: dict[str, dict] = {}
	for index, (_, art) in enumerate(frames):
		atlas.paste(art, (index * SCATTER_CELL, 0), art)
		meta_frames[f"scatter_{index:02d}.png"] = {
			"frame": {"x": index * SCATTER_CELL, "y": 0, "w": SCATTER_CELL, "h": SCATTER_CELL},
			"rotated": False,
			"trimmed": False,
			"spriteSourceSize": {"x": 0, "y": 0, "w": SCATTER_CELL, "h": SCATTER_CELL},
			"sourceSize": {"w": SCATTER_CELL, "h": SCATTER_CELL},
		}
	png_path = os.path.join(OUT_FX, "win_scatter.png")
	atlas.save(png_path, optimize=True)
	meta = {
		"frames": meta_frames,
		"meta": {
			"image": "win_scatter.png",
			"format": "RGBA8888",
			"size": {"w": atlas.width, "h": atlas.height},
			"scale": "1",
			"source": "Layer AI FLUX.1 [dev] coin/cartridge sheet, black-keyed",
		},
	}
	with open(os.path.join(OUT_FX, "win_scatter.json"), "w", encoding="utf-8") as handle:
		json.dump(meta, handle, indent=1)
	print(f"[win] wrote {png_path} ({os.path.getsize(png_path):,} B, {len(frames)} frames)")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--frame-only",
		action="store_true",
		help="rebake win_frame.png alone (the plates and atlases are unchanged)",
	)
	args = parser.parse_args()

	os.makedirs(OUT_CELEB, exist_ok=True)
	os.makedirs(OUT_FX, exist_ok=True)

	if args.frame_only:
		frame = build_frame()
		frame_path = os.path.join(OUT_CELEB, "win_frame.png")
		frame.save(frame_path, optimize=True)
		print(f"[win] wrote {frame_path} ({os.path.getsize(frame_path):,} B, frame only)")
		return

	for slug, source, crush, lift in TIER_PLATES:
		path = os.path.join(LAYER, source)
		if not os.path.isfile(path):
			raise SystemExit(f"missing Layer AI plate: {path}")
		art = grade_plate(Image.open(path), crush, lift)
		dest = os.path.join(OUT_CELEB, f"win_tier_{slug}.webp")
		art.save(dest, "WEBP", quality=86, method=6)
		peak = int(np.asarray(art.convert("L")).max())
		print(f"[win] tier {slug:11s} -> {os.path.basename(dest)} maxLuma={peak} ({os.path.getsize(dest):,} B)")

	frame = build_frame()
	frame_path = os.path.join(OUT_CELEB, "win_frame.png")
	frame.save(frame_path, optimize=True)
	print(f"[win] wrote {frame_path} ({os.path.getsize(frame_path):,} B)")

	scenario_used: list[str] = []

	def bake(specs, cell, label):
		out: list[tuple[str, Image.Image]] = []
		for name, path, role, tint in specs:
			if not os.path.isfile(path):
				raise SystemExit(f"missing {label} source: {path}")
			if os.path.normpath(path).startswith(os.path.normpath(SCENARIO)):
				scenario_used.append(os.path.basename(path))
			art = build_vfx_frame(name, path, role, tint, cell)
			out.append((name, art))
			peak = int(np.asarray(art.getchannel("A")).max())
			print(f"[win] {label} {name:12s} role={role:6s} peakA={peak:3d}  {os.path.basename(path)}")
		return out

	write_atlas(
		bake(LIGHT_FRAMES, LIGHT_CELL, "light"),
		"win_celeb_light",
		LIGHT_CELL,
		{"kenney_sources": ["kenney_light-masks-1.0/Transparent"]},
	)
	write_atlas(
		bake(VFX_FRAMES, CELL, "vfx"),
		"win_celeb_vfx",
		CELL,
		{
			"kenney_sources": [
				"kenney_particle-pack/PNG (Transparent)",
				"kenney_smoke-particles/PNG/{White puff,Flash}",
				"kenney_splat-pack/PNG/Default (256px)",
			],
			"scenario_reused_download_only": sorted(set(scenario_used)),
		},
	)
	write_scatter_atlas(build_scatter())


if __name__ == "__main__":
	main()
