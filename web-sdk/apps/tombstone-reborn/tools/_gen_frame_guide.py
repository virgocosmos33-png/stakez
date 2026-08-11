"""Render the EXACT board-frame silhouette as a generation guide.

The guide is the staircase ring band (outer = outline + BORDER, inner = the
cell outline) filled mid-grey on white, padded to a 4:3 canvas so it can be
passed to the image generator as a reference. wire_generated_frame.py undoes
the padding on the result.
"""

import os

from PIL import Image, ImageDraw

from make_board_frame_image import BORDER, MARGIN, SCALE, bounds, columns, silhouette, to_px

GEN = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
    )
)


def guide_geometry():
    cols = columns()
    outer = silhouette(cols, BORDER)
    x0, y0, x1, y1 = bounds(outer)
    x0 -= MARGIN
    y0 -= MARGIN
    x1 += MARGIN
    y1 += MARGIN
    size = (int(round((x1 - x0) * SCALE)), int(round((y1 - y0) * SCALE)))
    # pad to 4:3 (the closest generator aspect) — remember the pad for unpacking
    target_w = int(round(size[1] * 4 / 3))
    pad_x = max(0, (target_w - size[0]) // 2)
    return cols, x0, y0, size, pad_x, (size[0] + 2 * pad_x, size[1])


def main():
    cols, x0, y0, size, pad_x, canvas = guide_geometry()
    img = Image.new("RGB", canvas, (255, 255, 255))
    draw = ImageDraw.Draw(img)

    outer_px = [(x + pad_x, y) for x, y in to_px(silhouette(cols, BORDER), x0, y0)]
    inner_px = [(x + pad_x, y) for x, y in to_px(silhouette(cols, 0), x0, y0)]

    # solid wood-brown band with heavy outlines: generations adhere to a filled
    # colour region far better than to a pale grey wash (the grey guide let the
    # model redraw the whole left half of the ring off-stencil)
    draw.polygon(outer_px, fill=(101, 78, 58))
    draw.polygon(inner_px, fill=(255, 255, 255))
    draw.line(outer_px + [outer_px[0]], fill=(25, 18, 12), width=6)
    draw.line(inner_px + [inner_px[0]], fill=(25, 18, 12), width=6)

    dest = os.path.join(GEN, "tr_frame_guide.png")
    img.save(dest)
    print("wrote", dest, img.size, "| frame canvas", size, "| pad_x", pad_x)


if __name__ == "__main__":
    main()
