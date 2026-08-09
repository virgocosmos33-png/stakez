"""Bake the artwork for the BONUS BUY menu cards.

Every card in that menu should answer "what do I get for this money?" in one
glance. The scatter buys now show the SCATTERS THEMSELVES — the same word cards
that land on the reels, three of them for THE INTAKE, four for HER SIDE, five for
WHITEOUT — so the price is attached to a picture of the thing being bought.

The rest of the menu was still wearing Madam Mirror's art: ALL SPECIALS showed
that game's gold emblem, and the cell-count pictures were off by one against the
mode they were attached to. The cell cards are rebuilt here from the single lit
hatch (buy_feature1.webp) so a count is always drawn as that many hatches.

Outputs, into assets/sprites/mirror/:
  buy_scatter_1.webp   ante          one scatter
  buy_scatter_3.webp   THE INTAKE    three
  buy_scatter_4.webp   HER SIDE      four
  buy_scatter_5.webp   WHITEOUT      five
  buy_cells_9.webp     ALL BARS      nine open hatches
  buy_specials_9.webp  ALL SPECIALS  nine hatches, each holding a special card

Run:  python tools/make_buy_cards.py
"""

import os

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, "..", "assets", "sprites", "mirror"))

CANVAS = 768
HATCH = os.path.join(ART, "buy_feature1.webp")

# Where the glass sits inside the hatch art, as fractions of the tile. A special
# card is pasted into this window so it reads as sealed behind the glass.
GLASS = (0.17, 0.21, 0.84, 0.83)

SPECIALS = ["wr_split.png", "wr_clone.png", "wr_stretch.png", "wr_wild_expand.png"]

# (centre x, centre y, degrees) per card, as fractions of the canvas, plus the
# card size. Tossed rather than aligned — a neat grid of scatters reads as a
# paytable, and this is meant to read as a handful of them landing.
FANS: dict[int, tuple[float, list[tuple[float, float, float]]]] = {
    1: (0.62, [(0.50, 0.50, -4)]),
    3: (0.44, [(0.31, 0.34, -10), (0.69, 0.32, 8), (0.50, 0.69, -3)]),
    4: (0.42, [(0.31, 0.31, -8), (0.69, 0.30, 7), (0.31, 0.69, 6), (0.69, 0.70, -6)]),
    5: (
        0.36,
        [
            (0.24, 0.32, -11),
            (0.50, 0.29, 0),
            (0.76, 0.32, 11),
            (0.36, 0.71, -6),
            (0.64, 0.72, 6),
        ],
    ),
}


def shadowed(card: Image.Image, angle: float) -> Image.Image:
    """Rotate a card and give it a soft drop shadow, on its own transparent tile."""
    turned = card.rotate(angle, resample=Image.BICUBIC, expand=True)

    pad = round(card.width * 0.10)
    tile = Image.new("RGBA", (turned.width + pad * 2, turned.height + pad * 2), (0, 0, 0, 0))

    shadow = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    shadow.paste((10, 12, 14, 150), (pad, pad + round(pad * 0.35)), turned.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(pad * 0.45))

    tile.alpha_composite(shadow)
    tile.alpha_composite(turned, (pad, pad))
    return tile


def place(canvas: Image.Image, tile: Image.Image, cx: float, cy: float) -> None:
    canvas.alpha_composite(
        tile, (round(cx * CANVAS - tile.width / 2), round(cy * CANVAS - tile.height / 2))
    )


def scatter_fan(count: int) -> Image.Image:
    size_frac, spots = FANS[count]
    size = round(CANVAS * size_frac)
    out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    for i, (cx, cy, angle) in enumerate(spots):
        # 1st..5th scatter art, in the order they are named as they land
        face = Image.open(os.path.join(ART, f"wr_scatter_{i + 1}.png")).convert("RGBA")
        place(out, shadowed(face.resize((size, size), Image.LANCZOS), angle), cx, cy)
    return out


def hatch_grid(with_specials: bool) -> Image.Image:
    """Three by three lit hatches — the nine sealed cells, all open."""
    hatch = Image.open(HATCH).convert("RGBA")
    cell = round(CANVAS * 0.30)
    tile = hatch.resize((cell, cell), Image.LANCZOS)

    if with_specials:
        x0, y0, x1, y1 = (round(f * cell) for f in GLASS)
        window = (x1 - x0, y1 - y0)
        filled = []
        for i in range(9):
            face = Image.open(os.path.join(ART, SPECIALS[i % len(SPECIALS)])).convert("RGBA")
            # cover-fit the card into the glass, then dim it a touch so it sits
            # behind the pane rather than on top of it
            scale = max(window[0] / face.width, window[1] / face.height)
            face = face.resize((round(face.width * scale), round(face.height * scale)), Image.LANCZOS)
            face = face.crop(
                (
                    (face.width - window[0]) // 2,
                    (face.height - window[1]) // 2,
                    (face.width - window[0]) // 2 + window[0],
                    (face.height - window[1]) // 2 + window[1],
                )
            )
            face.putalpha(face.split()[3].point(lambda a: round(a * 0.88)))
            one = tile.copy()
            one.alpha_composite(face, (x0, y0))
            filled.append(one)
    else:
        filled = [tile] * 9

    out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    pitch = cell * 0.985  # a hair of overlap, so the nine read as one block
    # centre the whole block: three tiles span two pitches plus one tile
    origin = (CANVAS - (2 * pitch + cell)) / 2
    for i, one in enumerate(filled):
        out.alpha_composite(one, (round(origin + (i % 3) * pitch), round(origin + (i // 3) * pitch)))
    return out


def save(img: Image.Image, name: str) -> None:
    path = os.path.join(ART, name)
    img.save(path, quality=92, method=6)
    print(f"  {name}  {os.path.getsize(path) / 1024:.0f} KB")


if __name__ == "__main__":
    print("scatter fans:")
    for count in (1, 3, 4, 5):
        save(scatter_fan(count), f"buy_scatter_{count}.webp")

    print("cell grids:")
    save(hatch_grid(with_specials=False), "buy_cells_9.webp")
    save(hatch_grid(with_specials=True), "buy_specials_9.webp")
