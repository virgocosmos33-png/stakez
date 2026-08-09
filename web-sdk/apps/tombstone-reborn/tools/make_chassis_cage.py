"""Rebuild the side chassis as a thin cage sized to the card.

The old column was a machine panel: 605px of art wrapped around a 316px card,
with a hanging chain and a wide bolted rail, eating 42% of a phone screen. Even
slimmed it stayed wider than a board column, so the special cells sat about four
times further from the reels than the reels sit from each other.

This makes the side cells COLUMNS OF THE SAME GRID. The cage is one board column
pitch wide plus the same gutter the board uses between cards, and its three
openings sit on the board's row pitch — so all seven columns read as one board
rather than a board with two towers bolted to it.

Nothing here is drawn from scratch. The frame edge and the iron fill are cut from
the existing column art (chassis_side_l.png), so the material, grain and rivets
are the same ones the rest of the machine is built from.

The openings are cut a little smaller than the card that covers them, which is
how the old art worked too: LockedSlots draws a full-size symbol card over each
one, so the hole is only ever seen as the recess around its edge.

Run:  python tools/make_chassis_cage.py
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.normpath(os.path.join(HERE, "..", "assets", "sprites", "mirror"))
SRC = os.path.join(SRC_DIR, "chassis_side_l.png")

# --- geometry, in SYMBOL_SIZEs -----------------------------------------------
# These are the numbers chassisArt.ts is built from; the art is rendered to match
# rather than the other way round.
CARD_W = 0.754  # a board symbol card, = SYMBOL_CARD_W / SYMBOL_SIZE
CARD_H = 292 / 300
GUTTER = 0.046  # the gap the board leaves between two cards
ROW_PITCH = 1.0  # cells stack on the board's row pitch
SIDE_W = CARD_W + 2 * GUTTER  # 0.846 — one column pitch plus its gutter
SIDE_H = 3.588  # unchanged: leaves the cogs their seats above and below

# Opening slightly inside the card so the card always covers it
OPEN_W = CARD_W * 0.93
OPEN_H = CARD_H * 0.93
OPEN_RADIUS = 0.035  # rounded corners, matching the cards

H = 1505  # keep the source height so nothing is resampled vertically
UNIT = H / SIDE_H  # pixels per SYMBOL_SIZE
W = round(UNIT * SIDE_W)

# --- source regions ----------------------------------------------------------
# Measured off chassis_side_l.png with a coverage/luminance profile:
FRAME_STRIP = (110, 158)  # riveted outer frame edge, full height, no holes
FILL_STRIP = (425, 565)  # flat solid rail, full height, no holes


def strip(img: Image.Image, span: tuple[int, int]) -> Image.Image:
    return img.crop((span[0], 0, span[1], img.height))


def iron_fill(img: Image.Image, width: int) -> Image.Image:
    """Hole-free iron, mirror-tiled out to `width` so the tiling has no seam."""
    tile = strip(img, FILL_STRIP)
    flipped = tile.transpose(Image.FLIP_LEFT_RIGHT)
    out = Image.new("RGBA", (width, img.height), (0, 0, 0, 0))
    x = 0
    i = 0
    while x < width:
        out.paste(tile if i % 2 == 0 else flipped, (x, 0))
        x += tile.width
        i += 1
    return out.crop((0, 0, width, img.height))


def punch(plate: Image.Image, boxes: list[tuple[float, float, float, float]]) -> Image.Image:
    """Cut the openings and work a recess around each one.

    The bevel is a darkened band just inside the cut plus a lighter lip outside
    it, so the hole reads as machined through thick plate rather than a sticker.
    """
    hole = Image.new("L", plate.size, 0)
    draw = ImageDraw.Draw(hole)
    radius = round(OPEN_RADIUS * UNIT)
    for box in boxes:
        draw.rounded_rectangle(box, radius=radius, fill=255)

    inner = hole.filter(ImageFilter.GaussianBlur(radius * 0.9))
    px = np.asarray(plate, dtype=np.float32) / 255.0
    edge = np.asarray(inner, dtype=np.float32) / 255.0
    cut = np.asarray(hole, dtype=np.float32) / 255.0

    # darken toward the cut, then drop the hole itself out of the alpha
    shade = 1.0 - 0.55 * np.clip(edge - cut, 0.0, 1.0)[..., None]
    px[..., :3] = np.clip(px[..., :3] * shade, 0.0, 1.0)
    px[..., 3] = np.clip(px[..., 3] * (1.0 - cut), 0.0, 1.0)
    return Image.fromarray((px * 255).astype(np.uint8), "RGBA")


if __name__ == "__main__":
    src = Image.open(SRC).convert("RGBA")

    frame = strip(src, FRAME_STRIP)
    fill_w = W - frame.width * 2
    if fill_w <= 0:
        raise SystemExit(f"frame strips ({frame.width * 2}px) do not fit a {W}px cage")

    # symmetric frame: the same riveted edge down both sides, so it reads as a
    # cage rather than a panel with a machined face on one side
    plate = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    plate.paste(frame, (0, 0))
    plate.paste(iron_fill(src, fill_w), (frame.width, 0))
    plate.paste(frame.transpose(Image.FLIP_LEFT_RIGHT), (frame.width + fill_w, 0))

    ow, oh = OPEN_W * UNIT, OPEN_H * UNIT
    boxes = []
    for j in (-1, 0, 1):
        cy = H / 2 + j * ROW_PITCH * UNIT
        boxes.append((W / 2 - ow / 2, cy - oh / 2, W / 2 + ow / 2, cy + oh / 2))

    left = punch(plate, boxes)
    left.save(os.path.join(SRC_DIR, "chassis_side_l_cage.png"))
    left.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(SRC_DIR, "chassis_side_r_cage.png"))

    print(f"cage {W} x {H}  ({SIDE_W:.3f} x {SIDE_H:.3f} symbol sizes)")
    print(f"frame edge {frame.width}px per side, iron fill {fill_w}px")
    print()
    pitch = ROW_PITCH / SIDE_H
    print("chassisArt.ts ART.side:")
    print(f"    w: {W},")
    print(f"    h: {H},")
    print("    cxLeft: 0.5,")
    print("    cxRight: 0.5,")
    print(f"    cy: [{0.5 - pitch:.5f}, 0.5, {0.5 + pitch:.5f}],")
    print(f"    openW: {OPEN_W / SIDE_W:.5f},")
    print(f"    openH: {OPEN_H / SIDE_H:.5f},")
