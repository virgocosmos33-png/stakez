"""Measure nine-slice corner insets for the ornate gold reel frame.

Texture mirror_frame_wide.png (1213x892) is fully composited:
  - outer corners = transparent (alpha 0)
  - rails         = DIM bronze border down each side (max(r,g,b) ~ 30..90)
  - ornaments     = BRIGHT gold at the 4 corners + top/bottom centre cartouches
  - interior      = flat opaque near-black panel (rgb ~13,13,15)

For a single-texture PIXI.NineSliceSprite (CSS border-image equivalent) the
insets must put the whole ornate BORDER into the corner/edge bands and leave only
the flat interior in the stretchable centre. We report reaches for a few "gold"
brightness thresholds and render debug overlays so the cut lines can be eyeballed
(corners must sit fully inside the corner boxes).

Run from web-sdk/apps/ways:  python tools/measure_frame_nineslice.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

APP = Path(__file__).resolve().parent.parent
SRC = APP / "static" / "assets" / "sprites" / "mirror" / "mirror_frame_wide.png"
OUT = APP.parents[1] / "qa-shots" / "reelframe"
OUT.mkdir(parents=True, exist_ok=True)

ALPHA_T = 40
BAND = 0.45  # only look this far in from each edge when measuring a side


def reaches(px, W, H, thr):
    """max inward reach of pixels brighter than thr, per side, within BAND."""
    xlim = int(W * BAND)
    ylim = int(H * BAND)

    def bright(x, y):
        r, g, b, a = px[x, y]
        return a > ALPHA_T and max(r, g, b) >= thr

    leftW = 0
    rightW = 0
    for y in range(H):
        for x in range(xlim):
            if bright(x, y) and x > leftW:
                leftW = x
        for x in range(W - 1, W - xlim, -1):
            if bright(x, y) and (W - x) > rightW:
                rightW = W - x
    topH = 0
    bottomH = 0
    for x in range(W):
        for y in range(ylim):
            if bright(x, y) and y > topH:
                topH = y
        for y in range(H - 1, H - ylim, -1):
            if bright(x, y) and (H - y) > bottomH:
                bottomH = H - y
    return leftW + 1, topH + 1, rightW, bottomH


def main() -> None:
    im = Image.open(SRC).convert("RGBA")
    W, H = im.size
    px = im.load()
    print(f"[size] {W} x {H}  ratio {W/H:.4f}")

    for thr in (50, 70, 90, 110, 130):
        L, T, R, B = reaches(px, W, H, thr)
        print(
            f"[thr {thr:3}] leftWidth={L:4} topHeight={T:4} rightWidth={R:4} bottomHeight={B:4}"
            f"   (frac L={L/W:.3f} T={T/H:.3f} R={R/W:.3f} B={B/H:.3f})"
        )

    # render overlays for the two most likely thresholds
    for thr in (90, 110):
        L, T, R, B = reaches(px, W, H, thr)
        dbg = im.copy()
        d = ImageDraw.Draw(dbg)
        for x in (L, W - R):
            d.line([(x, 0), (x, H)], fill=(255, 0, 0, 255), width=3)
        for y in (T, H - B):
            d.line([(0, y), (W, y)], fill=(255, 0, 0, 255), width=3)
        p = OUT / f"_insets_thr{thr}.png"
        dbg.save(p)
        print(f"[debug] {p}")

    # crop the four corners so the ornament extent is directly visible
    im.crop((0, 0, 320, 300)).save(OUT / "_corner_TL.png")
    im.crop((W - 320, 0, W, 300)).save(OUT / "_corner_TR.png")
    print("[crop] _corner_TL.png _corner_TR.png")


if __name__ == "__main__":
    main()
