"""Bake the SCATTER card (tr_scatter.png) from the generated art.

Same pipeline as make_nudge_wild_card.py: the generation (tr_scatter_card.png,
the cracked BONUS tombstone) fills its whole canvas; this fits it onto the
SAME 300x300 canvas as wr_wild.png, at the same card bbox, and reuses
wr_wild's alpha channel so the rounded corners and edge feathering are
pixel-identical to every other card.
"""

import os

from PIL import Image

APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GEN = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
        "tr_scatter_card.png",
    )
)


def main():
    wild = Image.open(os.path.join(APP, "assets-src", "sprites", "mirror", "wr_wild.png"))
    alpha = wild.getchannel("A")
    x0, y0, x1, y1 = alpha.getbbox()

    art = Image.open(GEN).convert("RGB").resize((x1 - x0, y1 - y0), Image.LANCZOS)
    canvas = Image.new("RGB", wild.size, (0, 0, 0))
    canvas.paste(art, (x0, y0))
    out = canvas.convert("RGBA")
    out.putalpha(alpha)

    for base_dir in ("assets-src", os.path.join("static", "assets")):
        dst = os.path.join(APP, base_dir, "sprites", "mirror")
        if os.path.isdir(dst):
            path = os.path.join(dst, "tr_scatter.png")
            out.save(path, optimize=True)
            print("wrote", path, out.size)


if __name__ == "__main__":
    main()
