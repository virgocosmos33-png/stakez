"""Bake the five SCATTER cards, one per landing position.

The scatters land left to right and the game already voices them as five
distinct stops (SCATTER_LAND_SOUND_MAP). These cards give each stop its own
face: MEMORY, DOUBT, REGRET, REVELATION, OBLIVION.

Look is matched to the STRETCH / SPLIT / CLONE / WILD cards: a dirty white
ground with a heavy blocky wordmark cracked and worn across it. Those cards
have their words baked into generated art rather than set in a font, so the
match here is by treatment — Arial Black condensed to a single cap height for
all five words, then eaten away by cracks and speckle.

The ground is a plain off-white with nothing drawn on it — no wall, no quilting,
no figure. Just grime: broad staining, flaked speckle and a soft vignette. The
card keeps the bezel every other symbol wears (lifted from the atlas's s.png,
which is the only thing taken from the old wordless scatter art).

Also bakes wr_scatter_blur.png, the 300x480 spin smear, so a streaking reel
never falls back to the old head card either.

Run:  python tools/make_scatter_words.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic"))
MIRROR_DIR = os.path.normpath(os.path.join(HERE, "..", "assets", "sprites", "mirror"))
OUT_DIR = MIRROR_DIR
# the pay-table tiles are served straight out of static/ (no source-tree copy)
PAYTABLE_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "paytable"))

WORDS = ["MEMORY", "DOUBT", "REGRET", "REVELATION", "OBLIVION"]

CARD = 300
SS = 2  # everything is drawn at 2x and downsampled onto the card

RED = (214, 22, 40, 255)
WHITE = (252, 252, 250, 255)
KEYLINE = (26, 24, 22, 255)
LABEL_INK = (44, 41, 38, 255)

PAPER = (247, 245, 241)  # the clean white the grime is laid over

BLUR_H = 480  # spin-smear frame height, matching the atlas blur frames

WORD_CY = 132
WORD_MAX_W = 224
WORD_SIZE = 64  # one cap height for every word; long words condense instead
# Arial Black is heavy enough that the letters close up on each other as soon
# as they carry an edge — track them apart so the outline stays a per-letter
# outline instead of welding the word into one slab
WORD_TRACKING = 5.0
WORD_MIN_SQUEEZE = 0.42
OUTLINE = 3.0  # white paint edge
KEY = 1.2  # dark keyline outside the white, so red reads on a white ground

LABEL_CY = 197
LABEL_SIZE = 24
LABEL_TRACKING = 5.0

BEZEL_INSET = 9
BEZEL_RADIUS = 17


def font_path(name: str) -> Path:
    path = Path(r"C:\Windows\Fonts") / name
    if not path.exists():
        raise SystemExit(f"missing display font: {path}")
    return path


def base_card() -> Image.Image:
    """The stock scatter card — used for its bezel and its rounded silhouette."""
    with open(os.path.join(ATLAS_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        atlas = json.load(f)
    sheet = Image.open(os.path.join(ATLAS_DIR, "symbolsStatic.webp")).convert("RGBA")
    f = atlas["frames"]["s.png"]["frame"]
    return sheet.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))


def dirty_white(seed: int = 11) -> Image.Image:
    """Plain white, then filthy. No wall, no quilting, no picture — a flat sheet
    with broad staining, flaked speckle and a soft vignette worked into it."""
    rng = np.random.default_rng(seed)
    px = np.tile(np.asarray(PAPER, dtype=np.float32) / 255.0, (CARD, CARD, 1))

    def octave(cells: int) -> np.ndarray:
        small = rng.random((cells, cells)).astype(np.float32)
        return np.asarray(
            Image.fromarray((small * 255).astype(np.uint8)).resize((CARD, CARD), Image.BICUBIC),
            dtype=np.float32,
        ) / 255.0

    # grime: broad brown-grey staining plus a finer dirt layer
    stain = np.clip(octave(5) * 0.65 + octave(13) * 0.35, 0.0, 1.0)
    stain = np.clip((stain - 0.42) / 0.45, 0.0, 1.0) ** 1.3
    tint = np.stack([stain * 0.22, stain * 0.21, stain * 0.18], axis=-1)
    px = np.clip(px - tint, 0.0, 1.0)

    # paper grain, so the flat sheet still has a surface under the grime
    grain = rng.normal(0.0, 0.014, (CARD, CARD)).astype(np.float32)
    grain = np.asarray(
        Image.fromarray(((grain * 0.5 + 0.5) * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(0.5)
        ),
        dtype=np.float32,
    ) / 255.0 - 0.5
    px = np.clip(px + grain[..., None], 0.0, 1.0)

    # speckle: scattered dark flecks, like flaked paint
    fleck = rng.random((CARD, CARD)).astype(np.float32)
    fleck = np.clip((fleck - 0.985) / 0.015, 0.0, 1.0)
    fleck = np.asarray(
        Image.fromarray((fleck * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)),
        dtype=np.float32,
    ) / 255.0
    px = np.clip(px - fleck[..., None] * 0.35, 0.0, 1.0)

    # vignette so the wordmark sits in a slightly cleaner middle
    yy, xx = np.mgrid[0:CARD, 0:CARD].astype(np.float32)
    r = np.sqrt(((xx - CARD / 2) / (CARD / 2)) ** 2 + ((yy - CARD / 2) / (CARD / 2)) ** 2)
    px = np.clip(px - (np.clip(r - 0.58, 0, 1) ** 1.5 * 0.30)[..., None], 0.0, 1.0)

    return Image.fromarray((px * 255).astype(np.uint8), "RGB").convert("RGBA")


def ground(card: Image.Image) -> Image.Image:
    """Dirty white inside the bezel, the stock card's frame around it."""
    mask = Image.new("L", (CARD, CARD), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [BEZEL_INSET, BEZEL_INSET, CARD - 1 - BEZEL_INSET, CARD - 1 - BEZEL_INSET],
        radius=BEZEL_RADIUS,
        fill=255,
    )
    out = card.copy()
    out.paste(dirty_white(), (0, 0), mask)
    out.putalpha(card.split()[3])
    return out


