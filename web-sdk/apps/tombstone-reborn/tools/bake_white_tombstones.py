"""Bake dark feature cards onto the shared 300x300 wild canvas.

Fills wr_wild's card bbox (same as make_scatter_card.py) so the rounded gold
rim and alpha match every other symbol. Does NOT touch tr_scatter.png.
"""

import os
import shutil

from PIL import Image

APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GEN = os.path.normpath(
    os.path.join(os.path.expanduser("~"), ".cursor", "projects", "c-Users-Emex33-Desktop-stakez", "assets")
)

# Feature symbols + SUPER scatter only. Regular BONUS scatter stays the
# original cracked-stone card.
SPECS = [
    ("tr_feat_split.png", "tr_sp.png"),
    ("tr_feat_gunsmoke.png", "tr_gs.png"),
    ("tr_feat_tombstone.png", "tr_ts.png"),
    ("tr_feat_nudge.png", "tr_nw.png"),
    ("tr_feat_super.png", "tr_scatter_super.png"),
]


def _find(name: str) -> str:
    path = os.path.join(GEN, name)
    if os.path.isfile(path):
        return path
    raise SystemExit(f"missing generated art: {path}")


def _wild() -> Image.Image:
    path = os.path.join(APP, "static", "assets", "sprites", "mirror", "wr_wild.png")
    if not os.path.isfile(path):
        path = os.path.join(APP, "assets-src", "sprites", "mirror", "wr_wild.png")
    return Image.open(path).convert("RGBA")


def bake(wild: Image.Image, src_path: str) -> Image.Image:
    alpha = wild.getchannel("A")
    x0, y0, x1, y1 = alpha.getbbox()
    art = Image.open(src_path).convert("RGB").resize((x1 - x0, y1 - y0), Image.LANCZOS)
    canvas = Image.new("RGB", wild.size, (0, 0, 0))
    canvas.paste(art, (x0, y0))
    out = canvas.convert("RGBA")
    out.putalpha(alpha)
    return out


def write(img: Image.Image, filename: str):
    for base in ("assets-src", os.path.join("static", "assets")):
        dst = os.path.join(APP, base, "sprites", "mirror")
        os.makedirs(dst, exist_ok=True)
        path = os.path.join(dst, filename)
        img.save(path, optimize=True)
        print("wrote", path, img.size)


def main():
    wild = _wild()
    for src_name, dest_name in SPECS:
        src = _find(src_name)
        write(bake(wild, src), dest_name)
        raw_dst = os.path.join(APP, "assets-src", "sprites", "mirror", src_name)
        shutil.copy2(src, raw_dst)


if __name__ == "__main__":
    main()
