"""Install whiteroomcharnormalmode.png as lady cutouts + bluescreens for idle I2V."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "whiteroomcharnormalmode.png"
APP = Path(__file__).resolve().parents[1]
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
MASTERS = APP / "assets-raw" / "lady_masters"
VIDEO = APP / "assets-raw" / "lady_video"

BLUE = (0, 0, 255)
CANVAS = (720, 1280)
FIG_H_FRAC = 0.9


def tight_crop(im: Image.Image, pad: int = 8) -> Image.Image:
    arr = np.array(im.convert("RGBA"))
    alpha = arr[..., 3]
    ys, xs = np.where(alpha > 8)
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    y0, x0 = max(0, y0 - pad), max(0, x0 - pad)
    y1 = min(arr.shape[0] - 1, y1 + pad)
    x1 = min(arr.shape[1] - 1, x1 + pad)
    return Image.fromarray(arr[y0 : y1 + 1, x0 : x1 + 1])


def make_bonus(cut: Image.Image) -> Image.Image:
    rgb = cut.convert("RGB")
    rgb = ImageEnhance.Brightness(rgb).enhance(0.82)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.18)
    rgb = ImageEnhance.Color(rgb).enhance(0.78)
    r, g, b = rgb.split()
    r = r.point(lambda v: int(v * 0.92))
    g = g.point(lambda v: int(v * 0.98))
    b = b.point(lambda v: min(255, int(v * 1.05)))
    bonus = Image.merge("RGB", (r, g, b)).convert("RGBA")
    bonus.putalpha(cut.split()[-1])
    return bonus


def build_bluescreen(fig: Image.Image, dest: Path) -> None:
    canvas = Image.new("RGBA", CANVAS, BLUE + (255,))
    target_h = int(CANVAS[1] * FIG_H_FRAC)
    scale = target_h / fig.height
    target_w = int(fig.width * scale)
    fig2 = fig.resize((target_w, target_h), Image.LANCZOS)
    x = (CANVAS[0] - target_w) // 2
    y = (CANVAS[1] - target_h) // 2
    canvas.alpha_composite(fig2, (x, y))
    canvas.convert("RGB").save(dest, "PNG")
    print(f"[blue] {dest.name} {canvas.size} {dest.stat().st_size}", flush=True)


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"missing source: {SRC}")
    for p in (STATIC, VITE, MASTERS, VIDEO):
        p.mkdir(parents=True, exist_ok=True)

    # Source art faces RIGHT; host sits on the RIGHT of the board and must
    # face LEFT toward the reels — flip once at install.
    cut = tight_crop(Image.open(SRC)).transpose(Image.FLIP_LEFT_RIGHT)
    print(f"[cut] {cut.size} (flipped → faces LEFT / toward reels)", flush=True)
    bonus = make_bonus(cut)

    for dest in (
        STATIC / "lady_character.png",
        VITE / "lady_character.png",
        MASTERS / "white_room_character_base.png",
    ):
        cut.save(dest, "PNG")
        print(f"[wrote] {dest}", flush=True)

    for dest in (
        STATIC / "lady_bonus.png",
        VITE / "lady_bonus.png",
        MASTERS / "white_room_character_bonus.png",
    ):
        bonus.save(dest, "PNG")
        print(f"[wrote] {dest}", flush=True)

    build_bluescreen(cut, VIDEO / "lady_idle_base_blue.png")
    build_bluescreen(bonus, VIDEO / "lady_idle_bonus_blue.png")
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
