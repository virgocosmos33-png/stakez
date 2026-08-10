"""Bake the SPECIAL BAR art (the six-cell rail down the left of the board).

Inputs in assets-raw/special_bar/ (Scenario GPT Image 2, native transparent PNG):
  rail_plank_raw.png      iron-framed charred plank + skull (KEEP the frame)
  plaque_frame_raw.png    hollow ornate nameplate border (tintable empty slot)
  plaque_gang_raw.png     gold GANG plaque (baked embossed label)
  plaque_outlaw_raw.png   silver OUTLAW
  plaque_smoke_raw.png    bronze SMOKE
  plaque_open_raw.png     bronze OPEN
  plaque_digup_raw.png    green DIG UP

Outputs into static/assets/sprites/tombstone/:
  bar_rail.webp
  bar_plaque.png            hollow, neutral grey for tint
  bar_plaque_gang.png       … per-kind colored plaques (no tint needed)
  bar_plaque_outlaw.png
  bar_plaque_smoke.png
  bar_plaque_open.png
  bar_plaque_digup.png

The rail KEEP its iron surround. Labeled plaques keep their metal color;
only the hollow empty frame is neutralised for KIND_TINT / EMPTY_TINT.

Scenario plaque gens ship on an opaque near-white pad. Every plaque bake
border-floods that pad to alpha 0 (shared 2:1 canvas, no trim_surround) so
the wood rail shows through. Hollow frames also punch their filled centre.

Run:  python tools/make_special_bar_art.py
"""

from __future__ import annotations

import os
from collections import deque

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "assets-raw", "special_bar"))
OUT = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "tombstone"))

RAIL_W = 320
PLAQUE_W = 384
ALPHA_FLOOR = 8
# Scenario GPT Image 2 plaques land on a flat near-white pad. Key only
# border-connected low-chroma light pixels so metal glints stay opaque.
WHITE_BG_MIN = 215
WHITE_BG_CHROMA = 28

RAIL_HIGHLIGHT = 78
RAIL_CAST = (1.0, 0.88, 0.72)

LABELED = (
	("plaque_gang_raw.png", "bar_plaque_gang.png"),
	("plaque_outlaw_raw.png", "bar_plaque_outlaw.png"),
	("plaque_smoke_raw.png", "bar_plaque_smoke.png"),
	("plaque_open_raw.png", "bar_plaque_open.png"),
	("plaque_digup_raw.png", "bar_plaque_digup.png"),
)


def alpha_crop(image: Image.Image) -> Image.Image:
	alpha = image.getchannel("A").point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	box = alpha.getbbox()
	if box is None:
		raise SystemExit("image is fully transparent — wrong input file?")
	return image.crop(box)


def is_flat_white(pixel: tuple[int, int, int, int]) -> bool:
	red, green, blue, alpha = pixel
	if alpha <= ALPHA_FLOOR:
		return True
	if min(red, green, blue) < WHITE_BG_MIN:
		return False
	return (max(red, green, blue) - min(red, green, blue)) <= WHITE_BG_CHROMA


def key_border_white(image: Image.Image) -> Image.Image:
	"""Zero alpha on near-white background reachable from the image border.

	Does NOT trim the canvas — plaques keep a shared 2:1 frame so runtime
	cell aspect and opening fractions stay aligned. Interior fills (charcoal
	panels, embossed type) are untouched because they are not border-connected
	flat white.
	"""
	art = image.convert("RGBA")
	pixels = art.load()
	width, height = art.size
	seen = [[False] * width for _ in range(height)]
	queue: deque[tuple[int, int]] = deque()

	for x in range(width):
		for y in (0, height - 1):
			if is_flat_white(pixels[x, y]):
				seen[y][x] = True
				queue.append((x, y))
	for y in range(height):
		for x in (0, width - 1):
			if not seen[y][x] and is_flat_white(pixels[x, y]):
				seen[y][x] = True
				queue.append((x, y))

	while queue:
		x, y = queue.popleft()
		for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
			if not (0 <= nx < width and 0 <= ny < height) or seen[ny][nx]:
				continue
			if is_flat_white(pixels[nx, ny]):
				seen[ny][nx] = True
				queue.append((nx, ny))

	cleared = 0
	for y in range(height):
		for x in range(width):
			if not seen[y][x]:
				continue
			if pixels[x, y][3] > ALPHA_FLOOR:
				# zero RGB with alpha — leftover white under a=0 fringes in premul blend
				pixels[x, y] = (0, 0, 0, 0)
				cleared += 1
	print(f"[bar]   keyed border-white {cleared:,} px")
	return art


def force_opaque(image: Image.Image) -> Image.Image:
	"""Kill soft alpha. Soft edges are exactly the 'wood with opacity' look."""
	red, green, blue, alpha = image.split()
	alpha = alpha.point(lambda value: 255 if value > ALPHA_FLOOR else 0)
	# LANCZOS / prior white pads can leave colour under a=0 — scrub for premul
	black = Image.new("L", image.size, 0)
	red = Image.composite(red, black, alpha)
	green = Image.composite(green, black, alpha)
	blue = Image.composite(blue, black, alpha)
	return Image.merge("RGBA", (red, green, blue, alpha))


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
	height = max(1, round(image.height * width / image.width))
	return image.resize((width, height), Image.LANCZOS)


