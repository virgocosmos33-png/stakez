"""Bake the TOMBSTONE REBORN board reel-frame (chassis) art.

This is the source of truth for the wooden-and-iron frame BoardPlate.svelte is
skinned with. It replaces the old procedural Pixi Graphics frame (flat plank
face + hand-drawn sockets + nail dots) with baked, crafted timber art that is
cohesive with the shipped win-celebration timber-and-iron plates.

The board is a diamond STAIRCASE of columns of differing heights, and every
cell is the SAME size (CELL_PITCH_X x SYMBOL_SIZE). So the frame is built from
three tileable / repeatable pieces the component lays down on the live geometry,
never one baked bitmap of the whole staircase (which would fight the geometry
and alias into a bright hairline when a big texture is drawn small):

  board_plate.webp        weathered timber field, drawn behind the whole
                          staircase and clipped to its silhouette. Source:
                          Layer AI FLUX.1 [dev] plank render (assets-raw/
                          layer_board_frame/board_timber.png), graded dark so
                          the symbols always read on top of it.
  board_cell_socket.png   one crafted recessed window, drawn once per VISIBLE
                          cell at the exact cell size: dark recess + soft
                          top-left inner shadow + warm brass inner lip + four
                          corner rivets. Transparent margin equal to the old
                          grout, so the timber field reads as the raised wood
                          between windows and the symbol (drawn on top, full
                          cell) is never covered.
  board_corner_bracket.png a bolted iron corner boss, drawn at the four outer
                          corners of the staircase (the leftmost + rightmost
                          columns), inside the plate's PAD overhang.

Alpha discipline (the trap every previous bake hit): broad, soft forms only —
no 1-3px bright strokes that minify into a stray hairline — and every
transparent pixel is forced to RGB 0,0,0 so Pixi's premultiply cannot bleed a
fringe. The sockets and brackets are baked at ~2.5x their on-screen size so a
large texture is never drawn tiny.

Run:  python tools/make_board_frame_art.py
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
LAYER = os.path.join(APP, "assets-raw", "layer_board_frame")
KENNEY = os.path.join(APP, "assets-raw", "kenney_haul_win")
# The Tombstone baked art lives in TWO parallel trees, exactly like the shipped
# win-celebration / special-bar assets:
#   static/assets/sprites/board  the bake target the peer scripts write to
#   assets/sprites/board         the Vite-bundled tree src/game/assets.ts loads
#                                (`new URL('../../assets/sprites/board/...')`)
# Both are physically maintained (there is no build-time copy step), so the bake
# writes to BOTH — otherwise re-running it would leave the app on stale art.
OUT_DIRS = (
	os.path.join(APP, "static", "assets", "sprites", "board"),
	os.path.join(APP, "assets", "sprites", "board"),
)

# --- palette (same family as tools/make_win_celebration_art.py) --------------
IRON = (34, 30, 27)
IRON_LIT = (96, 82, 66)
TIMBER = (46, 33, 23)
TIMBER_HI = (86, 62, 40)
BRASS = (150, 112, 58)
BRASS_LIT = (198, 150, 78)
RECESS = (11, 9, 7)

# The socket is baked at the cell's own aspect: CELL_PITCH_X : SYMBOL_SIZE.
# CELL_PITCH_X = SYMBOL_SIZE * COLUMN_PITCH_SCALE (0.8), so the ratio is fixed
# at 0.8 regardless of the solved SYMBOL_SIZE — see src/game/chassisArt.ts.
CELL_ASPECT = 0.8
SOCK_H = 320
SOCK_W = round(SOCK_H * CELL_ASPECT)  # 256
# transparent outer margin = the old BoardPlate GROUT (2.25 design px against a
# 124 design-px cell), so the timber field shows through exactly the old gutter.
GROUT_FRACTION = 2.25 / 124.0
SOCK_MARGIN = round(GROUT_FRACTION * SOCK_H)  # ~6
# corner radius = old SOCKET_RADIUS (5 design px) scaled to bake px
SOCK_RADIUS = round((5.0 / 124.0) * SOCK_H)  # ~13


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
	data = np.array(image)
	data[data[:, :, 3] == 0] = (0, 0, 0, 0)
	return Image.fromarray(data, "RGBA")


# ---------------------------------------------------------------------------
# board timber plate (Layer AI plank render, graded dark)
# ---------------------------------------------------------------------------
PLATE_SIZE = 1024


def build_plate() -> Image.Image:
	src_path = os.path.join(LAYER, "board_timber.png")
	if not os.path.isfile(src_path):
		raise SystemExit(
			f"missing Layer AI timber: {src_path}\n"
			"run tools/fetch_layer_board_frame.py first"
		)
	src = Image.open(src_path).convert("RGB")
	# crop the central plank FIELD, away from the render's top/bottom iron straps
	# and corner brackets, so the backing is clean planks the sockets sit on
	w, h = src.size
	crop = src.crop((int(w * 0.16), int(h * 0.32), int(w * 0.84), int(h * 0.70)))
	art = crop.resize((PLATE_SIZE, PLATE_SIZE), Image.LANCZOS)

	# Drive the plate off LUMA only, then remap to a single warm-amber ramp: the
	# raw FLUX render carries stray green/blue in the midtones, and this backing
	# must be pure dark amber timber so nothing off-palette shows in the gutters.
	luma = np.asarray(art.convert("L")).astype(np.float32) / 255.0
	# gentle contrast so the grain stays legible without brightening the field
	luma = np.clip(luma, 0.0, 1.0) ** 1.2
	dark = np.array([16, 11, 7], dtype=np.float32) / 255.0
	# highlight cap stays LOW (mid-brown, not lit) — this is behind the symbols
	high = np.array([132, 92, 50], dtype=np.float32) / 255.0
	data = dark[None, None, :] + (high - dark)[None, None, :] * luma[:, :, None]

	art = Image.fromarray(np.clip(data * 255.0, 0, 255).astype(np.uint8), "RGB")
	return art.convert("RGBA")


# ---------------------------------------------------------------------------
# crafted recessed cell socket
# ---------------------------------------------------------------------------
def _rounded_mask(w: int, h: int, box, radius: int) -> np.ndarray:
	mask = Image.new("L", (w, h), 0)
	ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
	return np.asarray(mask).astype(np.float32) / 255.0


def build_socket() -> Image.Image:
	w, h = SOCK_W, SOCK_H
	m = SOCK_MARGIN
	box = (m, m, w - 1 - m, h - 1 - m)
	inside = _rounded_mask(w, h, box, SOCK_RADIUS)

	ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
	# straight-edge distances of the recess (box shading; corners handled by the
	# rounded mask multiply at the end)
	d_left = xs - m
	d_right = (w - 1 - m) - xs
	d_top = ys - m
	d_bottom = (h - 1 - m) - ys
	edge = np.minimum(np.minimum(d_left, d_right), np.minimum(d_top, d_bottom))
	edge = np.clip(edge, 0.0, None)

	rgb = np.zeros((h, w, 3), dtype=np.float32)
	rgb[:] = np.array(RECESS, dtype=np.float32)

	# --- inner shadow: darken toward the rim, biased to the TOP and LEFT so the
	# window reads as pressed into the wood face (light from top-left) ----------
	shadow_w = 30.0
	falloff = np.clip(1.0 - edge / shadow_w, 0.0, 1.0)  # 1 at rim -> 0 inward
	top_bias = np.clip(1.0 - d_top / shadow_w, 0.0, 1.0)
	left_bias = np.clip(1.0 - d_left / shadow_w, 0.0, 1.0)
	shade = falloff * 0.5 + np.maximum(top_bias, left_bias) * 0.5
	rgb *= (1.0 - 0.55 * shade)[:, :, None]

	# --- faint warm catch-light on the BOTTOM-RIGHT inner wall ----------------
	bottom_bias = np.clip(1.0 - d_bottom / shadow_w, 0.0, 1.0)
	right_bias = np.clip(1.0 - d_right / shadow_w, 0.0, 1.0)
	catch = np.maximum(bottom_bias, right_bias) * np.clip(1.0 - falloff, 0.0, 1.0)
	rgb += np.array(BRASS, dtype=np.float32)[None, None, :] * (catch * 0.10)[:, :, None]

	# --- warm brass inner lip: a soft ring right at the rim -------------------
	lip = np.clip(1.0 - np.abs(edge - 4.0) / 4.0, 0.0, 1.0)
	rgb = rgb * (1.0 - lip[:, :, None]) + np.array(BRASS_LIT, dtype=np.float32)[
		None, None, :
	] * lip[:, :, None]

	alpha = inside.copy()

	# --- four corner rivets: dark bolt heads with a warm glint ----------------
	rivet = round(SOCK_H * 0.026)  # ~8 bake px, ~3 display px
	off = m + SOCK_RADIUS + rivet
	spots = [
		(off, off),
		(w - off, off),
		(off, h - off),
		(w - off, h - off),
	]
	glint = Image.new("RGBA", (w, h), (0, 0, 0, 0))
	gd = ImageDraw.Draw(glint)
	heads = Image.new("RGBA", (w, h), (0, 0, 0, 0))
	hd = ImageDraw.Draw(heads)
	for px, py in spots:
		gd.ellipse(
			(px - rivet * 1.7, py - rivet * 1.9, px + rivet * 1.7, py + rivet * 1.4),
			fill=(*BRASS_LIT, 70),
		)
		hd.ellipse((px - rivet, py - rivet, px + rivet, py + rivet), fill=(20, 17, 14, 255))
		hd.ellipse(
			(px - rivet * 0.4, py - rivet * 0.5, px + rivet * 0.2, py + rivet * 0.1),
			fill=(*BRASS_LIT, 150),
		)
	glint = glint.filter(ImageFilter.GaussianBlur(rivet * 0.7))

	base = np.concatenate([rgb, (alpha * 255.0)[:, :, None]], axis=2)
	socket = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGBA")
	socket.alpha_composite(glint)
	socket.alpha_composite(heads)
	# rivets that spilled past the rounded rim get clipped back to the socket
	rim = np.asarray(Image.fromarray((inside * 255.0).astype(np.uint8), "L"))
	socket.putalpha(
		Image.fromarray(np.minimum(np.asarray(socket.getchannel("A")), rim))
	)
	return clear_transparent_rgb(socket)


# ---------------------------------------------------------------------------
# bolted iron corner boss
# ---------------------------------------------------------------------------
def linear_ramp(width: int, height: int, top: int, bottom: int) -> Image.Image:
	ramp = np.linspace(top, bottom, height, dtype=np.float32)
	return Image.fromarray(np.repeat(ramp[:, None], width, axis=1).astype(np.uint8), "L")


def build_bracket() -> Image.Image:
	size = 132
	pad = 8
	frame = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	# rounded iron plate
	plate = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	ImageDraw.Draw(plate).rounded_rectangle(
		(pad, pad, size - 1 - pad, size - 1 - pad), radius=18, fill=(*IRON, 245)
	)
	# top-lit bevel so it reads as forged iron, not a flat grey tab
	highlight = Image.new("RGBA", (size, size), (*IRON_LIT, 255))
	highlight.putalpha(linear_ramp(size, size, 96, 0).filter(ImageFilter.GaussianBlur(10)))
	plate.alpha_composite(highlight)
	# clip the highlight to the plate shape
	plate_mask = Image.new("L", (size, size), 0)
	ImageDraw.Draw(plate_mask).rounded_rectangle(
		(pad, pad, size - 1 - pad, size - 1 - pad), radius=18, fill=255
	)
	plate.putalpha(
		Image.fromarray(np.minimum(np.asarray(plate.getchannel("A")), np.asarray(plate_mask)))
	)
	# warm brass rim glow, soft (no hard stroke)
	glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	ImageDraw.Draw(glow).rounded_rectangle(
		(pad + 2, pad + 2, size - 3 - pad, size - 3 - pad), radius=16, outline=(*BRASS, 120), width=6
	)
	glow = glow.filter(ImageFilter.GaussianBlur(5))
	plate.alpha_composite(glow)
	frame.alpha_composite(plate)

	# four bolt heads
	bolt = 12
	off = pad + 22
	spots = [(off, off), (size - off, off), (off, size - off), (size - off, size - off)]
	heads = Image.new("RGBA", (size, size), (0, 0, 0, 0))
	hd = ImageDraw.Draw(heads)
	for px, py in spots:
		hd.ellipse((px - bolt, py - bolt, px + bolt, py + bolt), fill=(16, 14, 12, 255))
		hd.ellipse(
			(px - bolt * 0.4, py - bolt * 0.55, px + bolt * 0.2, py + bolt * 0.05),
			fill=(*BRASS_LIT, 170),
		)
	frame.alpha_composite(heads)
	return clear_transparent_rgb(frame)


def save(image: Image.Image, name: str) -> None:
	for out_dir in OUT_DIRS:
		path = os.path.join(out_dir, name)
		if name.endswith(".webp"):
			image.convert("RGB").save(path, "WEBP", quality=88, method=6)
		else:
			image.save(path, optimize=True)
	first = os.path.join(OUT_DIRS[0], name)
	print(f"[board] {name} {image.width}x{image.height} ({os.path.getsize(first):,} B) x{len(OUT_DIRS)} trees")


def main() -> None:
	for out_dir in OUT_DIRS:
		os.makedirs(out_dir, exist_ok=True)
	save(build_plate(), "board_plate.webp")
	save(build_socket(), "board_cell_socket.png")
	save(build_bracket(), "board_corner_bracket.png")
	print(
		f"[board] socket margin fraction = {SOCK_MARGIN / SOCK_H:.4f} of height"
		f"  (= design grout {GROUT_FRACTION * 124:.2f}px)"
	)
	print(f"[board] socket {SOCK_W}x{SOCK_H} aspect {SOCK_W / SOCK_H:.3f} (cell = {CELL_ASPECT})")


if __name__ == "__main__":
	main()