def glyph_mask(text: str, font: ImageFont.FreeTypeFont, tracking: float) -> Image.Image:
    """The word as a solid alpha mask, tracked out, trimmed to its own ink."""
    pad = 40 * SS
    widths = [font.getbbox(c)[2] - font.getbbox(c)[0] for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    canvas = Image.new("L", (int(total) + pad * 2, int(font.size * 2) + pad * 2), 0)
    draw = ImageDraw.Draw(canvas)
    x = pad
    for char, w in zip(text, widths):
        draw.text((x, canvas.height / 2), char, font=font, anchor="lm", fill=255)
        x += w + tracking
    return canvas.crop(canvas.getbbox())


def cracks(size: tuple[int, int], seed: int) -> Image.Image:
    """Worn paint: a few splintered cracks plus speckle, as an alpha multiplier
    applied to the whole wordmark — edge and all, the way the CLONE / STRETCH
    cards read."""
    rng = np.random.default_rng(seed)
    w, h = size
    wear = Image.new("L", size, 255)
    draw = ImageDraw.Draw(wear)

    # hairlines, not gashes: at card scale the cap height is only ~45px, so a
    # crack any thicker than a pixel or two reads as damage rather than wear
    for _ in range(rng.integers(2, 4)):
        y = rng.uniform(h * 0.15, h * 0.85)
        x = -w * 0.05
        points = [(x, y)]
        while x < w * 1.05:
            x += rng.uniform(w * 0.06, w * 0.16)
            y += rng.uniform(-h * 0.08, h * 0.08)
            points.append((x, min(max(y, 0), h)))
        draw.line(points, fill=0, width=int(rng.integers(1, 3)) * SS)

    # a couple of steeper splinters
    for _ in range(rng.integers(1, 3)):
        x = rng.uniform(w * 0.1, w * 0.9)
        y = rng.uniform(0, h)
        draw.line(
            [(x, y), (x + rng.uniform(-w * 0.04, w * 0.04), y + rng.uniform(-h * 0.4, h * 0.4))],
            fill=0,
            width=SS,
        )

    arr = np.asarray(wear, dtype=np.float32) / 255.0
    speckle = rng.random((h, w)).astype(np.float32)
    speckle = np.asarray(
        Image.fromarray((speckle * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)),
        dtype=np.float32,
    ) / 255.0
    arr *= np.clip(0.82 + 0.34 * speckle, 0.0, 1.0)
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "L")


def wordmark(word: str, font: ImageFont.FreeTypeFont, seed: int) -> Image.Image:
    """Red fill, white paint edge, dark keyline — then cracked through."""
    mask = glyph_mask(word, font, WORD_TRACKING * SS)

    # one cap height for all five words: condense instead of shrinking
    budget = (WORD_MAX_W - 2 * (OUTLINE + KEY)) * SS
    if mask.width > budget:
        squeeze = max(WORD_MIN_SQUEEZE, budget / mask.width)
        mask = mask.resize((max(1, int(mask.width * squeeze)), mask.height), Image.LANCZOS)

    pad = int((OUTLINE + KEY) * SS) + 6
    layer_size = (mask.width + pad * 2, mask.height + pad * 2)
    solid = Image.new("L", layer_size, 0)
    solid.paste(mask, (pad, pad))

    def dilate(src: Image.Image, radius: float) -> Image.Image:
        """Grow the mask by exactly `radius` card-pixels (MaxFilter(3) = 1px)."""
        out = src
        for _ in range(int(round(radius * SS))):
            out = out.filter(ImageFilter.MaxFilter(3))
        return out.filter(ImageFilter.GaussianBlur(0.6))

    layer = Image.new("RGBA", layer_size, (0, 0, 0, 0))
    for colour, radius in ((KEYLINE, OUTLINE + KEY), (WHITE, OUTLINE), (RED, 0)):
        part = Image.new("RGBA", layer_size, colour[:3] + (0,))
        part.putalpha(dilate(solid, radius) if radius else solid)
        layer = Image.alpha_composite(layer, part)

    worn = np.asarray(layer.split()[3], dtype=np.float32) / 255.0
    worn *= np.asarray(cracks(layer_size, seed), dtype=np.float32) / 255.0
    layer.putalpha(Image.fromarray((worn * 255).astype(np.uint8), "L"))
    return layer


