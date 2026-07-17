"""Prepare the generated Madam Mirror art for the frontend.

- Full-bleed images (backgrounds, intro panels, loading art) are copied as
  lossy webp into static/assets/sprites/mirror/.
- Cut-out images (logo, ways counter panel) get the baked checkerboard keyed
  out via border flood-fill, are trimmed, and saved as PNG with alpha.

Run:  python tools/prepare_art.py
"""

import os
from collections import deque

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "mirror"))
ICON_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"

FULL_BLEED = {
    "mirror_bg_base_landscape.png": "bg_base.webp",
    "mirror_bg_base_portrait.png": "bg_base_portrait.webp",
    "mirror_bg_freespin_landscape.png": "bg_freespin.webp",
    "mirror_intro_panel_seance.png": "intro_seance.webp",
    "mirror_intro_panel_otherside.png": "intro_otherside.webp",
    "mirror_intro_panel_bloodmoon.png": "intro_bloodmoon.webp",
    "mirror_loading_screen.png": "loading.webp",
    "mirror_buybutton_seance.png": "buy_seance.webp",
    "mirror_buybutton_otherside.png": "buy_otherside.webp",
    "mirror_buybutton_bloodmoon.png": "buy_bloodmoon.webp",
}

KEYED = {
    "mirror_logo.png": "logo.png",
    "mirror_ways_counter_panel.png": "ways_panel.png",
    "mirror_reels_frame.png": "mirror_frame.png",
}


def is_background(px):
    r, g, b = px[:3]
    lo, hi = min(r, g, b), max(r, g, b)
    return lo >= 205 and (hi - lo) <= 18


def key_out_background(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    background = bytearray(w * h)

    queue = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_background(px[x, y]) and not background[y * w + x]:
                background[y * w + x] = 1
                queue.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_background(px[x, y]) and not background[y * w + x]:
                background[y * w + x] = 1
                queue.append((x, y))

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                idx = ny * w + nx
                if not background[idx] and is_background(px[nx, ny]):
                    background[idx] = 1
                    queue.append((nx, ny))

    alpha = Image.frombytes("L", (w, h), bytes(255 if not b else 0 for b in background))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))

    out = im.convert("RGBA")
    out.putalpha(alpha)
    return out


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    for src_name, dst_name in FULL_BLEED.items():
        im = Image.open(os.path.join(ICON_DIR, src_name)).convert("RGB")
        im.save(os.path.join(OUT_DIR, dst_name), quality=82)
        print(f"{src_name} -> {dst_name} {im.size}")

    for src_name, dst_name in KEYED.items():
        im = key_out_background(Image.open(os.path.join(ICON_DIR, src_name)))
        bbox = im.getchannel("A").getbbox()
        if bbox:
            im = im.crop(bbox)
        if im.width > 1024:
            im = im.resize((1024, round(im.height * 1024 / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUT_DIR, dst_name))
        print(f"{src_name} -> {dst_name} {im.size}")
