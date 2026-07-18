"""Replace the SD2 gold coin flipbook with a spinning haunted-mirror gem.

Reads the existing SD2_Coin.json frame layout (12 frames of a Y-axis spin,
frame widths already encode the squash) and paints a faceted violet crystal
into every frame slot of SD2_Coin.png. The JSON is untouched, so WinCoins and
the particle emitters keep working as-is.

Run:  python tools/make_gem_flipbook.py
"""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

APP = Path(__file__).resolve().parents[1]
COIN_DIR = APP / "static" / "assets" / "sprites" / "coin"
BACKUP = APP / "assets-backup" / "gem_flipbook"

SUPER = 2

LILAC = (232, 218, 255)
VIOLET = (168, 128, 240)
DEEP = (96, 62, 168)
BACK_TINT = 0.72  # frames 7-12 show the darker back face


def lerp(a, b, f):
    return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))


def draw_gem(width: int, height: int, back: bool) -> Image.Image:
    """Elongated faceted crystal filling a width x height box (pre-squash)."""
    s = SUPER
    w, h = width * s, height * s
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    inset_x = w * 0.07
    inset_y = h * 0.05
    gw = w - inset_x * 2
    gh = h - inset_y * 2

    def P(fx: float, fy: float) -> tuple[float, float]:
        return (inset_x + gw * fx, inset_y + gh * fy)

    # marquise-cut silhouette: sharp top and bottom tips, wide girdle
    top = P(0.5, 0.0)
    upper_r = P(0.94, 0.3)
    lower_r = P(0.82, 0.74)
    bottom = P(0.5, 1.0)
    lower_l = P(0.18, 0.74)
    upper_l = P(0.06, 0.3)
    outline = [top, upper_r, lower_r, bottom, lower_l, upper_l]

    dim = BACK_TINT if back else 1.0

    # violet glow halo
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).polygon(outline, fill=(150, 105, 235, int(210 * dim)))
    glow = glow.filter(ImageFilter.GaussianBlur(w * 0.055 + 2))
    img.alpha_composite(glow)

    # facet triangles around a raised center ridge (two ridge points)
    ridge_hi = P(0.5, 0.3)
    ridge_lo = P(0.5, 0.7)
    facets = [
        # crown
        ([top, upper_r, ridge_hi], 1.18),
        ([top, upper_l, ridge_hi], 0.92),
        # girdle band
        ([upper_r, lower_r, ridge_lo, ridge_hi], 1.0),
        ([upper_l, lower_l, ridge_lo, ridge_hi], 0.72),
        # pavilion
        ([bottom, lower_r, ridge_lo], 0.85),
        ([bottom, lower_l, ridge_lo], 0.6),
    ]
    draw = ImageDraw.Draw(img)
    for poly, brightness in facets:
        base_top = lerp(LILAC, VIOLET, 0.25)
        base_bottom = DEEP
        mid_y = sum(p[1] for p in poly) / len(poly) / h
        color = lerp(base_top, base_bottom, mid_y)
        color = tuple(min(int(c * brightness * dim), 255) for c in color)
        draw.polygon(poly, fill=(*color, 255))

    # facet edges + rim
    edge = (255, 255, 255, int(140 * dim))
    for poly, _ in facets:
        draw.line([*poly, poly[0]], fill=edge, width=max(1, s))
    draw.line([*outline, outline[0]], fill=(255, 255, 255, int(220 * dim)), width=max(2, s))

    # specular sparkle on the crown
    if not back:
        sx, sy = P(0.38, 0.18)
        r = w * 0.05
        for angle in range(0, 360, 45):
            ex = sx + math.cos(math.radians(angle)) * r * (2 if angle % 90 == 0 else 0.9)
            ey = sy + math.sin(math.radians(angle)) * r * (2 if angle % 90 == 0 else 0.9)
            draw.line([(sx, sy), (ex, ey)], fill=(255, 255, 255, 230), width=max(1, s))
        draw.circle((sx, sy), r * 0.45, fill=(255, 255, 255, 250))

    return img.resize((width, height), Image.LANCZOS)


def main() -> None:
    meta = json.loads((COIN_DIR / "SD2_Coin.json").read_text())
    sheet_size = meta["meta"]["size"]

    BACKUP.mkdir(parents=True, exist_ok=True)
    if not (BACKUP / "SD2_Coin.png").exists():
        shutil.copy2(COIN_DIR / "SD2_Coin.png", BACKUP / "SD2_Coin.png")

    sheet = Image.new("RGBA", (sheet_size["w"], sheet_size["h"]), (0, 0, 0, 0))

    for name, frame_data in meta["frames"].items():
        frame = frame_data["frame"]
        rotated = frame_data["rotated"]
        index = int(name.split(".")[0])
        back = index > 6
        gem = draw_gem(frame["w"], frame["h"], back)
        if rotated:
            # rotated frames are stored 90 degrees clockwise in the sheet
            gem = gem.transpose(Image.ROTATE_270)
        sheet.alpha_composite(gem, (frame["x"], frame["y"]))
        print(f"[gem] frame {name} {'back' if back else 'front'} {frame['w']}x{frame['h']}")

    sheet.save(COIN_DIR / "SD2_Coin.png")
    print(f"[gem] wrote {COIN_DIR / 'SD2_Coin.png'}")


if __name__ == "__main__":
    main()
