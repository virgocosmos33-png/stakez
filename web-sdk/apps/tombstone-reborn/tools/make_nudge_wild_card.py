"""Bake the NUDGE WILD card (tr_nudge_wild.png) from the generated art.

The generation (tr_nudge_wild_card.png, painted over wr_wild.png as the style
reference) fills its whole canvas. This fits it onto the SAME 300x300 canvas
as wr_wild.png, at the same card bbox, and reuses wr_wild's alpha channel so
the rounded corners and edge feathering are pixel-identical to the plain wild.
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
        "tr_nudge_wild_card.png",
    )
)


def main():
    wild = Image.open(os.path.join(APP, "assets", "sprites", "mirror", "wr_wild.png"))
    alpha = wild.getchannel("A")
    x0, y0, x1, y1 = alpha.getbbox()

    art = Image.open(GEN).convert("RGB").resize((x1 - x0, y1 - y0), Image.LANCZOS)
    canvas = Image.new("RGB", wild.size, (0, 0, 0))
    canvas.paste(art, (x0, y0))
    out = canvas.convert("RGBA")
    out.putalpha(alpha)

    for base_dir in ("assets", os.path.join("static", "assets")):
        dst = os.path.join(APP, base_dir, "sprites", "mirror")
        if os.path.isdir(dst):
            path = os.path.join(dst, "tr_nudge_wild.png")
            out.save(path, optimize=True)
            print("wrote", path, out.size)


if __name__ == "__main__":
    main()
