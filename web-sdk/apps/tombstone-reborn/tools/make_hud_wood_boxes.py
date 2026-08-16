"""Bake WAYS / MULTI / WIN boxes from HUD-only timber — not the reel-frame sheet.

Source sheets (generated, different pieces from tr_frame_planks_v2 / scraps):
  assets-raw/hud_wood/tr_hud_planks.png
  assets-raw/hud_wood/tr_hud_scraps.png

Each box is four overlapping boards around a dark well, with a scrap nailed
on every corner — same carpentry language as the staircase, different wood.

Run:  python tools/make_hud_wood_boxes.py
"""

from __future__ import annotations

import os
import random
import shutil
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
RAW = os.path.join(APP, "assets-raw", "hud_wood")
GEN_DIR = os.path.normpath(
    os.path.join(
        os.path.expanduser("~"),
        ".cursor",
        "projects",
        "c-Users-Emex33-Desktop-stakez",
        "assets",
    )
)

sys.path.insert(0, HERE)
import make_board_frame_image as bf

W, H = 640, 400
WELL = (118, 96, 522, 304)
THICK = 52
OVER = 40

BOXES = (
    ("wood_readout_ways.png", 1901),
    ("wood_readout_multi.png", 1907),
    ("wood_readout_win.png", 1913),
)


def resolve_sheet(name: str) -> str:
    raw = os.path.join(RAW, name)
    gen = os.path.join(GEN_DIR, name)
    if os.path.isfile(raw):
        return raw
    if os.path.isfile(gen):
        os.makedirs(RAW, exist_ok=True)
        shutil.copy2(gen, raw)
        return raw
    raise SystemExit(f"missing HUD wood sheet: {name}")


def lay(dst: Image.Image, shadow: Image.Image, piece: Image.Image, cx: float, cy: float) -> None:
    px = int(round(cx - piece.width / 2))
    py = int(round(cy - piece.height / 2))
    sh = Image.new("RGBA", piece.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 150), (0, 0), piece.getchannel("A"))
    shadow.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (px + 3, py + 4))
    dst.alpha_composite(piece, (px, py))


def bake(planks, scraps, seed: int) -> Image.Image:
    rng = random.Random(seed)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    l, t, r, b = WELL
    cx, cy = (l + r) / 2, (t + b) / 2
    well_w, well_h = r - l, b - t

    top = bf.plank_segment(planks, rng, well_w + 2 * OVER, int(THICK * rng.uniform(0.88, 1.12)))
    bot = bf.plank_segment(planks, rng, well_w + 2 * OVER, int(THICK * rng.uniform(0.88, 1.12)))
    left = bf.plank_segment(planks, rng, well_h + 2 * OVER, int(THICK * rng.uniform(0.88, 1.12)))
    right = bf.plank_segment(planks, rng, well_h + 2 * OVER, int(THICK * rng.uniform(0.88, 1.12)))
    left = left.transpose(Image.ROTATE_90)
    right = right.transpose(Image.ROTATE_90)
    top = top.rotate(rng.uniform(-2.2, 2.2), expand=True, resample=Image.BICUBIC)
    bot = bot.rotate(rng.uniform(-2.2, 2.2), expand=True, resample=Image.BICUBIC)
    left = left.rotate(rng.uniform(-2.2, 2.2), expand=True, resample=Image.BICUBIC)
    right = right.rotate(rng.uniform(-2.2, 2.2), expand=True, resample=Image.BICUBIC)

    lay(out, shadow, top, cx + rng.uniform(-4, 4), t + rng.uniform(-3, 3))
    lay(out, shadow, bot, cx + rng.uniform(-4, 4), b + rng.uniform(-3, 3))
    lay(out, shadow, left, l + rng.uniform(-3, 3), cy + rng.uniform(-4, 4))
    lay(out, shadow, right, r + rng.uniform(-3, 3), cy + rng.uniform(-4, 4))

    order = list(range(len(scraps)))
    rng.shuffle(order)
    for i, (px, py) in enumerate(((l, t), (r, t), (l, b), (r, b))):
        scrap = scraps[order[i % len(order)]]
        if rng.random() < 0.5:
            scrap = scrap.transpose(Image.FLIP_LEFT_RIGHT)
        if rng.random() < 0.5:
            scrap = scrap.transpose(Image.FLIP_TOP_BOTTOM)
        f = rng.uniform(70, 98) / scrap.width
        scrap = scrap.resize((int(scrap.width * f), int(scrap.height * f)), Image.LANCZOS)
        scrap = scrap.rotate(rng.uniform(-22, 22), expand=True, resample=Image.BICUBIC)
        lay(out, shadow, scrap, px + rng.uniform(-5, 5), py + rng.uniform(-5, 5))

    framed = Image.alpha_composite(shadow, out)

    well = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(well)
    pad = 12
    wd.rounded_rectangle(
        [l + pad, t + pad, r - pad, b - pad],
        radius=6,
        fill=(12, 10, 8, 255),
    )
    wd.rounded_rectangle(
        [l + pad + 2, t + pad + 2, r - pad - 2, b - pad - 2],
        radius=4,
        outline=(0, 0, 0, 200),
        width=2,
    )
    return Image.alpha_composite(framed, well)


def main() -> None:
    bf.PLANK_SHEET = resolve_sheet("tr_hud_planks.png")
    bf.SCRAP_SHEET = resolve_sheet("tr_hud_scraps.png")
    planks = bf.load_plank_bands()
    scraps = bf.load_scrap_pieces()
    if len(planks) < 3:
        raise SystemExit(f"only {len(planks)} HUD planks — sheet split failed")
    if len(scraps) < 4:
        raise SystemExit(f"only {len(scraps)} HUD scraps — sheet split failed")

    pad = 12
    l, t, r, b = WELL
    opening = {
        "x0": round((l + pad) / W, 4),
        "x1": round((r - pad) / W, 4),
        "y0": round((t + pad) / H, 4),
        "y1": round((b - pad) / H, 4),
    }

    for name, seed in BOXES:
        framed = bake(planks, scraps, seed)
        for base in ("assets-src", os.path.join("static", "assets")):
            path = os.path.join(APP, base, "sprites", "tombstone", name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            framed.save(path, optimize=True)
            print(f"wrote {path} {framed.size}")
    print(f"opening={opening} aspect={W / H:.3f} planks={len(planks)} scraps={len(scraps)}")


if __name__ == "__main__":
    main()
