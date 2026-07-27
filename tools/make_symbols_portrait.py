"""Reshape the board symbol cards from square to portrait.

The reel pitch is square (SYMBOL_SIZE on both axes) and is NOT changed here: a
portrait *card* is painted inside that square footprint instead, so the leftover
margin becomes real gap between neighbouring symbols. That is what makes the
symbols read as tall, and it is also what stops two low symbols -- which used to
be edge-to-edge opaque panels -- from merging into one block.

Doing it in the art rather than in the layout matters: the win/land/postWin Spine
rigs keep their own copies of the same cards in mm_symbols.atlas, and those
regions must stay 300x300 or every rig would need re-authoring. Repainting the
pixels inside the region leaves the rigs untouched, so a symbol looks identical
whether it is a static sprite or a spine animation.

The packed atlases are the only copy of the card art left (the tool named in
symbolsStatic.json's meta is long gone), so the first run snapshots every region
it is about to touch into assets-raw/symbols_square/ and every run reads from
that snapshot. Re-running therefore rebuilds from square originals instead of
eating another crop off an already-portrait card.

    python tools/make_symbols_portrait.py --preview   # contact sheet only
    python tools/make_symbols_portrait.py             # write the atlases
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "web-sdk/apps/white-room/assets"
STATIC_DIR = ASSETS / "sprites/symbolsStatic"
SPINE_DIR = ASSETS / "spines/mm_symbols"
SNAPSHOT = ASSETS.parent / "assets-raw/symbols_square"

# --- card shape ---------------------------------------------------------------
# Fractions of the square cell the card is painted into. Height is nearly the
# full cell (a hairline of breathing room so stacked cards show a seam); width is
# what makes it portrait. 0.75 is the usual slot card ratio and leaves a clear
# column of background between reels.
CARD_H_FRAC = 292 / 300
CARD_ASPECT = 0.775  # card width / card height
RADIUS_FRAC = 20 / 300

# Bezel drawn from the outside in. Deliberately thin -- a couple of screen pixels
# at the live 118px cell -- so it separates neighbours without framing them.
EDGE_RGBA = (8, 10, 12, 235)
BEZEL_RGBA = (146, 154, 163, 230)
INNER_RGBA = (18, 20, 24, 200)
EDGE_W, BEZEL_W, INNER_W = 2, 3, 1

SS = 4  # supersample factor for smooth rounded corners

# The two card classes are authored differently, so they are reshaped
# differently. Premiums/wild/scatter are full-bleed photographs sitting inside a
# uniform dark margin: crop the margin off and let the portrait opening crop the
# sides, which is flattering on a face. The lows are small objects floating on a
# flat panel: scale the object to sit inside the opening, whole.
#
# This is keyed off the symbol name rather than measured, because measuring gets
# it wrong -- h4's photograph is dark along its top edge, so a content-bbox test
# reads it as a floating object and letterboxes the face.
PHOTO_CARDS = [f"h{i}" for i in range(1, 6)] + ["w", "s"]
OBJECT_CARDS = [f"l{i}" for i in range(1, 6)]
CARDS = PHOTO_CARDS + OBJECT_CARDS
CONTAIN_PAD = 0.95


def snapshot(name: str, tile: Image.Image) -> Image.Image:
    """Pristine square original for `name`, captured on the first run."""
    SNAPSHOT.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT / f"{name}.png"
    if not path.exists():
        tile.save(path)
    return Image.open(path).convert("RGBA")


def content_box(img: Image.Image) -> tuple[int, int, int, int]:
    """Bounding box of what reads as content, against the card's own backdrop."""
    a = np.asarray(img.convert("RGBA"))
    rgb, alpha = a[..., :3].astype(int).mean(axis=2), a[..., 3]
    corners = [rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]]
    mask = (np.abs(rgb - float(np.median(corners))) > 12) & (alpha > 8)
    if not mask.any():
        return 0, 0, img.width, img.height
    xs, ys = np.where(mask.any(axis=0))[0], np.where(mask.any(axis=1))[0]
    return int(xs[0]), int(ys[0]), int(xs[-1]) + 1, int(ys[-1]) + 1


def backdrop(img: Image.Image) -> tuple[int, int, int, int]:
    a = np.asarray(img.convert("RGBA"))
    corners = np.stack([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]]).astype(int)
    r, g, b = (int(v) for v in corners[:, :3].mean(axis=0))
    return r, g, b, 255


def fit(content: Image.Image, box_w: int, box_h: int, cover: bool) -> Image.Image:
    scale_fn = max if cover else min
    scale = scale_fn(box_w / content.width, box_h / content.height)
    if not cover:
        scale *= CONTAIN_PAD
    resized = content.resize(
        (max(1, round(content.width * scale)), max(1, round(content.height * scale))),
        Image.LANCZOS,
    )
    out = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    out.paste(resized, ((box_w - resized.width) // 2, (box_h - resized.height) // 2))
    return out


def rounded_mask(w: int, h: int, radius: int) -> Image.Image:
    mask = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, w * SS - 1, h * SS - 1), radius=radius * SS, fill=255
    )
    return mask.resize((w, h), Image.LANCZOS)


