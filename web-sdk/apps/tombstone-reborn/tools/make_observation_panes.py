"""Build SINGLE-CELL observation-pane overlays for THE WHITE ROOM.

Writes:
  static/assets/sprites/mirror/glass_intact.png
  static/assets/sprites/mirror/glass_broken.png
  static/assets/sprites/mirror/observation_pane_intact.png
  static/assets/sprites/mirror/observation_pane_cracked.png
  assets-raw/split_fx/ceramic_chip_00..07.png  (spit/shatter stamps)

These REPLACE Madam Mirror full-board scrying-glass sheets. Each overlay is one
SYMBOL_SIZE cell: frosted clinical glass + steel bezel + optional frost cracks.

Optional Scenario masters: drop PNGs into assets-raw/observation_panes/ as
  intact_src.png / cracked_src.png — luminance→alpha keyed like prepare_glass_overlays.

Run:  python tools/make_observation_panes.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

APP = Path(__file__).resolve().parents[1]
OUT = APP / "static" / "assets" / "sprites" / "mirror"
RAW = APP / "assets-raw" / "observation_panes"
SPLIT_RAW = APP / "assets-raw" / "split_fx"
SIZE = 512

BONE = (244, 241, 236)
SILVER = (200, 196, 188)
STEEL = (138, 134, 128)
CHARCOAL = (58, 54, 50)
BLOOD = (107, 42, 40)
DARK = (18, 16, 14)


def luminance_key(im: Image.Image, alpha_gain: float, base_alpha: float) -> Image.Image:
	im = im.convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
	out = Image.new("RGBA", (SIZE, SIZE))
	sp, op = im.load(), out.load()
	for y in range(SIZE):
		for x in range(SIZE):
			r, g, b = sp[x, y]
			lum = max(r, g, b)
			a = min(255, int(lum * alpha_gain + 255 * base_alpha))
			op[x, y] = (r, g, b, a)
	return out


def draw_intact() -> Image.Image:
	"""Frosted observation glass with steel bezel — NOT oxidized haunted mirror."""
	img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
	d = ImageDraw.Draw(img)
	m = int(SIZE * 0.06)
	# outer steel bezel
	d.rounded_rectangle([m, m, SIZE - m, SIZE - m], radius=18, fill=(*CHARCOAL, 230))
	inner = m + 14
	d.rounded_rectangle([inner, inner, SIZE - inner, SIZE - inner], radius=12, fill=(*STEEL, 210))
	glass = inner + 8
	# frosted clinical glass body (semi-transparent grey)
	body = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
	bd = ImageDraw.Draw(body)
	bd.rounded_rectangle(
		[glass, glass, SIZE - glass, SIZE - glass],
		radius=10,
		fill=(90, 88, 84, 110),
	)
	# soft fluorescent glint
	glint = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
	gd = ImageDraw.Draw(glint)
	cx, cy = SIZE * 0.38, SIZE * 0.32
	gd.ellipse([cx - 90, cy - 40, cx + 110, cy + 55], fill=(*BONE, 55))
	glint = glint.filter(ImageFilter.GaussianBlur(18))
	body.alpha_composite(glint)
	img.alpha_composite(body)
	# silver rim line
	d.rounded_rectangle(
		[glass, glass, SIZE - glass, SIZE - glass],
		radius=10,
		outline=(*SILVER, 200),
		width=3,
	)
	# corner L-brackets
	arm = 38
	for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
		x = SIZE // 2 + sx * (SIZE // 2 - m - 8)
		y = SIZE // 2 + sy * (SIZE // 2 - m - 8)
		d.line([(x, y), (x - sx * arm, y)], fill=(*BONE, 230), width=4)
		d.line([(x, y), (x, y - sy * arm)], fill=(*BONE, 230), width=4)
	# sparse dried-blood flecks in corners only
	rng = random.Random(404)
	for i in range(5):
		x = rng.randint(m + 20, m + 70) if i % 2 == 0 else SIZE - m - 70 + rng.randint(0, 40)
		y = rng.randint(m + 20, m + 70) if i < 3 else SIZE - m - 70 + rng.randint(0, 40)
		r = rng.randint(2, 5)
		d.ellipse([x - r, y - r, x + r, y + r], fill=(*BLOOD, rng.randint(70, 140)))
	return img


def draw_cracked() -> Image.Image:
	"""Same pane with frost-crack web + impact hole — single cell, not full board."""
	img = draw_intact()
	d = ImageDraw.Draw(img)
	rng = random.Random(1897)
	cx = cy = SIZE // 2
	# impact hole
	hr = 55
	d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=(0, 0, 0, 0))
	# clear the center by punching alpha
	px = img.load()
	for y in range(cy - hr, cy + hr):
		for x in range(cx - hr, cx + hr):
			if 0 <= x < SIZE and 0 <= y < SIZE:
				if (x - cx) ** 2 + (y - cy) ** 2 <= hr * hr:
					r, g, b, a = px[x, y]
					px[x, y] = (r, g, b, 0)
	# frost crack branches
	for i in range(9):
		ang = (i / 9) * math.tau + rng.uniform(-0.15, 0.15)
		x0, y0 = cx + math.cos(ang) * hr * 0.7, cy + math.sin(ang) * hr * 0.7
		pts = [(x0, y0)]
		x, y = x0, y0
		for _ in range(5):
			x += math.cos(ang + rng.uniform(-0.4, 0.4)) * rng.uniform(28, 55)
			y += math.sin(ang + rng.uniform(-0.4, 0.4)) * rng.uniform(28, 55)
			pts.append((x, y))
		d.line(pts, fill=(*BONE, 220), width=3)
		d.line(pts, fill=(*SILVER, 160), width=1)
	# jagged rim around impact
	for i in range(16):
		ang = (i / 16) * math.tau
		r0 = hr - 4
		r1 = hr + rng.randint(6, 22)
		x0, y0 = cx + math.cos(ang) * r0, cy + math.sin(ang) * r0
		x1, y1 = cx + math.cos(ang) * r1, cy + math.sin(ang) * r1
		d.line([(x0, y0), (x1, y1)], fill=(*STEEL, 200), width=2)
	return img


def draw_chip(seed: int) -> Image.Image:
	"""Small clinical spit stamp — ceramic / pill / buckle. NEVER glass knives."""
	s = 128
	img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
	d = ImageDraw.Draw(img)
	rng = random.Random(seed)
	kind = seed % 4
	cx = cy = s // 2
	if kind == 0:
		# porcelain tile chip (equant — not blade)
		pts = []
		for i in range(6):
			ang = (i / 6) * math.tau + rng.uniform(-0.15, 0.15)
			r = rng.uniform(30, 46)
			pts.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
		d.polygon(pts, fill=(*BONE, 235), outline=(*STEEL, 200))
	elif kind == 1:
		# pill capsule (clinical debris, not glass sliver)
		d.rounded_rectangle([cx - 36, cy - 14, cx + 36, cy + 14], radius=12, fill=(*BONE, 240))
		d.rounded_rectangle([cx, cy - 14, cx + 36, cy + 14], radius=12, fill=(*STEEL, 230))
		d.line([(cx, cy - 12), (cx, cy + 12)], fill=(*CHARCOAL, 120), width=1)
	elif kind == 2:
		# torn PATIENT 404 paper scrap
		pts = [
			(cx - 34, cy - 22),
			(cx + 30, cy - 18),
			(cx + 36, cy + 24),
			(cx - 28, cy + 20),
		]
		d.polygon(pts, fill=(236, 232, 224, 230), outline=(*STEEL, 180))
		for i in range(3):
			y = cy - 10 + i * 8
			d.line([(cx - 22, y), (cx + 22, y)], fill=(*CHARCOAL, 100), width=1)
	else:
		# restraint buckle fragment
		d.rounded_rectangle([cx - 28, cy - 16, cx + 28, cy + 16], radius=3, fill=(*STEEL, 230))
		d.rounded_rectangle([cx - 14, cy - 8, cx + 14, cy + 8], radius=2, fill=(*CHARCOAL, 220))
		# leather strap stub
		d.rectangle([cx - 40, cy - 6, cx - 28, cy + 6], fill=(74, 64, 56, 220))
		if rng.random() > 0.5:
			d.ellipse([cx + 10, cy - 20, cx + 18, cy - 12], fill=(*BLOOD, 140))
	return img


def main() -> None:
	OUT.mkdir(parents=True, exist_ok=True)
	SPLIT_RAW.mkdir(parents=True, exist_ok=True)
	RAW.mkdir(parents=True, exist_ok=True)

	intact_src = RAW / "intact_src.png"
	cracked_src = RAW / "cracked_src.png"
	if intact_src.is_file():
		intact = luminance_key(Image.open(intact_src), 1.25, 0.08)
		print(f"keyed {intact_src.name}")
	else:
		intact = draw_intact()
		print("procedural intact pane")
	if cracked_src.is_file():
		cracked = luminance_key(Image.open(cracked_src), 1.4, 0.05)
		print(f"keyed {cracked_src.name}")
	else:
		cracked = draw_cracked()
		print("procedural cracked pane")

	def save_atomic(path: Path, im: Image.Image) -> None:
		tmp = path.with_name(path.stem + ".tmp.png")
		im.save(tmp, format="PNG")
		try:
			tmp.replace(path)
		except OSError:
			# OneDrive / locked target — keep sibling so pipeline still has art
			alt = path.with_name(path.stem + "_wr.png")
			im.save(alt, format="PNG")
			try:
				tmp.unlink(missing_ok=True)
			except OSError:
				pass
			print(f"locked {path.name}; wrote {alt.name}")
			return
		print(f"wrote {path}")

	for name, im in (
		("observation_pane_intact.png", intact),
		("observation_pane_cracked.png", cracked),
		("glass_intact.png", intact),
		("glass_broken.png", cracked),
	):
		save_atomic(OUT / name, im)

	for i in range(8):
		chip = draw_chip(4040 + i)
		p = SPLIT_RAW / f"ceramic_chip_{i:02d}.png"
		chip.save(p)
		print(f"wrote {p}")


if __name__ == "__main__":
	main()
