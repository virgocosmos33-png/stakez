"""Pack Kenney whitePuff00-24 into a dusty gunsmoke flipbook for the pistol muzzle."""

import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
HAUL = os.path.join(APP, "assets-raw", "kenney", "muzzle-smoke")
OUT_NAME = "muzzle_smoke"
CELL = 128
COLS = 5
ROWS = 5

# dusty western gunsmoke (luminance-mapped, keep source alpha)
SMOKE_RGB = (196, 178, 148)  # bone-dust / spent powder

DESTS = [
    os.path.join(APP, "static", "assets", "sprites", "fx"),
    os.path.join(APP, "assets-src", "assets", "sprites", "fx"),
    os.path.join(APP, "assets", "sprites", "fx"),
]


def dusty(im: Image.Image) -> Image.Image:
    arr = np.array(im.convert("RGBA"), dtype=np.float32)
    lum = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255.0
    boost = np.clip(lum * 1.15, 0.0, 1.0)
    r, g, b = SMOKE_RGB
    out = np.empty_like(arr)
    out[:, :, 0] = np.clip(r * boost, 0, 255)
    out[:, :, 1] = np.clip(g * boost, 0, 255)
    out[:, :, 2] = np.clip(b * boost, 0, 255)
    out[:, :, 3] = arr[:, :, 3]
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def main() -> None:
    frames_meta = {}
    atlas = Image.new("RGBA", (COLS * CELL, ROWS * CELL), (0, 0, 0, 0))
    for i in range(25):
        src_path = os.path.join(HAUL, f"whitePuff{i:02d}.png")
        im = dusty(Image.open(src_path))
        im.thumbnail((CELL, CELL), Image.LANCZOS)
        tile = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
        ox = (CELL - im.width) // 2
        oy = (CELL - im.height) // 2
        tile.paste(im, (ox, oy), im)
        col, row = i % COLS, i // COLS
        x, y = col * CELL, row * CELL
        atlas.paste(tile, (x, y), tile)
        name = f"puff_{i:02d}.png"
        frames_meta[name] = {
            "frame": {"x": x, "y": y, "w": CELL, "h": CELL},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": CELL, "h": CELL},
            "sourceSize": {"w": CELL, "h": CELL},
        }

    sheet = {
        "frames": frames_meta,
        "meta": {
            "app": "tools/make_muzzle_smoke_atlas.py",
            "image": f"{OUT_NAME}.png",
            "format": "RGBA8888",
            "size": {"w": COLS * CELL, "h": ROWS * CELL},
            "scale": "1",
        },
    }

    for dest in DESTS:
        os.makedirs(dest, exist_ok=True)
        atlas.save(os.path.join(dest, f"{OUT_NAME}.png"), "PNG")
        with open(os.path.join(dest, f"{OUT_NAME}.json"), "w", encoding="utf-8") as f:
            json.dump(sheet, f, indent=1)
        print(f"wrote {dest}")


if __name__ == "__main__":
    main()
