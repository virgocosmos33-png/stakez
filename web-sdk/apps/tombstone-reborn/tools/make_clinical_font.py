"""Bake THE WHITE ROOM clinical win-amount bitmap font (NEW per-game face).

Face name: "clinical" — stamped hospital-chart / observation-plaque numerals.
NOT the Mining-Mayhem western slab (silverFont), NOT Ghastly Panic blood/gold.

Output:
  static/assets/fonts/whiteRoomFont/wr_clinical.{png,webp,xml}
  assets/fonts/whiteRoomFont/… (mirror for Vite import.meta.url paths)

Re-run:  python tools/make_clinical_font.py
Pipeline: regenerate_assets scope=fonts
"""

from __future__ import annotations

import os
import random
import shutil

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
OUT_STATIC = os.path.join(APP, "static", "assets", "fonts", "whiteRoomFont")
OUT_ASSETS = os.path.join(APP, "assets", "fonts", "whiteRoomFont")

# Geometric condensed — clinical chart / plaque (not western slab, not horror drip)
FACE_TTF = r"C:\Windows\Fonts\bahnschrift.ttf"
FALLBACK = r"C:\Windows\Fonts\arialbd.ttf"

CELL_H = 120
SUPER = 4
FACE_NAME = "clinical"
FILE_STEM = "wr_clinical"

# Charset: currency amounts + PRESS ANYWHERE TO CONTINUE + common UI punctuation
CHAR_IDS = (
	list(range(32, 127))  # basic ASCII
	+ [163, 165, 8364, 8377, 8381, 8369, 8361]  # £ ¥ € ₹ ₽ ₱ ₩
)


def ink_band(big_font: ImageFont.FreeTypeFont, chars: list[str]) -> tuple[int, int]:
	top: int | None = None
	bottom: int | None = None
	for char in chars:
		bbox = big_font.getbbox(char)
		if not bbox or bbox[2] <= bbox[0] or bbox[3] <= bbox[1]:
			continue
		top = bbox[1] if top is None else min(top, bbox[1])
		bottom = bbox[3] if bottom is None else max(bottom, bbox[3])
	if top is None or bottom is None:
		return 0, 1
	return top, bottom


