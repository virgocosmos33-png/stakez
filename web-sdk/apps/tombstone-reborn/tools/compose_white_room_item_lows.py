"""Local fallback masters for THE WHITE ROOM low symbols (items, not card ranks).

Used when Scenario custom-generation hits plan limits (HTTP 429). Draws readable
clinical asylum prop icons onto a charcoal void plate (1024²) matching gen_symbols
framing. Palette: whites / greys / silvers + sparse dried-blood #6b2a28.

    python tools/compose_white_room_item_lows.py
    python tools/compose_white_room_item_lows.py l1 l3
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

HERE = Path(__file__).resolve().parent
OUT = HERE / "symbol_art"
SIZE = 1024
BG = (18, 18, 20, 255)
WHITE = (244, 241, 236, 255)
SILVER = (200, 196, 188, 255)
GREY = (138, 134, 128, 255)
DARK = (90, 88, 84, 255)
BLOOD = (107, 42, 40, 220)


def _canvas() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), BG)


def _shade(img: Image.Image) -> Image.Image:
    arr = np.asarray(img).astype(np.float32)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    cx = cy = SIZE / 2
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    vignette = np.clip(1.15 - (r / (SIZE * 0.72)) ** 1.6, 0.55, 1.0)
    noise = np.random.default_rng(1897).normal(0, 4.5, (SIZE, SIZE))
    for c in range(3):
        arr[..., c] = np.clip(arr[..., c] * vignette + noise, 0, 255)
    out = Image.fromarray(arr.astype(np.uint8), "RGBA")
    return out.filter(ImageFilter.GaussianBlur(radius=0.6))


def compose_syringe() -> Image.Image:
    im = _canvas()
    d = ImageDraw.Draw(im)
    # barrel
    x0, y0, x1, y1 = 390, 220, 634, 720
    d.rounded_rectangle([x0, y0, x1, y1], radius=28, fill=WHITE, outline=GREY, width=6)
    # glass sheen
    d.rectangle([410, 250, 450, 690], fill=(255, 255, 255, 70))
    # measurement ticks
    for i, y in enumerate(range(300, 680, 55)):
        d.line([(460, y), (560 if i % 2 == 0 else 520, y)], fill=DARK, width=4)
    # blood residue near tip
    d.ellipse([430, 640, 590, 700], fill=BLOOD)
    # plunger rod
    d.rectangle([470, 120, 554, 240], fill=SILVER, outline=DARK, width=4)
    d.ellipse([440, 90, 584, 150], fill=GREY, outline=DARK, width=4)
    # hub + needle
    d.polygon([(420, 720), (604, 720), (540, 780), (484, 780)], fill=SILVER, outline=DARK)
    d.line([(512, 780), (512, 900)], fill=GREY, width=10)
    d.polygon([(500, 900), (524, 900), (512, 940)], fill=DARK)
    return _shade(im)


def compose_stethoscope() -> Image.Image:
    im = _canvas()
    d = ImageDraw.Draw(im)
    # tubing loop
    d.arc([220, 200, 804, 760], start=200, end=340, fill=SILVER, width=28)
    d.arc([260, 240, 764, 720], start=210, end=330, fill=GREY, width=18)
    # earpieces
    for cx in (300, 724):
        d.ellipse([cx - 36, 170, cx + 36, 242], fill=SILVER, outline=DARK, width=5)
        d.ellipse([cx - 16, 190, cx + 16, 222], fill=DARK)
    # chest piece
    d.ellipse([420, 620, 604, 804], fill=SILVER, outline=DARK, width=8)
    d.ellipse([450, 650, 574, 774], fill=WHITE, outline=GREY, width=5)
    d.ellipse([490, 690, 534, 734], fill=BLOOD)
    # stem
    d.rectangle([492, 560, 532, 640], fill=GREY, outline=DARK, width=4)
    return _shade(im)


def compose_restraint_buckle() -> Image.Image:
    im = _canvas()
    d = ImageDraw.Draw(im)
    # leather strap
    d.rounded_rectangle([160, 420, 864, 620], radius=40, fill=(58, 54, 50, 255), outline=DARK, width=6)
    # stitch lines
    for y in (450, 590):
        for x in range(200, 840, 28):
            d.ellipse([x, y, x + 6, y + 6], fill=GREY)
    # blood fleck
    d.ellipse([700, 500, 760, 555], fill=BLOOD)
    # steel buckle plate
    d.rounded_rectangle([360, 360, 664, 680], radius=18, fill=SILVER, outline=DARK, width=8)
    d.rounded_rectangle([400, 400, 624, 640], radius=12, fill=WHITE, outline=GREY, width=5)
    # prong
    d.rectangle([500, 300, 524, 520], fill=GREY, outline=DARK, width=4)
    d.ellipse([470, 280, 554, 340], fill=SILVER, outline=DARK, width=5)
    return _shade(im)


def compose_clipboard_404() -> Image.Image:
    im = _canvas()
    d = ImageDraw.Draw(im)
    # board
    d.rounded_rectangle([260, 140, 764, 900], radius=24, fill=GREY, outline=DARK, width=8)
    # paper
    d.rectangle([300, 220, 724, 860], fill=WHITE, outline=SILVER, width=4)
    # clip
    d.rounded_rectangle([400, 110, 624, 230], radius=10, fill=SILVER, outline=DARK, width=6)
    d.rectangle([430, 150, 594, 200], fill=DARK)
    # PATIENT 404 stamp
    d.rectangle([340, 320, 684, 420], outline=BLOOD, width=8)
    # crude block digits / letters via thick lines (no font dependency)
    # "404"
    def digit_block(x, y, w=70, h=90):
        d.rectangle([x, y, x + w, y + h], outline=BLOOD, width=10)

    digit_block(360, 480)
    d.ellipse([470, 480, 560, 570], outline=BLOOD, width=10)  # 0
    digit_block(590, 480)
    # underline bars as "PATIENT"
    for i, y in enumerate(range(620, 760, 28)):
        d.line([(360, y), (680 - i * 8, y)], fill=DARK, width=6)
    return _shade(im)


def compose_pill_bottle() -> Image.Image:
    im = _canvas()
    d = ImageDraw.Draw(im)
    # body
    d.rounded_rectangle([360, 300, 664, 820], radius=40, fill=WHITE, outline=GREY, width=7)
    # label strip
    d.rectangle([380, 480, 644, 620], fill=SILVER, outline=DARK, width=4)
    d.line([(400, 530), (624, 530)], fill=DARK, width=5)
    d.line([(400, 565), (580, 565)], fill=GREY, width=4)
    # cap
    d.rounded_rectangle([390, 200, 634, 320], radius=20, fill=SILVER, outline=DARK, width=6)
    d.ellipse([410, 180, 614, 240], fill=GREY, outline=DARK, width=5)
    # residue near rim
    d.ellipse([520, 300, 600, 350], fill=BLOOD)
    # highlight
    d.rectangle([390, 340, 430, 780], fill=(255, 255, 255, 55))
    return _shade(im)


COMPOSERS = {
    "l1": ("card_l1_syringe.png", compose_syringe),
    "l2": ("card_l2_stethoscope.png", compose_stethoscope),
    "l3": ("card_l3_restraint_buckle.png", compose_restraint_buckle),
    "l4": ("card_l4_clipboard_404.png", compose_clipboard_404),
    "l5": ("card_l5_pill_bottle.png", compose_pill_bottle),
}


def compose_one(sid: str) -> Path:
    sid = sid.lower()
    if sid not in COMPOSERS:
        raise KeyError(sid)
    name, fn = COMPOSERS[sid]
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img = fn()
    # slight contrast punch for reel readability
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img.save(path, "PNG")
    print(f"{sid}: composed {path}")
    return path


if __name__ == "__main__":
    wanted = [a.lower() for a in sys.argv[1:] if not a.startswith("-")] or list(COMPOSERS)
    for sid in wanted:
        compose_one(sid)
