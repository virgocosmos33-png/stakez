"""Bake TOMBSTONE REBORN feature cards onto the shared 300x300 wild canvas.

Board specials (SG/SO/GS/DU/CF) reuse the existing bar-plaque art, fitted into
wr_wild's alpha so they drop as the same rounded card as every other symbol.
Last-reel specials (SH MARK, SS SUPERSPLIT) reuse the golden lane cards.
"""

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def _first(*paths):
    for p in paths:
        if p and os.path.isfile(p):
            return p
    return None


def _wild():
    path = _first(
        os.path.join(APP, "assets-src", "sprites", "mirror", "wr_wild.png"),
        os.path.join(APP, "static", "assets", "sprites", "mirror", "wr_wild.png"),
    )
    if not path:
        raise SystemExit("missing wr_wild.png")
    return Image.open(path).convert("RGBA")


def _plaque(name):
    return _first(
        os.path.join(APP, "assets-src", "sprites", "tombstone", name),
        os.path.join(APP, "static", "assets", "sprites", "tombstone", name),
    )


def _fit_into(art: Image.Image, box: tuple[int, int, int, int], canvas_size):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    src = art.convert("RGBA")
    scale = min(bw / src.width, bh / src.height)
    nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
    src = src.resize((nw, nh), Image.LANCZOS)
    layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    layer.paste(src, (x0 + (bw - nw) // 2, y0 + (bh - nh) // 2), src)
    return layer


def _label_card(wild: Image.Image, box, title: str, subtitle: str, ink=(240, 214, 150)):
    """Fallback when plaque art is missing: stone card + western wordmark."""
    x0, y0, x1, y1 = box
    canvas = Image.new("RGBA", wild.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((x0, y0, x1, y1), fill=(28, 24, 20, 255))
    try:
        font_big = ImageFont.truetype("arialbd.ttf", 42)
        font_sm = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font_big = ImageFont.load_default()
        font_sm = font_big
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    draw.text((cx, cy - 12), title, fill=ink, font=font_big, anchor="mm")
    draw.text((cx, cy + 28), subtitle, fill=(180, 160, 120), font=font_sm, anchor="mm")
    return canvas.filter(ImageFilter.SMOOTH)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except OSError:
        return ImageFont.load_default()


def stamp_band(art: Image.Image, text: str, y0: float, y1: float) -> Image.Image:
    """Paint a thin word band and stamp gold caps. Does not wipe half the card."""
    out = art.convert("RGBA")
    draw = ImageDraw.Draw(out)
    w, h = out.size
    top, bot = int(h * y0), int(h * y1)
    draw.rectangle((int(w * 0.08), top, int(w * 0.92), bot), fill=(22, 18, 14, 230))
    draw.text(
        (w / 2, (top + bot) / 2),
        text,
        fill=(240, 214, 150, 255),
        font=_font(max(22, (bot - top) * 2 // 3)),
        anchor="mm",
    )
    return out


def bake(
    wild: Image.Image,
    art_path: str | None,
    fallback_title: str,
    fallback_sub: str,
    cover_banner: str | None = None,
    band: tuple[float, float] | None = None,
):
    alpha = wild.getchannel("A")
    box = alpha.getbbox()
    x0, y0, x1, y1 = box
    if art_path:
        art = Image.open(art_path).convert("RGBA")
        if cover_banner:
            y0b, y1b = band if band else (0.78, 0.94)
            art = stamp_band(art, cover_banner, y0b, y1b)
        art = art.convert("RGB").resize((x1 - x0, y1 - y0), Image.LANCZOS)
        canvas = Image.new("RGB", wild.size, (0, 0, 0))
        canvas.paste(art, (x0, y0))
        out = canvas.convert("RGBA")
    else:
        layer = _label_card(wild, box, fallback_title, fallback_sub)
        out = Image.new("RGBA", wild.size, (0, 0, 0, 0))
        out.paste(layer, (0, 0), layer)
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
    specs = [
        ("tr_sp.png", _first(os.path.join(APP, "assets-src", "sprites", "mirror", "tr_feat_split.png")), "SPLIT", "WAYS", None),
        ("tr_gs.png", _first(os.path.join(APP, "assets-src", "sprites", "mirror", "tr_feat_gunsmoke.png")), "GUNSMOKE", "", None),
        ("tr_ts.png", _first(os.path.join(APP, "assets-src", "sprites", "mirror", "tr_feat_tombstone.png")), "TOMBSTONE", "", None),
        ("tr_nw.png", _first(os.path.join(APP, "assets-src", "sprites", "mirror", "tr_feat_nudge.png")), "NUDGE", "WAYS", None),
        # MARK = shooter, crossed-gun plaque. SUPERSPLIT = the knife SPLIT card.
        ("tr_sh.png", _plaque("lane_gold_supersplit.webp"), "MARK", "SHOOT", "MARK"),
        (
            "tr_ss.png",
            _first(
                os.path.join(APP, "static", "assets", "sprites", "mirror", "tr_sp.png"),
                os.path.join(APP, "assets-src", "sprites", "mirror", "tr_sp.png"),
            ),
            "SUPER SPLIT",
            "",
            "SUPER SPLIT",
        ),
    ]
    for filename, src, title, sub, banner in specs:
        band = (0.40, 0.62) if filename == "tr_ss.png" else None
        write(bake(wild, src, title, sub, cover_banner=banner, band=band), filename)


if __name__ == "__main__":
    main()