def render_glyph(
	char: str,
	font: ImageFont.FreeTypeFont,
	cell_h: int,
	band: tuple[int, int],
	rng: random.Random,
) -> Image.Image:
	"""Stamped clinical plaque glyph: charcoal body, sparse ink noise, thin rim."""
	s = SUPER
	big = font.font_variant(size=font.size * s)
	pad = 10 * s
	band_top, band_bottom = band
	band_h = max(band_bottom - band_top, 1)
	bbox = big.getbbox(char)
	if not bbox or bbox[2] <= bbox[0]:
		bbox = (0, band_top, 6 * s, band_bottom)
	width = max(bbox[2] - bbox[0], 6 * s) + pad * 2

	canvas = Image.new("L", (width, band_h + pad * 2), 0)
	draw = ImageDraw.Draw(canvas)
	draw.text((pad - bbox[0], pad - band_top), char, font=big, fill=255)

	mask = canvas
	solid_bbox = mask.getbbox()
	if solid_bbox is None:
		return Image.new("RGBA", (max(width // s, 6), cell_h), (0, 0, 0, 0))

	# Stencil-ish slots on thick capitals (observation stamp, not western bevel)
	if char.isalpha() and char.isupper() and solid_bbox[2] - solid_bbox[0] > 18 * s:
		slot = ImageDraw.Draw(mask)
		cy = (solid_bbox[1] + solid_bbox[3]) // 2
		slot_h = max(2 * s, int((solid_bbox[3] - solid_bbox[1]) * 0.11))
		inset = int((solid_bbox[2] - solid_bbox[0]) * 0.18)
		slot.rectangle(
			[solid_bbox[0] + inset, cy - slot_h // 2, solid_bbox[2] - inset, cy + slot_h // 2],
			fill=0,
		)

	# Clinical fill: off-white → cool silver (White Room palette)
	grad = Image.new("RGBA", mask.size)
	top_c = (244, 241, 236)  # #f4f1ec
	bot_c = (200, 196, 188)  # #c8c4bc
	px = grad.load()
	h = mask.size[1]
	for y in range(h):
		f = y / max(h - 1, 1)
		r = int(top_c[0] + (bot_c[0] - top_c[0]) * f)
		g = int(top_c[1] + (bot_c[1] - top_c[1]) * f)
		b = int(top_c[2] + (bot_c[2] - top_c[2]) * f)
		for x in range(mask.size[0]):
			px[x, y] = (r, g, b, 255)

	body = Image.new("RGBA", mask.size, (0, 0, 0, 0))
	body.paste(grad, (0, 0), mask)

	# Charcoal stamp rim
	rim_mask = mask.filter(ImageFilter.MaxFilter(2 * s + 1))
	rim = Image.new("RGBA", mask.size, (42, 38, 34, 255))  # #2a2622
	layered = Image.new("RGBA", mask.size, (0, 0, 0, 0))
	layered.paste(rim, (0, 0), rim_mask)
	layered.alpha_composite(body)

	# Sparse ink-stamp speckles (deterministic per char)
	speckle = Image.new("RGBA", mask.size, (0, 0, 0, 0))
	sp = speckle.load()
	m = mask.load()
	for _ in range(max(4, (mask.size[0] * mask.size[1]) // (900 * s * s))):
		x = rng.randint(0, mask.size[0] - 1)
		y = rng.randint(0, mask.size[1] - 1)
		if m[x, y] > 180:
			sp[x, y] = (90, 42, 40, rng.randint(40, 90))  # sparse dried-blood fleck
	layered.alpha_composite(speckle)

	band_crop = layered.crop((0, pad, layered.width, pad + band_h))
	target_h = int(cell_h * 0.9)
	scale = target_h / band_h
	scaled = band_crop.resize(
		(max(int(band_crop.width * scale), 1), target_h), Image.LANCZOS
	)
	cell = Image.new("RGBA", (scaled.width, cell_h), (0, 0, 0, 0))
	cell.paste(scaled, (0, (cell_h - target_h) // 2), scaled)

	alpha_bbox = cell.split()[-1].getbbox()
	if alpha_bbox:
		cell = cell.crop((alpha_bbox[0], 0, alpha_bbox[2], cell_h))
	return cell


def write_font(out_dir: str, atlas: Image.Image, entries: list[tuple], atlas_w: int, atlas_h: int) -> None:
	os.makedirs(out_dir, exist_ok=True)
	png = os.path.join(out_dir, f"{FILE_STEM}.png")
	webp = os.path.join(out_dir, f"{FILE_STEM}.webp")
	xml_path = os.path.join(out_dir, f"{FILE_STEM}.xml")
	atlas.save(png)
	atlas.save(webp, lossless=True)
	chars_xml = "\n".join(
		f'    <char id="{code}" x="{x}" y="{y}" width="{w}" height="{h}" '
		f'xoffset="0" yoffset="0" xadvance="{adv}" yadvance="{h}"/>'
		for code, x, y, w, h, adv in entries
	)
	xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<font>
  <info face="{FACE_NAME}" size="{CELL_H}" bold="0" italic="0" charset="" unicode="" stretchH="{CELL_H}" smooth="1" aa="1" padding="0,0,0,0" spacing="1,0" outline="0"/>
  <common lineHeight="{CELL_H}" base="{CELL_H}" scaleW="{atlas_w}" scaleH="{atlas_h}" pages="1" packed="0"/>
  <pages>
    <page id="0" file="{FILE_STEM}.webp"/>
  </pages>
  <chars count="{len(entries)}">
{chars_xml}
  </chars>
</font>
"""
	with open(xml_path, "w", encoding="utf-8") as f:
		f.write(xml)
	print(f"wrote {out_dir} ({atlas_w}x{atlas_h}, {len(entries)} chars, face={FACE_NAME})")


def main() -> None:
	ttf = FACE_TTF if os.path.isfile(FACE_TTF) else FALLBACK
	font = ImageFont.truetype(ttf, CELL_H)
	ids = sorted(set(CHAR_IDS))
	chars = [chr(c) for c in ids if c != 32]
	big = font.font_variant(size=font.size * SUPER)
	band = ink_band(big, chars)

	glyphs: dict[int, Image.Image] = {}
	for code in ids:
		if code == 32:
			continue
		rng = random.Random(0xC11C1CA1 ^ code)
		glyphs[code] = render_glyph(chr(code), font, CELL_H, band, rng)
		print(f"rendered U+{code:04X} w={glyphs[code].width}")

	max_w = 1600
	spacing = 1
	rows: list[list[int]] = [[]]
	x = 0
	for code in glyphs:
		w = glyphs[code].width
		if x + w + spacing > max_w and rows[-1]:
			rows.append([])
			x = 0
		rows[-1].append(code)
		x += w + spacing

	atlas_w = max_w
	atlas_h = (CELL_H + spacing) * len(rows)
	atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))
	entries: list[tuple] = []
	space_w = int(CELL_H * 0.36)
	entries.append((32, 0, 0, space_w, 1, space_w))
	y = 0
	for row in rows:
		x = 0
		for code in row:
			g = glyphs[code]
			atlas.paste(g, (x, y), g)
			entries.append((code, x, y, g.width, CELL_H, g.width + 2))
			x += g.width + spacing
		y += CELL_H + spacing

	write_font(OUT_STATIC, atlas, entries, atlas_w, atlas_h)
	# Mirror for Vite import.meta.url ../../assets/fonts/...
	if os.path.isdir(OUT_ASSETS):
		shutil.rmtree(OUT_ASSETS)
	shutil.copytree(OUT_STATIC, OUT_ASSETS)
	print(f"mirrored -> {OUT_ASSETS}")


if __name__ == "__main__":
	main()
