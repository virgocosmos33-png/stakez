"""Process the 5 generated bullet-crack variants into clean white-on-transparent
decals: bullet_crack_1..5.png.

Alpha is luminance * existing-alpha so:
  - bright cracks  -> opaque white
  - dark centre    -> transparent hole
  - any already-transparent background (light-checker generations) stays gone,
    instead of turning the pale paper into a white haze.
"""
import os

from PIL import Image, ImageChops

GEN = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
    )
)
APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


# Some generations baked the "transparency" checkerboard in as real mid-grey
# pixels. Key ONLY the near-white crack lines: mid-grey (checker / paper / soft
# shadow) drops to fully transparent, pure-white lines stay opaque, with a short
# feather on the edges. NO autocontrast (that stretched the grey checker up to
# white and turned it into an opaque square).
LO, HI = 225, 252


def _curve(v: int) -> int:
    if v <= LO:
        return 0
    if v >= HI:
        return 255
    return int((v - LO) / (HI - LO) * 255)


def process(src_path: str) -> Image.Image:
    img = Image.open(src_path).convert("RGBA")
    existing = img.getchannel("A")
    lum = img.convert("L")
    mask = lum.point(_curve)
    # respect any genuine transparency too, then floor faint noise to 0
    mask = ImageChops.multiply(mask, existing)
    mask = mask.point(lambda v: 0 if v < 12 else v)
    out = Image.new("RGBA", img.size, (255, 255, 255, 0))
    out.putalpha(mask)
    bbox = mask.getbbox()
    if bbox:
        out = out.crop(bbox)
        cw, ch = out.size
        side = max(cw, ch)
        sq = Image.new("RGBA", (side, side), (255, 255, 255, 0))
        sq.paste(out, ((side - cw) // 2, (side - ch) // 2), out)
        out = sq
    return out


for i in range(1, 6):
    src = os.path.join(GEN, f"tr_crack_{i}.png")
    if not os.path.isfile(src):
        print("missing", src)
        continue
    decal = process(src)
    for base in ("assets", os.path.join("static", "assets")):
        dst = os.path.join(APP, base, "sprites", "board")
        if os.path.isdir(dst):
            path = os.path.join(dst, f"bullet_crack_{i}.png")
            decal.save(path, optimize=True)
            print("wrote", path, decal.size)
print("done")
