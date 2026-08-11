"""Bake the Tombstone Reborn BONUS-ENTRY BANNER art set.

The banner announces which of the two real buy modes the player just bought
(src/game/betModeMeta.ts) before the bought round spins:

  bonus_small (80x)    DEAD MAN'S HAND   the six-card special bar is fully awake
  bonus_super (1000x)  OPEN GRAVE        the bar plus the sealed last-reel lane

Both are a SINGLE enhanced spin, so there is no free-spin count and no ladder of
bonus levels — two tiers, nothing else.

Inputs
  assets-raw/layer_bonus/*.png              the two hero plates, generated on
                                            Layer AI (tools/fetch_layer_bonus_entry.py)
  assets-raw/kenney_haul_bonus/*/*.png      Kenney CC0 fantasy-ui DOUBLE border /
                                            divider families (brass filigree)
  assets-raw/kenney_haul_win/splat/*.png    Kenney CC0 splats, for weathering

Outputs
  static/assets/sprites/celeb/bonus_entry_small.webp
  static/assets/sprites/celeb/bonus_entry_super.webp
  static/assets/sprites/celeb/bonus_frame_small.png
  static/assets/sprites/celeb/bonus_frame_super.png

WHY THE BANNER OWNS BOTH FRAMES: the SMALL tier originally wore the win ladder's
`win_frame.png`. The win takeover then had its thin panel outline removed on
request — its gold inlay hairline, iron edge line, strap outlines and nail rims
are gone and the panel edge is carried by light alone — while the banner was
explicitly asked to keep its framing. Sharing the asset would have propagated
that removal here, so `bonus_frame_small.png` is the outlined build, kept intact.

DELIBERATELY NOT BAKED, because they already ship and are reused as-is:
  win_celeb_light.*   god-rays, lantern glow and the SUPER tier's bell rings
  win_celeb_vfx.*     starburst, spark streaks, muzzle flares, dust, gunsmoke,
                      embers, the revolver title emblem
A second copy of any of those would be a parallel VFX system, which is exactly
what src/game/winCelebrationArt.ts exists to prevent. The grade helpers, the
timber field and the alpha discipline are imported from the win bake for the
same reason.

Run:  python tools/make_bonus_entry_art.py
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from make_win_celebration_art import (
	BRASS,
	GOLD,
	IRON,
	KENNEY,
	OUT_CELEB,
	PLATE_H,
	PLATE_W,
	clear_transparent_rgb,
	grade_plate,
	wood_grain,
)

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
LAYER = os.path.join(APP, "assets-raw", "layer_bonus")
KENNEY_BONUS = os.path.join(APP, "assets-raw", "kenney_haul_bonus")

# slug -> chosen Layer AI variant. Same grade contract as the win tiers
# (shadow_crush, gold_lift), pitched so SUPER sits brighter and more golden than
# SMALL even before the runtime light layers escalate.
TIER_PLATES: list[tuple[str, str, float, float]] = [
	# slug,   source,        shadow_crush, gold_lift
	# SMALL carries a fanned hand of pale playing cards, so it takes a heavier
	# gold lift than its tier position implies: at a lower lift the card faces
	# grade out as cream and start reading like the cloned game's near-white.
	("small", "small_2.png", 0.88, 0.22),
	("super", "super_1.png", 0.94, 0.24),
]

# A Layer render sometimes lands its composition in a narrower band with flat
# black bars above and below. The banner cover-fits its plate into the frame
# window, so a surviving bar would show up as a dead black stripe across the
# hero art. Trim any fully-crushed border rows before grading.
LETTERBOX_LUMA = 10
LETTERBOX_MAX_FRAC = 0.22


def crop_letterbox(image: Image.Image) -> Image.Image:
	luma = np.asarray(image.convert("L")).astype(np.float32)
	rows = luma.mean(axis=1)
	limit = int(len(rows) * LETTERBOX_MAX_FRAC)
	top = 0
	while top < limit and rows[top] < LETTERBOX_LUMA:
		top += 1
	bottom = len(rows)
	while bottom > len(rows) - limit and rows[bottom - 1] < LETTERBOX_LUMA:
		bottom -= 1
	if top == 0 and bottom == len(rows):
		return image
	print(f"[bonus] trimmed letterbox: {top}px top, {len(rows) - bottom}px bottom")
	return image.crop((0, top, image.width, bottom))


# ---------------------------------------------------------------------------
# the SUPER frame: same construction as win_frame, escalated
# ---------------------------------------------------------------------------
# SUPER gets a visibly heavier build than SMALL so the two tiers differ in more
# than a word: a deeper timber band, a doubled iron outer band, corner straps half
# again as large, a strap on every mid-edge instead of only top and bottom, a
# second gold inlay, a brass filigree stamped into the timber and a brass rule
# top and bottom.
#
# The straps deliberately do NOT run the full length of an edge: bare weathered
# timber is the thing this frame family is recognised by, so every added piece of
# iron leaves plank showing between it and the next.
SMALL_PAD = 74  # same band as the win ladder's frame, which this tier used to wear
SUPER_PAD = 112
SMALL_STRAP = 150
SUPER_STRAP = 200  # corner strap, vs 150 on win_frame
SUPER_MID_STRAP = 150
NAIL = 9
FILIGREE_ALPHA = 0.34
# The banner's own edge tones. win_frame.png dropped its thin iron edge line and
# its gold inlay when the win takeover's panel outline was removed; the banner
# keeps both, so the tones live here rather than being imported from a frame that
# no longer draws them.
IRON_EDGE = (74, 64, 54)
# Kenney nine-slice tile: 96px with 32px corners. Used as a soft stamped
# decoration, never as crisp UI chrome — it is line art authored for 1x UI, so
# it is scaled up under a low alpha where softness reads as worn brass.
KENNEY_TILE = 96
KENNEY_SLICE = 32
FILIGREE_TILE = "panel-border-022.png"  # double outline, four-point star corners
# The divider families are HALF rules: a line fading out to the left with a
# finial on the right. Mirrored into itself it becomes a symmetric brass rule.
DIVIDER_TILE = "divider-005.png"


def nine_slice(tile: Image.Image, width: int, height: int) -> Image.Image:
	"""Stretch a 96px nine-slice tile to any size, corners kept unstretched."""
	slice_size = KENNEY_SLICE
	out = Image.new("RGBA", (width, height), (0, 0, 0, 0))
	mid_w = max(1, width - slice_size * 2)
	mid_h = max(1, height - slice_size * 2)
	regions = {
		"tl": ((0, 0, slice_size, slice_size), (0, 0), None),
		"tr": ((slice_size * 2, 0, KENNEY_TILE, slice_size), (width - slice_size, 0), None),
		"bl": ((0, slice_size * 2, slice_size, KENNEY_TILE), (0, height - slice_size), None),
		"br": (
			(slice_size * 2, slice_size * 2, KENNEY_TILE, KENNEY_TILE),
			(width - slice_size, height - slice_size),
			None,
		),
		"t": ((slice_size, 0, slice_size * 2, slice_size), (slice_size, 0), (mid_w, slice_size)),
		"b": (
			(slice_size, slice_size * 2, slice_size * 2, KENNEY_TILE),
			(slice_size, height - slice_size),
			(mid_w, slice_size),
		),
		"l": ((0, slice_size, slice_size, slice_size * 2), (0, slice_size), (slice_size, mid_h)),
		"r": (
			(slice_size * 2, slice_size, KENNEY_TILE, slice_size * 2),
			(width - slice_size, slice_size),
			(slice_size, mid_h),
		),
	}
	for box, spot, size in regions.values():
		part = tile.crop(box)
		if size is not None:
			part = part.resize(size, Image.LANCZOS)
		out.alpha_composite(part, spot)
	return out


def brass_filigree(width: int, height: int) -> Image.Image:
	"""Kenney double-border line art, recoloured to worn brass and softened."""
	path = os.path.join(KENNEY_BONUS, "double_border", FILIGREE_TILE)
	tile = Image.open(path).convert("RGBA")
	art = nine_slice(tile, width, height)
	art = art.resize((width, height), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.4))
	alpha = art.getchannel("A").point(lambda value: int(value * FILIGREE_ALPHA))
	brass = Image.new("RGBA", art.size, (*BRASS, 255))
	brass.putalpha(alpha)
	return brass


def brass_rule(width: int, height: int) -> Image.Image:
	"""Kenney half-divider mirrored into a symmetric brass rule."""
	path = os.path.join(KENNEY_BONUS, "double_divider", DIVIDER_TILE)
	half = Image.open(path).convert("RGBA").resize((width // 2, height), Image.LANCZOS)
	art = Image.new("RGBA", (half.width * 2, height), (0, 0, 0, 0))
	art.alpha_composite(half.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
	art.alpha_composite(half, (half.width, 0))
	alpha = art.getchannel("A").point(lambda value: int(value * 0.62))
	brass = Image.new("RGBA", art.size, (*GOLD, 255))
	brass.putalpha(alpha)
	return brass


def nails(draw: ImageDraw.ImageDraw, spots: list[tuple[float, float]], size: int = NAIL) -> None:
	"""Square-head brass-rimmed nails — the fastener this frame family uses."""
	for px, py in spots:
		draw.rectangle((px - size, py - size, px + size, py + size), fill=(18, 16, 14, 255))
		draw.rectangle(
			(px - size, py - size, px + size, py + size), outline=(*BRASS, 195), width=2
		)


def weather(frame: Image.Image, splats: tuple[str, ...], size: int, alpha: float) -> None:
	"""Kenney splats multiplied down over the timber, laid out across the band."""
	columns = 3 if len(splats) > 4 else 2
	for index, name in enumerate(splats):
		path = os.path.join(KENNEY, "splat", f"{name}.png")
		if not os.path.isfile(path):
			continue
		splat = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
		faded = splat.getchannel("A").point(lambda value: int(value * alpha))
		stain = Image.new("RGBA", splat.size, (11, 8, 6, 255))
		stain.putalpha(faded)
		span = size + 20
		frame.alpha_composite(
			stain,
			(
				(index % columns) * ((frame.width - span) // max(columns - 1, 1)) + 12,
				(index // columns) * (frame.height - span) + 12,
			),
		)


def punch_window(frame: Image.Image, pad: int) -> Image.Image:
	"""Knock the hero window out of the frame so the plate shows through."""
	hole = Image.new("L", frame.size, 255)
	ImageDraw.Draw(hole).rectangle(
		(pad, pad, frame.width - 1 - pad, frame.height - 1 - pad), fill=0
	)
	frame.putalpha(
		Image.fromarray(np.minimum(np.asarray(frame.getchannel("A")), np.asarray(hole)))
	)
	return clear_transparent_rgb(frame)


def build_small_frame() -> Image.Image:
	"""DEAD MAN'S HAND's frame: the timber/iron build with the gold inlay kept.

	This is the frame the SMALL tier used to borrow from the win ladder. The win
	takeover has since had its panel outline removed — the player asked for the
	celebration panels to be framed by light alone — but asked for the banner's
	framing to stay exactly as it is, so the banner now owns this build instead of
	sharing `win_frame.png` and inheriting that change.
	"""
	width = PLATE_W + SMALL_PAD * 2
	height = PLATE_H + SMALL_PAD * 2
	frame = wood_grain(width, height)
	draw = ImageDraw.Draw(frame, "RGBA")

	# iron outer band
	draw.rectangle((0, 0, width - 1, height - 1), outline=IRON, width=14)
	draw.rectangle((6, 6, width - 7, height - 7), outline=IRON_EDGE, width=2)

	# gold inlay hairline just outside the hero window
	inlay = SMALL_PAD - 16
	draw.rectangle(
		(inlay, inlay, width - 1 - inlay, height - 1 - inlay), outline=(*GOLD, 210), width=3
	)

	# iron corner straps with square-head nails
	for cx, cy in ((0, 0), (width, 0), (0, height), (width, height)):
		sx = 0 if cx == 0 else width - SMALL_STRAP
		sy = 0 if cy == 0 else height - SMALL_STRAP
		box = (sx + 8, sy + 8, sx + SMALL_STRAP - 8, sy + SMALL_STRAP - 8)
		draw.rectangle(box, fill=(*IRON, 235))
		draw.rectangle(box, outline=IRON_EDGE, width=3)
		nails(
			draw,
			[
				(sx + SMALL_STRAP * nx, sy + SMALL_STRAP * ny)
				for nx, ny in ((0.28, 0.28), (0.72, 0.28), (0.28, 0.72), (0.72, 0.72))
			],
			7,
		)

	# mid-edge branded plaques, brass-rimmed and warm-lit
	for sy in (0, height - 62):
		plaque = (width // 2 - 120, sy + 8, width // 2 + 120, sy + 54)
		draw.rectangle(plaque, fill=(40, 31, 24, 235))
		draw.rectangle(plaque, outline=(*BRASS, 200), width=3)
		draw.line((plaque[0] + 10, sy + 16, plaque[2] - 10, sy + 16), fill=(*GOLD, 90), width=2)

	weather(frame, ("splat04", "splat12", "splat20", "splat28"), 240, 0.22)
	return punch_window(frame, SMALL_PAD)


def build_super_frame() -> Image.Image:
	width = PLATE_W + SUPER_PAD * 2
	height = PLATE_H + SUPER_PAD * 2
	frame = wood_grain(width, height)

	# brass filigree stamped into the timber, under the ironwork
	frame.alpha_composite(brass_filigree(width - 24, height - 24), (12, 12))

	draw = ImageDraw.Draw(frame, "RGBA")

	# doubled iron outer band
	draw.rectangle((0, 0, width - 1, height - 1), outline=IRON, width=18)
	draw.rectangle((9, 9, width - 10, height - 10), outline=IRON_EDGE, width=3)
	draw.rectangle((24, 24, width - 25, height - 25), outline=IRON, width=8)

	# oversized corner straps, square-head nails at the four quarters
	for cx, cy in ((0, 0), (width, 0), (0, height), (width, height)):
		sx = 0 if cx == 0 else width - SUPER_STRAP
		sy = 0 if cy == 0 else height - SUPER_STRAP
		box = (sx + 10, sy + 10, sx + SUPER_STRAP - 10, sy + SUPER_STRAP - 10)
		draw.rectangle(box, fill=(*IRON, 238))
		draw.rectangle(box, outline=IRON_EDGE, width=4)
		nails(
			draw,
			[
				(sx + SUPER_STRAP * nx, sy + SUPER_STRAP * ny)
				for nx, ny in ((0.26, 0.26), (0.74, 0.26), (0.26, 0.74), (0.74, 0.74))
			],
		)

	# a strap across every mid-edge. win_frame only banded top and bottom, so
	# the extra pair down the sides is part of what makes SUPER read heavier.
	for sy in (12, height - 12 - SUPER_MID_STRAP // 2):
		box = (
			width // 2 - SUPER_MID_STRAP,
			sy,
			width // 2 + SUPER_MID_STRAP,
			sy + SUPER_MID_STRAP // 2,
		)
		draw.rectangle(box, fill=(42, 33, 25, 240))
		draw.rectangle(box, outline=(*BRASS, 205), width=4)
		nails(draw, [(box[0] + 22, (box[1] + box[3]) / 2), (box[2] - 22, (box[1] + box[3]) / 2)])
	for sx in (12, width - 12 - SUPER_MID_STRAP // 2):
		box = (
			sx,
			height // 2 - SUPER_MID_STRAP,
			sx + SUPER_MID_STRAP // 2,
			height // 2 + SUPER_MID_STRAP,
		)
		draw.rectangle(box, fill=(42, 33, 25, 240))
		draw.rectangle(box, outline=(*BRASS, 205), width=4)
		nails(draw, [((box[0] + box[2]) / 2, box[1] + 22), ((box[0] + box[2]) / 2, box[3] - 22)])

	# double gold inlay hugging the hero window
	for offset in (SUPER_PAD - 24, SUPER_PAD - 13):
		draw.rectangle(
			(offset, offset, width - 1 - offset, height - 1 - offset),
			outline=(*GOLD, 200),
			width=3,
		)

	# brass rules in the bare timber above and below the window
	rule = brass_rule(int(width * 0.44), 30)
	for ry in (SUPER_PAD - 62, height - SUPER_PAD + 34):
		frame.alpha_composite(rule, ((width - rule.width) // 2, ry))

	weather(frame, ("splat07", "splat15", "splat23", "splat31", "splat03", "splat19"), 260, 0.20)
	return punch_window(frame, SUPER_PAD)


def main() -> None:
	os.makedirs(OUT_CELEB, exist_ok=True)

	for slug, source, crush, lift in TIER_PLATES:
		path = os.path.join(LAYER, source)
		if not os.path.isfile(path):
			raise SystemExit(f"missing Layer AI plate: {path}")
		art = grade_plate(crop_letterbox(Image.open(path)), crush, lift)
		dest = os.path.join(OUT_CELEB, f"bonus_entry_{slug}.webp")
		art.save(dest, "WEBP", quality=88, method=6)
		peak = int(np.asarray(art.convert("L")).max())
		print(
			f"[bonus] tier {slug:5s} -> {os.path.basename(dest)} "
			f"maxLuma={peak} ({os.path.getsize(dest):,} B)"
		)

	for slug, pad, build in (
		("small", SMALL_PAD, build_small_frame),
		("super", SUPER_PAD, build_super_frame),
	):
		frame_path = os.path.join(OUT_CELEB, f"bonus_frame_{slug}.png")
		build().save(frame_path, optimize=True)
		print(
			f"[bonus] wrote {frame_path} ({os.path.getsize(frame_path):,} B, pad={pad})"
		)
	print("[bonus] both tiers reuse win_celeb_light / win_celeb_vfx for light and particles")


if __name__ == "__main__":
	main()
