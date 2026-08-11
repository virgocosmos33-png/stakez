"""Preview the burning-frame fire over the reference card. The frame is baked and
drawn NORMAL alpha in-game, so a plain alpha-composite here is exactly what the
engine draws — no GPU needed. Renders 3 flipbook phases side by side.

Run: python tools/qa_fire_mock.py
"""
from __future__ import annotations
import json
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
FX = os.path.join(APP, "static", "assets", "sprites", "fx")
REF = os.path.join(APP, "assets-raw", "ref_fire")
OUT = os.path.join(APP, "qa-shots")

atlas = Image.open(os.path.join(FX, "cell_fire.png")).convert("RGBA")
meta = json.load(open(os.path.join(FX, "cell_fire.json")))
geo = meta["meta"]["geometry"]


def frames(prefix: str):
    out = []
    for name, f in meta["frames"].items():
        if name.startswith(prefix):
            fr = f["frame"]
            out.append(atlas.crop((fr["x"], fr["y"], fr["x"] + fr["w"], fr["y"] + fr["h"])))
    return out


FRAMES = frames("0_frame_")


def compose(phase: int) -> Image.Image:
    card = Image.open(os.path.join(REF, "ref_card.png")).convert("RGBA")
    cw = 220
    ch = int(card.height * cw / card.width)
    card = card.resize((cw, ch), Image.LANCZOS)

    # sprite footprint = card * (frame/card ratio), centred on the card
    fw = int(cw * geo["frameW"] / geo["cardW"])
    fh = int(ch * geo["frameH"] / geo["cardH"])
    fire = FRAMES[phase % len(FRAMES)].resize((fw, fh), Image.LANCZOS)

    W, H = fw + 120, fh + 120
    canvas = Image.new("RGBA", (W, H), (18, 20, 26, 255))
    cx, cy = W // 2, H // 2
    canvas.alpha_composite(card, (cx - cw // 2, cy - ch // 2))
    canvas.alpha_composite(fire, (cx - fw // 2, cy - fh // 2))
    return canvas


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    tiles = [compose(p) for p in (0, 5, 10)]
    w = sum(t.width for t in tiles) + 20 * (len(tiles) - 1)
    h = max(t.height for t in tiles)
    strip = Image.new("RGBA", (w, h), (10, 10, 12, 255))
    x = 0
    for t in tiles:
        strip.alpha_composite(t, (x, 0))
        x += t.width + 20
    strip.convert("RGB").save(os.path.join(OUT, "fire_mock.png"))
    print("[mock] wrote", os.path.join(OUT, "fire_mock.png"), strip.size)


if __name__ == "__main__":
    main()
