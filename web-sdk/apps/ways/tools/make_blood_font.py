"""Bake a dripping-blood bitmap font atlas that replaces the gold font.

Renders the same charset as the original mm_gold atlas using Nosifer
(a horror dripping typeface), colored with a blood gradient + dark rim,
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
NOSIFER = os.path.join(HERE, "Nosifer-Regular.ttf")
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


def pick_size(font_path: str, chars: str, target_h: int) -> ImageFont.FreeTypeFont:
    """Largest size whose tallest glyph (ascent->drip bottom) fits target_h."""
    size = target_h
    while size > 8:
        font = ImageFont.truetype(font_path, size)
        ascent, descent = font.getmetrics()
        if ascent + descent <= target_h:
            return font
        size -= 1
    return ImageFont.truetype(font_path, 8)


def render_glyph(char: str, font: ImageFont.FreeTypeFont, cell_h: int) -> Image.Image:
    """Render one glyph at supersampled resolution, blood styled, baseline-aligned."""
    s = SUPER
    big = font.font_variant(size=font.size * s)
    ascent, descent = big.getmetrics()
    pad = 14 * s
    bbox = big.getbbox(char)
    width = max(bbox[2] - bbox[0], 6 * s) + pad * 2

    canvas = Image.new("L", (width, cell_h * s + pad * 2), 0)
    draw = ImageDraw.Draw(canvas)
    # baseline sits so ascent+descent are centered in the cell
    top = (cell_h * s - (ascent + descent)) // 2 + pad
    draw.text((pad - bbox[0], top), char, font=big, fill=255)

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

    # downsample to target cell height, keep full cell (baseline consistent)
    cell = layered.crop((0, pad, layered.width, pad + cell_h * s))
    cell = cell.resize((max(cell.width // s, 1), cell_h), Image.LANCZOS)

    # trim horizontal whitespace only
    alpha_bbox = cell.getbbox()
    if alpha_bbox:
        cell = cell.crop((alpha_bbox[0], 0, alpha_bbox[2], cell_h))
    return cell


def main() -> None:
    ids = charset()
    nosifer = pick_size(NOSIFER, "", CELL_H - 6)
    fallback = pick_size(FALLBACK, "", CELL_H - 14)
    nosifer_cmap = set()
    from fontTools.ttLib import TTFont

    nosifer_cmap = set(TTFont(NOSIFER).getBestCmap().keys())

    glyphs: dict[int, Image.Image] = {}
    for code in ids:
        char = chr(code)
        if code == 32:
            continue
        font = nosifer if code in nosifer_cmap else fallback
        glyphs[code] = render_glyph(char, font, CELL_H)
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