def spin_smear(face: Image.Image) -> Image.Image:
    """The reel-blur frame: the card stretched to the atlas smear height and
    dragged along y, so a spinning reel streaks the new card instead of falling
    back to s_blur.png (which is the old head)."""
    tall = Image.new("RGBA", (CARD, BLUR_H), (0, 0, 0, 0))
    tall.paste(face, (0, (BLUR_H - CARD) // 2))

    px = np.asarray(tall, dtype=np.float32) / 255.0
    alpha = px[..., 3:4]
    px[..., :3] *= alpha  # premultiply so the smear does not drag black in

    # box blur along y only, via a running sum
    radius = 46
    pad = np.pad(px, ((radius + 1, radius), (0, 0), (0, 0)), mode="edge")
    csum = np.cumsum(pad, axis=0)
    px = (csum[2 * radius + 1 :] - csum[: -(2 * radius + 1)]) / (2 * radius + 1)

    alpha = np.clip(px[..., 3:4], 1e-4, 1.0)
    rgb = np.clip(px[..., :3] / alpha, 0.0, 1.0)
    out = np.concatenate([rgb, np.clip(px[..., 3:4], 0.0, 1.0)], axis=-1)
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def draw_tracked(draw: ImageDraw.ImageDraw, cx: float, cy: float, text: str,
                 font: ImageFont.FreeTypeFont, tracking: float, fill) -> None:
    widths = [font.getbbox(c)[2] - font.getbbox(c)[0] for c in text]
    x = cx - (sum(widths) + tracking * (len(text) - 1)) / 2
    for char, w in zip(text, widths):
        draw.text((x, cy), char, font=font, anchor="lm", fill=fill)
        x += w + tracking


def build(card: Image.Image, word: str, word_font: ImageFont.FreeTypeFont,
          label_font: ImageFont.FreeTypeFont, seed: int) -> Image.Image:
    layer = Image.new("RGBA", (CARD * SS, CARD * SS), (0, 0, 0, 0))

    mark = wordmark(word, word_font, seed)
    # soft shadow so the mark lifts off the wall behind it
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    tinted = Image.new("RGBA", mark.size, (0, 0, 0, 0))
    tinted.putalpha(
        Image.fromarray((np.asarray(mark.split()[3], dtype=np.float32) * 0.34).astype(np.uint8), "L")
    )
    shadow.paste(
        tinted,
        (int(CARD * SS / 2 - mark.width / 2), int(WORD_CY * SS - mark.height / 2 + 3 * SS)),
    )
    layer = Image.alpha_composite(layer, shadow.filter(ImageFilter.GaussianBlur(3 * SS)))

    layer.paste(
        mark,
        (int(CARD * SS / 2 - mark.width / 2), int(WORD_CY * SS - mark.height / 2)),
        mark,
    )

    draw_tracked(
        ImageDraw.Draw(layer), CARD * SS / 2, LABEL_CY * SS, "SCATTER", label_font,
        LABEL_TRACKING * SS, fill=LABEL_INK,
    )

    out = Image.alpha_composite(card, layer.resize((CARD, CARD), Image.LANCZOS))
    out.putalpha(card.split()[3])
    return out


if __name__ == "__main__":
    word_font = ImageFont.truetype(str(font_path("ariblk.ttf")), WORD_SIZE * SS)
    label_font = ImageFont.truetype(str(font_path("ariblk.ttf")), LABEL_SIZE * SS)
    card = ground(base_card())

    faces = []
    for i, word in enumerate(WORDS, start=1):
        dst = os.path.join(OUT_DIR, f"wr_scatter_{i}.png")
        face = build(card, word, word_font, label_font, seed=i * 17)
        face.save(dst)
        faces.append(face)
        print(f"wrote {word:<11} -> {dst}")

    blur = os.path.join(OUT_DIR, "wr_scatter_blur.png")
    spin_smear(faces[0]).save(blur)
    print(f"wrote spin smear -> {blur}")

    # the pay table shows the first face — the wordless card no longer appears
    # anywhere in game, every scatter now lands wearing one of these
    pay = os.path.join(PAYTABLE_DIR, "s.png")
    faces[0].save(pay)
    print(f"wrote pay tile -> {pay}")
