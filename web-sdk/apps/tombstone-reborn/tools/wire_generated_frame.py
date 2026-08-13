"""Wire the GENERATED board frame (tr_frame_generated.png).

The frame is painted by the image model over the exact staircase stencil from
_gen_frame_guide.py (grey band on white, padded to 4:3). This script undoes the
padding, keys the pure-white ground to transparency, force-clears the cell
interior (so no stray pixel ever sits over a symbol), and writes
board_frame.png at the same anchor box the guide used (BORDER + MARGIN canvas).

BoardPlate.svelte's frameBox pad MUST equal BORDER + MARGIN.
"""

import os

import numpy as np
from PIL import Image, ImageDraw

from _gen_frame_guide import GEN, guide_geometry
from make_board_frame_image import APP, silhouette, to_px

# white ground -> alpha: opaque below LO, transparent above HI (lum feather).
# The wood is grey-brown (< 210) and the paper scraps are cream (~235 max), so
# a high band keeps them while dropping the white ground.
LO, HI = 242, 252


def main():
    cols, x0, y0, size, pad_x, canvas = guide_geometry()

    src = Image.open(os.path.join(GEN, "tr_frame_generated.png")).convert("RGB")
    src = src.resize(canvas, Image.LANCZOS)
    src = src.crop((pad_x, 0, pad_x + size[0], size[1]))

    arr = np.array(src, float)
    lum = arr.mean(axis=2)
    alpha = np.clip((HI - lum) / (HI - LO), 0, 1) * 255

    # guarantee the play area: clear everything more than a whisker inside the
    # cell outline, whatever the paint did (plank lips may keep ~4 units)
    inner = Image.new("L", size, 0)
    ImageDraw.Draw(inner).polygon(to_px(silhouette(cols, -4), x0, y0), fill=255)
    alpha = np.where(np.array(inner) > 0, 0, alpha)

    out = np.dstack([arr.astype(np.uint8), alpha.astype(np.uint8)])
    img = Image.fromarray(out, "RGBA")

    for base_dir in ("assets", os.path.join("static", "assets")):
        dst = os.path.join(APP, base_dir, "sprites", "board")
        if os.path.isdir(dst):
            path = os.path.join(dst, "board_frame.png")
            img.save(path, optimize=True)
            print("wrote", path, img.size)
    print("anchor pad (BORDER+MARGIN) must be in BoardPlate:", end=" ")
    from make_board_frame_image import BORDER, MARGIN

    print(BORDER + MARGIN)


if __name__ == "__main__":
    main()
