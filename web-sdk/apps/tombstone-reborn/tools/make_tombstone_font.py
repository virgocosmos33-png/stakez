"""Bake the TOMBSTONE REBORN win-amount bitmap font (per-game face).

Face name: "tombstone" — the western display face with a branded-gold body and a
dark iron rim, so celebration amounts read as stamped gold on iron.

Drawn from the VENDORED faces (static/assets/fonts/webfont, SIL OFL 1.1), not
from a system font. Two reasons that matters:

  * Licence. This atlas embeds the source outlines as pixels, so whatever it is
    baked from ships inside the game. It used to be baked from Georgia Bold off
    C:\\Windows\\Fonts, which is proprietary and not redistributable, and which
    also made the output depend on which machine ran the script.
  * Identity. Georgia is a bookish Roman serif, near-indistinguishable from the
    Cinzel of the game this was cloned from. Rye is wood-type western with
    spurred slab serifs, matching the display role in src/game/typography.ts.

Rye carries $ £ ¥ € but no ₹ ₽ ₱ ₩, so those four fall back to Archivo Narrow
(the tabular value face) rather than being dropped from the atlas.

DIGITS GET A UNIFORM ADVANCE. Every glyph here is cropped to its ink, and the
advance used to be that ink width, which makes digits proportional even when the
source face is tabular — so a win count-up visibly jitters as the digits roll.
Digits are therefore padded into one shared cell; everything else stays snug.

Output:
  static/assets/fonts/tombstoneFont/tr_tombstone.{png,webp,xml}
(`assets/` is a junction to `static/assets`, so no mirror copy is needed.)

Re-run:  python tools/make_tombstone_font.py
"""

from __future__ import annotations

import os
import random
import tempfile

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
OUT_STATIC = os.path.join(APP, "static", "assets", "fonts", "tombstoneFont")
WEBFONT_DIR = os.path.join(APP, "static", "assets", "fonts", "webfont")

FACE_WOFF2 = "rye-400-latin.woff2"
# Only for the codepoints Rye does not ship; instanced at the same weight the
# `value` typography role renders at so the two faces agree in the HUD.
CURRENCY_WOFF2 = "archivo-narrow-var-latin-ext.woff2"
CURRENCY_WEIGHT = 700

CELL_H = 120
SUPER = 4
FACE_NAME = "tombstone"
FILE_STEM = "tr_tombstone"
DIGITS = "0123456789"

# Branded gold body, hot at the top and sinking into deep brass.
GOLD_TOP = (238, 206, 132)
GOLD_BOTTOM = (150, 108, 40)
IRON_RIM = (22, 17, 13)
EMBER_FLECK = (176, 92, 38)

CHAR_IDS = (
	list(range(32, 127))
	+ [163, 165, 8364, 8377, 8381, 8369, 8361]  # £ ¥ € ₹ ₽ ₱ ₩
)


def load_face(filename: str, weight: int | None = None) -> tuple[str, set[int]]:
	"""Unpack a vendored woff2 to a temp TTF PIL can read, plus its coverage.

	PIL/FreeType will not open woff2, but woff2 is only a compressed sfnt, so
	round-tripping it through fontTools costs nothing and keeps the bake sourced
	from the exact files the game ships.
	"""
	font = TTFont(os.path.join(WEBFONT_DIR, filename))
	if weight is not None and "fvar" in font:
		from fontTools.varLib.instancer import instantiateVariableFont

		font = instantiateVariableFont(font, {"wght": weight}, inplace=False)
	covered: set[int] = set()
	for table in font["cmap"].tables:
		covered.update(table.cmap.keys())
	path = os.path.join(tempfile.gettempdir(), f"tr_bake_{filename}.ttf")
	font.flavor = None
	font.save(path)
	return path, covered


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


def gold_gradient(size: tuple[int, int]) -> Image.Image:
	width, height = size
	column = Image.new("RGB", (1, height))
	pixels = column.load()
	for y in range(height):
		f = y / max(height - 1, 1)
		# ease the gradient so the hot gold holds longer near the top
		f = f ** 0.78
		pixels[0, y] = tuple(
			int(GOLD_TOP[i] + (GOLD_BOTTOM[i] - GOLD_TOP[i]) * f) for i in range(3)
		)
	return column.resize((width, height), Image.BILINEAR).convert("RGBA")


