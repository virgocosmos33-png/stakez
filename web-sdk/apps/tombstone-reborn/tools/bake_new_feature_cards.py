"""Bake the new SPLIT / TOMBSTONE / NUDGE plaques onto the wild card,
and key the nudge-fire plume to transparent.

Sources live in the Cursor generated-assets folder (or --src). Writes both
assets-src and static/assets trees.
"""

import os
import sys

from PIL import Image

APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GEN = os.path.normpath(
    os.path.join(os.path.expanduser("~"), ".cursor", "projects", "c-Users-Emex33-Desktop-stakez", "assets")
)


def _first(*paths):
    for path in paths:
        if path and os.path.isfile(path):
            return path
    return None


def _wild():
    path = _first(
        os.path.join(APP, "assets-src", "sprites", "mirror", "wr_wild.png"),
        os.path.join(APP, "static", "assets", "sprites", "mirror", "wr_wild.png"),
    )
    if not path:
        raise SystemExit("missing wr_wild.png")
    return Image.open(path).convert("RGBA")


def _fit_into(art: Image.Image, box, canvas_size):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    src = art.convert("RGBA")
    scale = min(bw / src.width, bh / src.height)
    nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
    src = src.resize((nw, nh), Image.LANCZOS)
    layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    layer.paste(src, (x0 + (bw - nw) // 2, y0 + (bh - nh) // 2), src)
    return layer


def write_both(img: Image.Image, rel_dir: str, filename: str):
    for base in ("assets-src", os.path.join("static", "assets")):
        dst = os.path.join(APP, base, rel_dir)
        os.makedirs(dst, exist_ok=True)
        path = os.path.join(dst, filename)
        img.save(path, optimize=True)
        print("wrote", path, img.size)


def bake_plaque(wild: Image.Image, src_path: str, filename: str):
    alpha = wild.getchannel("A")
    box = alpha.getbbox()
    art = Image.open(src_path).convert("RGBA")
    layer = _fit_into(art, box, wild.size)
    out = Image.new("RGBA", wild.size, (0, 0, 0, 0))
    out.paste(layer, (0, 0), layer)
    out.putalpha(alpha)
    write_both(out, os.path.join("sprites", "mirror"), filename)
    # keep the raw plaque too
    plaque = Image.open(src_path).convert("RGBA")
    write_both(plaque, os.path.join("sprites", "tombstone"), os.path.basename(src_path))


def key_fire(src_path: str):
    img = Image.open(src_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            luma = (r * 3 + g * 6 + b) // 10
            # near-black field → transparent; keep flame, sparks, smoke
            if luma < 18 and r < 30 and g < 24:
                pixels[x, y] = (r, g, b, 0)
            elif luma < 36:
                pixels[x, y] = (r, g, b, min(a, int(luma * 6)))
    write_both(img, os.path.join("sprites", "fx"), "fx_nudge_fire.png")


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else GEN
    wild = _wild()
    specs = [
        ("bar_plaque_split.png", "tr_sp.png"),
        ("bar_plaque_tombstone.png", "tr_ts.png"),
        ("bar_plaque_nudge.png", "tr_nw.png"),
    ]
    for plaque, card in specs:
        path = os.path.join(src, plaque)
        if not os.path.isfile(path):
            raise SystemExit(f"missing {path}")
        bake_plaque(wild, path, card)
    fire = os.path.join(src, "fx_nudge_fire.png")
    if not os.path.isfile(fire):
        raise SystemExit(f"missing {fire}")
    key_fire(fire)


if __name__ == "__main__":
    main()
