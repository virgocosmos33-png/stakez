"""Diagnose the headless-lady bug: crop the packed atlas region + source and
report where opaque content actually sits (top-to-bottom alpha profile)."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "spines", "lady"))
SCENE_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "scene"))
SHOTS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "qa-shots", "lady"))
os.makedirs(SHOTS, exist_ok=True)


def alpha_profile(img, label):
    w, h = img.size
    a = img.split()[-1]
    px = a.load()
    print(f"\n== {label} ({w}x{h}) ==")
    bands = 20
    for b in range(bands):
        y0 = b * h // bands
        y1 = (b + 1) * h // bands
        cnt = 0
        tot = 0
        for y in range(y0, y1, max(1, (y1 - y0) // 8)):
            for x in range(0, w, max(1, w // 40)):
                tot += 1
                if px[x, y] > 20:
                    cnt += 1
        frac = cnt / max(1, tot)
        bar = "#" * int(frac * 40)
        print(f"  y {y0:4d}-{y1:4d}  {frac*100:5.1f}%  {bar}")
    bbox = a.getbbox()
    print(f"  alpha bbox: {bbox}")


page = Image.open(os.path.join(OUT_DIR, "lady.png")).convert("RGBA")
print("atlas page size", page.size)
# lady_base bounds 2,2,614,1000
base = page.crop((2, 2, 2 + 614, 2 + 1000))
base.save(os.path.join(SHOTS, "atlas_base_crop.png"))
alpha_profile(base, "atlas lady_base crop")

src = Image.open(os.path.join(SCENE_DIR, "lady_character.png")).convert("RGBA")
alpha_profile(src, "source lady_character.png")
