"""Key the white background (outside + enclosed centre hole) out of the
generated root-frame borders and save them into the mirror sprite folder.

Any large connected near-white region becomes transparent; small white
highlights inside the root artwork are preserved.

Run:  python tools/prepare_root_frames.py
"""

import os
from collections import deque

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "mirror"))
ICON_DIR = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"

FRAMES = {
    "root_frame_a.png": "root_frame_a.png",
    "root_frame_b.png": "root_frame_b.png",
}

WHITE_THRESHOLD = 232
MIN_REGION = 500  # px; anything smaller stays (glints/highlights)


def is_white(px):
    r, g, b = px[:3]
    return min(r, g, b) >= WHITE_THRESHOLD


def key_white_regions(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    background = bytearray(w * h)
    visited = bytearray(w * h)

    for sy in range(h):
        for sx in range(w):
            if visited[sy * w + sx] or not is_white(px[sx, sy]):
                continue
            component = []
            queue = deque([(sx, sy)])
            visited[sy * w + sx] = 1
            while queue:
                x, y = queue.popleft()
                component.append(y * w + x)
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and not visited[ny * w + nx] and is_white(px[nx, ny]):
                        visited[ny * w + nx] = 1
                        queue.append((nx, ny))
            if len(component) >= MIN_REGION:
                for idx in component:
                    background[idx] = 1

    alpha = Image.frombytes("L", (w, h), bytes(255 if not b else 0 for b in background))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))

    out = im.convert("RGBA")
    out.putalpha(alpha)
    return out


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for src_name, dst_name in FRAMES.items():
        im = key_white_regions(Image.open(os.path.join(ICON_DIR, src_name)))
        if im.width > 700:
            im = im.resize((700, round(im.height * 700 / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUT_DIR, dst_name))
        print(f"{src_name} -> {dst_name} {im.size}")