def to_night(image: Image.Image) -> Image.Image:
	"""Darken by highlight, keep a slight warm cast on the wood."""
	values = sorted(
		v
		for v, a in zip(image.convert("L").getdata(), image.getchannel("A").getdata())
		if a > 128
	)
	if not values:
		raise SystemExit("no opaque pixels — wrong input file?")
	highlight = max(1, values[int(len(values) * 0.98)])
	scale = RAIL_HIGHLIGHT / highlight
	red, green, blue, alpha = image.split()
	toned = [
		channel.point(lambda value, cast=cast: max(0, min(255, round(value * scale * cast))))
		for channel, cast in zip((red, green, blue), RAIL_CAST)
	]
	return Image.merge("RGBA", (*toned, alpha))


def neutralise(image: Image.Image) -> Image.Image:
	"""Flatten to grey and stretch levels so KIND_TINT multiplies cleanly."""
	grey = image.convert("L")
	opaque = [
		value
		for value, alpha in zip(grey.getdata(), image.getchannel("A").getdata())
		if alpha > 128
	]
	if not opaque:
		raise SystemExit("no opaque pixels to measure — wrong input file?")
	opaque.sort()
	low = opaque[int(len(opaque) * 0.02)]
	high = opaque[int(len(opaque) * 0.98)]
	span = max(1, high - low)
	stretched = grey.point(lambda value: max(0, min(255, round((value - low) * 255 / span))))
	return Image.merge("RGBA", (stretched, stretched, stretched, image.getchannel("A")))


def report_opening(image: Image.Image) -> None:
	"""Print the plaque's hollow as fractions of the sprite."""
	alpha = image.getchannel("A")

	def clear_run(values: list[int], start: int) -> tuple[int, int]:
		low = start
		while low > 0 and values[low - 1] <= ALPHA_FLOOR:
			low -= 1
		high = start
		while high < len(values) - 1 and values[high + 1] <= ALPHA_FLOOR:
			high += 1
		return low, high + 1

	row = [alpha.getpixel((x, image.height // 2)) for x in range(image.width)]
	column = [alpha.getpixel((image.width // 4, y)) for y in range(image.height)]
	left, right = clear_run(row, image.width // 2)
	top, bottom = clear_run(column, image.height // 2)
	print(
		f"[bar]   opening x {left / image.width:.4f}..{right / image.width:.4f}"
		f"  y {top / image.height:.4f}..{bottom / image.height:.4f}"
	)
	print(f"[bar]   plaque size {image.width}x{image.height}")


def report_rail(image: Image.Image) -> None:
	print(f"[bar]   rail size {image.width}x{image.height}")
	inset = max(24, round(image.width * 0.14))
	print(f"[bar]   suggested RAIL_INSET={inset}")


def save(art: Image.Image, out_name: str) -> None:
	path = os.path.join(OUT, out_name)
	if out_name.endswith(".webp"):
		art.save(path, quality=90, method=6)
	else:
		art.save(path, optimize=True)
	print(f"[bar] {out_name} {art.width}x{art.height} ({os.path.getsize(path):,} B)")


def build_rail() -> None:
	source = Image.open(os.path.join(RAW, "rail_plank_raw.png")).convert("RGBA")
	art = to_night(force_opaque(resize_to_width(alpha_crop(source), RAIL_W)))
	save(art, "bar_rail.webp")
	report_rail(art)


def punch_hollow(image: Image.Image, color_slack: int = 48) -> tuple[Image.Image, tuple[float, float, float, float]]:
	"""Clear the filled centre GPT often leaves inside a 'hollow' frame.

	Flood-fills from the image centre through near-seed colours and zeros alpha.
	Returns the image and the hole bbox as fractions (x0, x1, y0, y1).
	"""
	pixels = image.load()
	width, height = image.size
	seed_x, seed_y = width // 2, height // 2
	seed = pixels[seed_x, seed_y]
	queue: deque[tuple[int, int]] = deque([(seed_x, seed_y)])
	seen = {(seed_x, seed_y)}
	while queue:
		x, y = queue.popleft()
		for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
			if not (0 <= nx < width and 0 <= ny < height) or (nx, ny) in seen:
				continue
			red, green, blue, alpha = pixels[nx, ny]
			if alpha <= ALPHA_FLOOR:
				seen.add((nx, ny))
				continue
			dist = abs(red - seed[0]) + abs(green - seed[1]) + abs(blue - seed[2])
			if dist <= color_slack:
				seen.add((nx, ny))
				queue.append((nx, ny))
	xs = [x for x, _ in seen]
	ys = [y for _, y in seen]
	hole = (
		min(xs) / width,
		(max(xs) + 1) / width,
		min(ys) / height,
		(max(ys) + 1) / height,
	)
	for x, y in seen:
		if pixels[x, y][3] > ALPHA_FLOOR:
			pixels[x, y] = (0, 0, 0, 0)
	return image, hole


def build_plaque() -> None:
	source = Image.open(os.path.join(RAW, "plaque_frame_raw.png")).convert("RGBA")
	# key white pad, punch centre fill, THEN harden alpha — never revive trim_surround
	art = key_border_white(source)
	art, hole = punch_hollow(resize_to_width(art, PLAQUE_W))
	art = neutralise(force_opaque(art))
	save(art, "bar_plaque.png")
	print(
		f"[bar]   opening x {hole[0]:.4f}..{hole[1]:.4f}"
		f"  y {hole[2]:.4f}..{hole[3]:.4f}"
	)
	print(f"[bar]   plaque size {art.width}x{art.height}")


def build_labeled() -> None:
	for raw_name, out_name in LABELED:
		source = Image.open(os.path.join(RAW, raw_name)).convert("RGBA")
		# key white pad; keep metal color + embossed label + charcoal panel
		art = force_opaque(resize_to_width(key_border_white(source), PLAQUE_W))
		save(art, out_name)


if __name__ == "__main__":
	os.makedirs(OUT, exist_ok=True)
	build_rail()
	build_plaque()
	build_labeled()
