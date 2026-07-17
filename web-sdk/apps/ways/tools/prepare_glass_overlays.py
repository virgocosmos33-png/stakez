"""Convert the generated glass renders (on pure black) into translucent overlays.

Luminance becomes alpha, so the dark glass body turns see-through while the
frame, glints and cracks stay visible. Output goes to static sprites.
"""

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
SRC_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"
OUT_DIR = os.path.join(APP, "static", "assets", "sprites", "mirror")

JOBS = {
    "glass_intact_src.png": ("glass_intact.png", 1.35, 0.10),
    "glass_broken_src.png": ("glass_broken.png", 1.5, 0.06),
}

SIZE = 512

for src_name, (out_name, alpha_gain, base_alpha) in JOBS.items():
    im = Image.open(os.path.join(SRC_DIR, src_name)).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    out = Image.new("RGBA", (SIZE, SIZE))
    src_px = im.load()
    out_px = out.load()
    for y in range(SIZE):
        for x in range(SIZE):
            r, g, b = src_px[x, y]
            lum = max(r, g, b)
            # base_alpha keeps a faint glass body visible even in dark areas
            alpha = min(255, int(lum * alpha_gain + 255 * base_alpha))
            out_px[x, y] = (r, g, b, alpha)
    out.save(os.path.join(OUT_DIR, out_name))
    print(f"{src_name} -> {out_name}")
