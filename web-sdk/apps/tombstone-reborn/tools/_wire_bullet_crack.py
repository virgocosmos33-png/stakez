"""Turn the generated bullet-hole art into a clean white-on-transparent decal.

The generator leaves a dark cast over the whole frame; we rebuild the alpha from
luminance (bright cracks -> opaque, dark background + centre hole -> transparent)
and force the RGB to pure white so it reads as shattered glass over any board.
"""
import os

from PIL import Image, ImageOps

SRC = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
        "tr_bullet_crack.png",
    )
)
APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

img = Image.open(SRC).convert("RGBA")

# alpha from luminance, gently contrasted so faint background noise drops out
lum = ImageOps.autocontrast(img.convert("L"), cutoff=1)
# hard floor: anything dim becomes fully transparent (kills the grey cast)
alpha = lum.point(lambda v: 0 if v < 28 else v)

white = Image.new("RGBA", img.size, (255, 255, 255, 0))
white.putalpha(alpha)

# trim to the cracked content so the decal scales predictably from its centre
bbox = alpha.getbbox()
if bbox:
    white = white.crop(bbox)
    # re-square around the hole so anchor 0.5 stays on the impact point
    w, h = white.size
    side = max(w, h)
    sq = Image.new("RGBA", (side, side), (255, 255, 255, 0))
    sq.paste(white, ((side - w) // 2, (side - h) // 2), white)
    white = sq

for base in ("assets", os.path.join("static", "assets")):
    dst = os.path.join(APP, base, "sprites", "board")
    if os.path.isdir(dst):
        path = os.path.join(dst, "bullet_crack.png")
        white.save(path, optimize=True)
        print("wrote", path, white.size)
print("done")