def make_card(src: Image.Image, cover: bool) -> Image.Image:
    """Repaint a square card as a portrait card centred in the same footprint."""
    cw, ch = src.width, src.height
    card_h = round(ch * CARD_H_FRAC)
    card_w = round(card_h * CARD_ASPECT)
    radius = max(2, round(ch * RADIUS_FRAC))
    inset = EDGE_W + BEZEL_W + INNER_W

    x0, y0, x1, y1 = content_box(src)
    if cover:
        # Uniform dark margin around the photograph -- the left edge measures it
        # reliably on every premium, so square it up and drop it on all sides.
        m = x0
        x0, y0, x1, y1 = m, m, cw - m, ch - m
    content = src.crop((x0, y0, x1, y1))

    card = Image.new("RGBA", (card_w, card_h), backdrop(src))
    card.paste(
        fit(content, card_w - 2 * inset, card_h - 2 * inset, cover), (inset, inset), None
    )

    # bezel, outside in
    layer = Image.new("RGBA", (card_w * SS, card_h * SS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    off = 0
    for colour, width in ((EDGE_RGBA, EDGE_W), (BEZEL_RGBA, BEZEL_W), (INNER_RGBA, INNER_W)):
        draw.rounded_rectangle(
            (off * SS, off * SS, (card_w - off) * SS - 1, (card_h - off) * SS - 1),
            radius=max(1, radius - off) * SS,
            outline=colour,
            width=width * SS,
        )
        off += width
    card.alpha_composite(layer.resize((card_w, card_h), Image.LANCZOS))

    card.putalpha(
        Image.composite(card.getchannel("A"), Image.new("L", card.size, 0), rounded_mask(card_w, card_h, radius))
    )

    out = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    out.paste(card, ((cw - card_w) // 2, (ch - card_h) // 2), card)
    return out


def make_smear(src: Image.Image) -> Image.Image:
    """Narrow a spin smear to the card's width -- no bezel, it is motion not a card.

    A straight centre crop, deliberately: the smear is already the card blurred at
    cell scale, so rescaling it to the new width would zoom the streak and it
    would no longer match the card it blurs into when the reel stops.
    """
    cw, ch = src.width, src.height
    card_w = round(cw * CARD_H_FRAC * CARD_ASPECT)
    out = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    left = (cw - card_w) // 2
    out.paste(src.crop((left, 0, left + card_w, ch)), (left, 0))
    return out


def region_jobs() -> list[tuple[str, dict, str]]:
    """(atlas key, frame rect, snapshot name) for every region we repaint."""
    jobs: list[tuple[str, dict, str]] = []

    frames = json.loads((STATIC_DIR / "symbolsStatic.json").read_text())["frames"]
    for key, meta in frames.items():
        stem = key.split(".")[0]
        base = stem.removesuffix("_burn").removesuffix("_blur")
        if base in CARDS:
            jobs.append(("static", meta["frame"], stem))

    atlas = (SPINE_DIR / "mm_symbols.atlas").read_text().splitlines()
    for i, line in enumerate(atlas):
        if line.strip().startswith("bounds:"):
            name = atlas[i - 1].strip()
            if name in CARDS:
                x, y, w, h = (int(v) for v in line.split(":")[1].split(","))
                jobs.append(("spine", {"x": x, "y": y, "w": w, "h": h}, f"spine_{name}"))
    return jobs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()

    sheets = {
        "static": Image.open(STATIC_DIR / "symbolsStatic.png").convert("RGBA"),
        "spine": Image.open(SPINE_DIR / "mm_symbols.png").convert("RGBA"),
    }
    built: list[tuple[str, Image.Image]] = []

    for atlas_key, rect, name in region_jobs():
        sheet = sheets[atlas_key]
        box = (rect["x"], rect["y"], rect["x"] + rect["w"], rect["y"] + rect["h"])
        src = snapshot(name, sheet.crop(box))
        base = name.removeprefix("spine_").removesuffix("_burn").removesuffix("_blur")
        card = make_smear(src) if name.endswith("_blur") else make_card(src, base in PHOTO_CARDS)
        built.append((name, card))
        if not args.preview:
            sheet.paste(card, box)  # region size is fixed; only the pixels change

    if args.preview:
        cards = [c for n, c in built if not n.startswith("spine_") and not n.endswith(("_burn", "_blur"))]
        w = max(c.width for c in cards)
        sheet = Image.new("RGBA", (w * len(cards), cards[0].height), (26, 28, 32, 255))
        for i, c in enumerate(cards):
            sheet.paste(c, (i * w, 0), c)
        sheet.save(ROOT / "_symbol_preview.png")
        print(f"preview -> _symbol_preview.png ({len(cards)} cards)")
        return

    for key, path in (("static", STATIC_DIR / "symbolsStatic"), ("spine", SPINE_DIR / "mm_symbols")):
        sheets[key].save(path.with_suffix(".png"))
        sheets[key].save(path.with_suffix(".webp"), quality=95, method=6)
        print(f"wrote {path.name}.png / .webp")
    print(f"repainted {len(built)} regions")


if __name__ == "__main__":
    main()
