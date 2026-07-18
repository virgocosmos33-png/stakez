"""Bake a dripping-blood bitmap font atlas that replaces the gold font.

Renders the same charset as the original mm_gold atlas using Ghastly Panic
(the user-supplied horror typeface), colored with a blood gradient + dark rim,
and writes mm_gold.png/webp/xml in place (face stays "gold" so every
component keeps working untouched).
"""

import os
import shutil
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
FONT_DIR = os.path.join(APP, "static", "assets", "fonts", "goldFont")
NOSIFER = os.path.join(HERE, "GhastlyPanic.ttf")
FALLBACK = r"C:\Windows\Fonts\arialbd.ttf"

CELL_H = 105  # matches original metrics (lineHeight/base/height all 105)
SUPER = 4  # supersampling factor

ORIGINAL_XML = os.path.join(FONT_DIR, "mm_gold.xml")


def charset() -> list[int]:
    tree = ET.parse(ORIGINAL_XML)
    ids = []
    for char in tree.iter("char"):
        value = char.get("id")
        if value and value.isdigit():
            ids.append(int(value))
    return sorted(ids)


def ink_band(big_font: ImageFont.FreeTypeFont, chars: list[str]) -> tuple[int, int]:
    """Real ink extents (min top, max bottom) across the charset.

    Ghastly Panic declares enormous ascent/descent, so metrics-based fitting
    renders microscopic glyphs; measuring actual ink keeps the letterforms
    filling the cell while every glyph still shares one baseline.
    """
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
) -> Image.Image:
    """Render one glyph at supersampled resolution, blood styled, band-aligned."""
    s = SUPER
    big = font.font_variant(size=font.size * s)
    pad = 14 * s
    band_top, band_bottom = band
    band_h = band_bottom - band_top
    bbox = big.getbbox(char)
    if not bbox or bbox[2] <= bbox[0]:
        bbox = (0, band_top, 6 * s, band_bottom)
    width = max(bbox[2] - bbox[0], 6 * s) + pad * 2

    canvas = Image.new("L", (width, band_h + pad * 2), 0)
    draw = ImageDraw.Draw(canvas)
    # anchor the shared ink band; all glyphs keep one baseline
    draw.text((pad - bbox[0], pad - band_top), char, font=big, fill=255)

    mask = canvas
    solid_bbox = mask.getbbox()
    if solid_bbox is None:
        return Image.new("RGBA", (max(width // s, 6), cell_h), (0, 0, 0, 0))

    # blood gradient: bright arterial red at top -> near-black dried blood below
    grad = Image.new("RGBA", mask.size)
    top_color = (214, 28, 22)
    bottom_color = (74, 3, 3)
    height = mask.size[1]
    px = grad.load()
    for y in range(height):
        f = y / max(height - 1, 1)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * f)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * f)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * f)
        for x in range(mask.size[0]):
            px[x, y] = (r, g, b, 255)

    body = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    body.paste(grad, (0, 0), mask)

    # dark rim so it reads on any background
    rim_mask = mask.filter(ImageFilter.MaxFilter(2 * s + 1))
    rim = Image.new("RGBA", mask.size, (26, 0, 0, 255))
    layered = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    layered.paste(rim, (0, 0), rim_mask)
    layered.alpha_composite(body)

    # glossy highlight band near the top of the letterforms
    glyph_top = solid_bbox[1]
    glyph_h = solid_bbox[3] - solid_bbox[1]
    highlight_mask = mask.point(lambda v: v)
    hl = Image.new("L", mask.size, 0)
    hl_draw = ImageDraw.Draw(hl)
    hl_draw.rectangle(
        [0, glyph_top + int(glyph_h * 0.08), mask.size[0], glyph_top + int(glyph_h * 0.26)],
        fill=110,
    )
    hl.paste(0, (0, 0), highlight_mask.point(lambda v: 255 - v))
    shine = Image.new("RGBA", mask.size, (255, 120, 110, 0))
    shine.putalpha(hl)
    layered.alpha_composite(shine)

    # scale the styled band into the cell (small margin so drips survive)
    band_crop = layered.crop((0, pad, layered.width, pad + band_h))
    target_h = int(cell_h * 0.94)
    scale = target_h / band_h
    scaled = band_crop.resize(
        (max(int(band_crop.width * scale), 1), target_h), Image.LANCZOS
    )
    cell = Image.new("RGBA", (scaled.width, cell_h), (0, 0, 0, 0))
    cell.paste(scaled, (0, (cell_h - target_h) // 2))

    # trim horizontal whitespace only
    alpha_bbox = cell.getbbox()
    if alpha_bbox:
        cell = cell.crop((alpha_bbox[0], 0, alpha_bbox[2], cell_h))
    return cell


def main() -> None:
    ids = charset()
    ghastly = ImageFont.truetype(NOSIFER, CELL_H)
    fallback = ImageFont.truetype(FALLBACK, CELL_H)
    from fontTools.ttLib import TTFont

    ghastly_cmap = set(TTFont(NOSIFER).getBestCmap().keys())

    def assigned_font(code: int) -> ImageFont.FreeTypeFont:
        # Ghastly Panic maps some non-ASCII codes to a decorative notdef ring;
        # use the fallback for currency symbols so amounts stay legible
        return ghastly if code in ghastly_cmap and code <= 122 else fallback

    # one shared ink band per font keeps a common baseline across its glyphs
    bands: dict[ImageFont.FreeTypeFont, tuple[int, int]] = {}
    for font in (ghastly, fallback):
        chars = [chr(code) for code in ids if code != 32 and assigned_font(code) is font]
        if chars:
            big = font.font_variant(size=font.size * SUPER)
            bands[font] = ink_band(big, chars)

    glyphs: dict[int, Image.Image] = {}
    for code in ids:
        char = chr(code)
        if code == 32:
            continue
        font = assigned_font(code)
        glyphs[code] = render_glyph(char, font, CELL_H, bands[font])
        print(f"rendered {code} w={glyphs[code].width}")

    # pack into rows max 1500px wide, 1px spacing
    max_w = 1500
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

    entries = []
    space_width = int(CELL_H * 0.38)
    entries.append((32, 0, 0, space_width, 1, space_width))  # space
    y = 0
    for row in rows:
        x = 0
        for code in row:
            glyph = glyphs[code]
            atlas.paste(glyph, (x, y))
            entries.append((code, x, y, glyph.width, CELL_H, glyph.width + 2))
            x += glyph.width + spacing
        y += CELL_H + spacing

    # backup originals once
    backup = os.path.join(FONT_DIR, "backup_gold")
    if not os.path.isdir(backup):
        os.makedirs(backup)
        for name in ("mm_gold.png", "mm_gold.webp", "mm_gold.xml"):
            shutil.copy2(os.path.join(FONT_DIR, name), os.path.join(backup, name))

    atlas.save(os.path.join(FONT_DIR, "mm_gold.png"))
    atlas.save(os.path.join(FONT_DIR, "mm_gold.webp"), lossless=True)

    chars_xml = "\n".join(
        f'    <char id="{code}" x="{x}" y="{y}" width="{w}" height="{h}" '
        f'xoffset="0" yoffset="0" xadvance="{adv}" yadvance="{h}"/>'
        for code, x, y, w, h, adv in entries
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<font>
  <info face="gold" size="{CELL_H}" bold="0" italic="0" charset="" unicode="" stretchH="{CELL_H}" smooth="1" aa="1" padding="0,0,0,0" spacing="1,0" outline="0"/>
  <common lineHeight="{CELL_H}" base="{CELL_H}" scaleW="{atlas_w}" scaleH="{atlas_h}" pages="1" packed="0"/>
  <pages>
    <page id="0" file="mm_gold.webp"/>
  </pages>
  <chars count="{len(entries)}">
{chars_xml}
  </chars>
</font>
"""
    with open(os.path.join(FONT_DIR, "mm_gold.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"atlas {atlas_w}x{atlas_h}, {len(entries)} chars -> {FONT_DIR}")


if __name__ == "__main__":
    main()
