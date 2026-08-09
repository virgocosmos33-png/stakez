"""Bake the EXPANDING WILD card: the straitjacket WILD with a rising arrow.

The plain WILD (assets/sprites/mirror/wr_wild.png) substitutes in place. The
expanding one is the wild that drops into a bottom cell and grows its whole
reel upward, so it carries an up-arrow stencilled on the jacket.

The arrow sits BELOW the WILD wordmark, around the card's vertical centre, on
purpose: the bottom cells clip a card's height to the middle band (see
cellFrames -> bottom:N, SlotSymbol clipH), so anything near the top or bottom
edge is masked away exactly where this symbol lives.

Run:  python tools/make_expanding_wild.py
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.normpath(os.path.join(HERE, "..", "assets", "sprites", "mirror"))
SRC = os.path.join(MIRROR, "wr_wild.png")
DST = os.path.join(MIRROR, "wr_wild_expand.png")
# pay-table tiles are served straight out of static/ (no source-tree copy)
PAY = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "paytable", "wexpand.png"))
PAY_SIZE = 300

SS = 2  # supersample factor for the arrow geometry


def arrow_mask(size: int) -> Image.Image:
    """Solid up-arrow mask, drawn oversized then downsampled for clean edges."""
    s = size * SS
    mask = Image.new("L", (s, s), 0)
    draw = ImageDraw.Draw(mask)

    cx = 0.5 * s
    # y range 0.47..0.74 of the card: inside the middle band a bottom cell keeps
    head_top = 0.472 * s
    head_bottom = 0.605 * s
    shaft_bottom = 0.735 * s
    head_half = 0.170 * s
    shaft_half = 0.066 * s

    draw.polygon(
        [(cx, head_top), (cx + head_half, head_bottom), (cx - head_half, head_bottom)],
        fill=255,
    )
    draw.rectangle(
        [cx - shaft_half, head_bottom - 0.012 * s, cx + shaft_half, shaft_bottom],
        fill=255,
    )
    return mask.resize((size, size), Image.LANCZOS)


def grunge(mask: Image.Image, seed: int = 7) -> Image.Image:
    """Worn-stencil alpha: speckle + soft blotches, matching the sprayed WILD."""
    rng = np.random.default_rng(seed)
    size = mask.size[0]

    speckle = rng.random((size, size)).astype(np.float32)
    speckle = np.asarray(
        Image.fromarray((speckle * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)),
        dtype=np.float32,
    ) / 255.0
    speckle = np.clip((speckle - 0.34) / 0.30, 0.0, 1.0)

    blotch = rng.random((size // 12 + 1, size // 12 + 1)).astype(np.float32)
    blotch = np.asarray(
        Image.fromarray((blotch * 255).astype(np.uint8)).resize((size, size), Image.BICUBIC),
        dtype=np.float32,
    ) / 255.0
    blotch = np.clip(blotch * 1.55 - 0.18, 0.0, 1.0)

    # mostly solid paint with a light mottle — at board scale a heavily worn
    # arrow just reads as a grey smudge instead of a direction
    wear = np.clip(0.80 + 0.20 * speckle * blotch, 0.0, 1.0)
    out = np.asarray(mask, dtype=np.float32) / 255.0 * wear
    return Image.fromarray((out * 255).astype(np.uint8), "L")


if __name__ == "__main__":
    card = Image.open(SRC).convert("RGBA")
    size = card.size[0]

    solid = arrow_mask(size)
    worn = grunge(solid)

    out = card.copy()

    # cast shadow first so the arrow lifts off the jacket at board scale
    shadow = solid.filter(ImageFilter.GaussianBlur(9))
    shadow = Image.fromarray((np.asarray(shadow, dtype=np.float32) * 0.72).astype(np.uint8), "L")
    shadow_layer = Image.new("RGBA", card.size, (8, 9, 12, 0))
    shadow_layer.putalpha(shadow.transform(
        card.size, Image.AFFINE, (1, 0, 0, 0, 1, -int(size * 0.012)), resample=Image.BILINEAR
    ))
    out = Image.alpha_composite(out, shadow_layer)

    # dark keyline: the dilated silhouette, so the white reads on light cloth
    keyline = solid.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1.4))
    key_layer = Image.new("RGBA", card.size, (22, 24, 28, 0))
    key_layer.putalpha(
        Image.fromarray((np.asarray(keyline, dtype=np.float32) * 0.92).astype(np.uint8), "L")
    )
    out = Image.alpha_composite(out, key_layer)

    paint = Image.new("RGBA", card.size, (247, 249, 252, 0))
    paint.putalpha(worn)
    out = Image.alpha_composite(out, paint)

    # the arrow must never punch a hole outside the figure's own silhouette
    out.putalpha(Image.fromarray(
        np.maximum(np.asarray(card.split()[3]), np.asarray(out.split()[3])).astype(np.uint8), "L"
    ))

    out.save(DST)
    print(f"wrote {DST} ({out.size[0]}x{out.size[1]})")

    out.resize((PAY_SIZE, PAY_SIZE), Image.LANCZOS).save(PAY)
    print(f"wrote {PAY} ({PAY_SIZE}x{PAY_SIZE})")