def render_glyph(
	char: str,
	font: ImageFont.FreeTypeFont,
	cell_h: int,
	band: tuple[int, int],
	rng: random.Random,
) -> Image.Image:
	"""Branded glyph: gold body, iron rim, burnt ember flecks."""
	s = SUPER
	big = font.font_variant(size=font.size * s)
	pad = 12 * s
	band_top, band_bottom = band
	band_h = max(band_bottom - band_top, 1)
	bbox = big.getbbox(char)
	if not bbox or bbox[2] <= bbox[0]:
		bbox = (0, band_top, 6 * s, band_bottom)
	width = max(bbox[2] - bbox[0], 6 * s) + pad * 2

	mask = Image.new("L", (width, band_h + pad * 2), 0)
	ImageDraw.Draw(mask).text((pad - bbox[0], pad - band_top), char, font=big, fill=255)
	if mask.getbbox() is None:
		return Image.new("RGBA", (max(width // s, 6), cell_h), (0, 0, 0, 0))

	body = Image.new("RGBA", mask.size, (0, 0, 0, 0))
	body.paste(gold_gradient(mask.size), (0, 0), mask)

	# Iron rim, thick enough to hold the glyph against a bright hero plate.
	rim_mask = mask.filter(ImageFilter.MaxFilter(3 * s + 1))
	rim = Image.new("RGBA", mask.size, (*IRON_RIM, 255))
	layered = Image.new("RGBA", mask.size, (0, 0, 0, 0))
	layered.paste(rim, (0, 0), rim_mask)
	layered.alpha_composite(body)

	# Burnt-brand flecks, deterministic per character.
	flecks = Image.new("RGBA", mask.size, (0, 0, 0, 0))
	fleck_pixels = flecks.load()
	mask_pixels = mask.load()
	for _ in range(max(6, (mask.size[0] * mask.size[1]) // (700 * s * s))):
		x = rng.randint(0, mask.size[0] - 1)
		y = rng.randint(0, mask.size[1] - 1)
		if mask_pixels[x, y] > 170:
			fleck_pixels[x, y] = (*EMBER_FLECK, rng.randint(50, 110))
	layered.alpha_composite(flecks)

	band_crop = layered.crop((0, pad, layered.width, pad + band_h))
	target_h = int(cell_h * 0.9)
	scale = target_h / band_h
	scaled = band_crop.resize((max(int(band_crop.width * scale), 1), target_h), Image.LANCZOS)
	cell = Image.new("RGBA", (scaled.width, cell_h), (0, 0, 0, 0))
	cell.paste(scaled, (0, (cell_h - target_h) // 2), scaled)

	alpha_bbox = cell.split()[-1].getbbox()
	if alpha_bbox:
		cell = cell.crop((alpha_bbox[0], 0, alpha_bbox[2], cell_h))
	return cell


def write_font(atlas: Image.Image, entries: list[tuple], atlas_w: int, atlas_h: int) -> None:
	os.makedirs(OUT_STATIC, exist_ok=True)
	atlas.save(os.path.join(OUT_STATIC, f"{FILE_STEM}.png"))
	atlas.save(os.path.join(OUT_STATIC, f"{FILE_STEM}.webp"), lossless=True)
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
	with open(os.path.join(OUT_STATIC, f"{FILE_STEM}.xml"), "w", encoding="utf-8") as handle:
		handle.write(xml)
	print(f"wrote {OUT_STATIC} ({atlas_w}x{atlas_h}, {len(entries)} chars, face={FACE_NAME})")


def main() -> None:
	face_path, face_covered = load_face(FACE_WOFF2)
	currency_path, currency_covered = load_face(CURRENCY_WOFF2, CURRENCY_WEIGHT)
	font = ImageFont.truetype(face_path, CELL_H)
	currency_font = ImageFont.truetype(currency_path, CELL_H)

	ids = sorted(set(CHAR_IDS))
	missing = [c for c in ids if c not in face_covered and c not in currency_covered]
	if missing:
		print(f"  skipped (in neither face): {[hex(c) for c in missing]}")
	ids = [c for c in ids if c not in missing]

	# The ink band is measured on the primary face only: it sets the common
	# baseline every glyph is scaled against, and letting a fallback glyph with
	# different vertical metrics widen it would shrink the whole face.
	chars = [chr(code) for code in ids if code != 32 and code in face_covered]
	band = ink_band(font.font_variant(size=font.size * SUPER), chars)

	glyphs: dict[int, Image.Image] = {}
	for code in ids:
		if code == 32:
			continue
		source = font if code in face_covered else currency_font
		glyphs[code] = render_glyph(chr(code), source, CELL_H, band, random.Random(0x70B570 ^ code))

	# Tabularize the digits: one shared cell, each digit centred inside it, so a
	# count-up rolls without the string re-flowing on every frame.
	digit_codes = [ord(d) for d in DIGITS if ord(d) in glyphs]
	if digit_codes:
		cell_w = max(glyphs[code].width for code in digit_codes)
		for code in digit_codes:
			glyph = glyphs[code]
			padded = Image.new("RGBA", (cell_w, glyph.height), (0, 0, 0, 0))
			padded.paste(glyph, ((cell_w - glyph.width) // 2, 0), glyph)
			glyphs[code] = padded

	max_w = 1600
	spacing = 1
	rows: list[list[int]] = [[]]
	x = 0
	for code in glyphs:
		width = glyphs[code].width
		if x + width + spacing > max_w and rows[-1]:
			rows.append([])
			x = 0
		rows[-1].append(code)
		x += width + spacing

	atlas_h = (CELL_H + spacing) * len(rows)
	atlas = Image.new("RGBA", (max_w, atlas_h), (0, 0, 0, 0))
	entries: list[tuple] = []
	space_w = int(CELL_H * 0.30)
	entries.append((32, 0, 0, space_w, 1, space_w))
	y = 0
	for row in rows:
		x = 0
		for code in row:
			glyph = glyphs[code]
			atlas.paste(glyph, (x, y), glyph)
			entries.append((code, x, y, glyph.width, CELL_H, glyph.width + 2))
			x += glyph.width + spacing
		y += CELL_H + spacing

	write_font(atlas, entries, max_w, atlas_h)

	# Guard the property the whole bake exists to protect. Printed rather than
	# asserted silently so a future change to the packing shows up immediately.
	advances = {code: adv for code, _x, _y, _w, _h, adv in entries}
	digit_advances = {advances[ord(d)] for d in DIGITS if ord(d) in advances}
	print(
		f"  digits: {'TABULAR at ' + str(next(iter(digit_advances))) if len(digit_advances) == 1 else 'PROPORTIONAL ' + str(sorted(digit_advances)) + ' -> count-ups WILL jitter'}"
	)


if __name__ == "__main__":
	main()
