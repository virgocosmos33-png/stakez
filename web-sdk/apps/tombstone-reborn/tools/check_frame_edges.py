"""Measure whether a baked frame shows a bright hairline at real display size.

The repeated bug in this project: a 1-3px bright stroke baked into a large frame
texture and drawn much smaller samples a single bright texel under GPU
minification and comes back as a crisp outline tracing the panel. A full-size
look at the PNG hides it, because at 1428px the stroke is honestly 3px of gold.

So this downsamples each frame to the size it is actually drawn at (~563px wide
for the win takeover on a 1280x800 viewport), composites it over the graveyard
dark, and reports the brightest ring of pixels just outside the hero window
against the timber behind it. A large gap is a hairline; a small gap means the
edge is carried by broad forms and light.

NEAREST is reported alongside LANCZOS because it is the worst case a GPU can hit
without mipmaps, and it is what actually shipped the artifact before.

Usage:  python tools/check_frame_edges.py [--display 563]
Output: qa-shots/frame-edges/<name>.png  (4x zoom of the top-left window corner)
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
from PIL import Image

APP = Path(__file__).resolve().parents[1]
CELEB = APP / "static" / "assets" / "sprites" / "celeb"
OUT = APP / "qa-shots" / "frame-edges"

# file -> (window pad in 1280-plate space, whether an outline is WANTED)
# The win takeover was asked to drop its panel outline and carry the edge with
# light; the bonus banner was asked to keep its framing. Both expectations are
# asserted here so neither can drift into the other.
FRAMES: dict[str, tuple[int, bool]] = {
    "win_frame.png": (74, False),
    "bonus_frame_small.png": (74, True),
    "bonus_frame_super.png": (112, True),
}

GRAVEYARD_DARK = (18, 16, 14)
ZOOM = 4
# A hairline is a NARROW bright feature: brighter than the timber on BOTH sides.
# Scoring it as the SMALLER of the two differences is what separates it from the
# two things that are supposed to be there — a wide warm gradient (no local peak
# at all) and a step where timber meets the iron band (bright on one side only).
LINE_SCORE = 8.0


def band_profiles(art: Image.Image, pad: float) -> list[np.ndarray]:
    """Luma from the window edge outward, per edge, averaged along that edge.

    Only the middle half of each edge is sampled: the corner straps are legitimate
    broad forms and would otherwise swamp the profile.
    """
    luma = np.asarray(art.convert("L")).astype(np.float32)
    height, width = luma.shape
    inner = int(round(pad))
    depth = max(4, inner - 1)
    quarter_x = slice(width // 4, width - width // 4)
    quarter_y = slice(height // 4, height - height // 4)
    edges = [
        luma[inner - depth : inner, quarter_x].mean(axis=1)[::-1],
        luma[height - inner : height - inner + depth, quarter_x].mean(axis=1),
        luma[quarter_y, inner - depth : inner].mean(axis=0)[::-1],
        luma[quarter_y, width - inner : width - inner + depth].mean(axis=0),
    ]
    return [edge for edge in edges if edge.size >= 7]


EDGE_NAMES = ("top", "bottom", "left", "right")


def line_score(profiles: list[np.ndarray]) -> tuple[float, str]:
    """Sharpest narrow bright ridge in the band, and where it sits.

    The distance is measured OUTWARD from the hero window, so `top+2px` is a line
    hugging the panel (the reported artifact) while `top+60px` is a feature out at
    the frame's outer edge, such as a branded plaque.
    """
    best = 0.0
    where = "none"
    for edge, profile in enumerate(profiles):
        for index in range(2, profile.size - 2):
            ridge = min(
                profile[index] - profile[index - 2], profile[index] - profile[index + 2]
            )
            if ridge > best:
                best = float(ridge)
                where = f"{EDGE_NAMES[edge]}+{index}px"
    return best, where


def check(name: str, pad: int, wants_outline: bool, display: int) -> bool:
    path = CELEB / name
    if not path.is_file():
        print(f"  {name:24s} MISSING")
        return False
    art = Image.open(path).convert("RGBA")
    scale = display / art.width
    size = (display, max(1, int(round(art.height * scale))))
    verdicts = []
    for label, filter_ in (("lanczos", Image.LANCZOS), ("nearest", Image.NEAREST)):
        small = art.resize(size, filter_)
        plate = Image.new("RGBA", size, (*GRAVEYARD_DARK, 255))
        plate.alpha_composite(small)
        score, where = line_score(band_profiles(plate, pad * scale))
        verdicts.append((label, score, where))
        if label == "lanczos":
            inner = int(round(pad * scale))
            crop = plate.crop((0, 0, inner + 26, inner + 26)).resize(
                ((inner + 26) * ZOOM, (inner + 26) * ZOOM), Image.NEAREST
            )
            OUT.mkdir(parents=True, exist_ok=True)
            crop.convert("RGB").save(OUT / name.replace(".png", "_corner.png"))
    worst = max(score for _, score, _ in verdicts)
    has_outline = worst > LINE_SCORE
    ok = has_outline == wants_outline
    detail = "  ".join(
        f"{label}: line={score:5.1f} at {where:11s}" for label, score, where in verdicts
    )
    print(
        f"  {name:24s} {detail}  outline={'YES' if has_outline else 'no ':3s} "
        f"want={'YES' if wants_outline else 'no ':3s} {'ok' if ok else 'FAIL'}"
    )
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--display",
        type=int,
        default=563,
        help="width the frame is actually drawn at, in canvas pixels",
    )
    args = parser.parse_args()
    print(f"frame edges at {args.display}px display width (baked at 1428/1504px):")
    results = [
        check(name, pad, wants, args.display) for name, (pad, wants) in FRAMES.items()
    ]
    print(f"corner zooms -> {os.path.relpath(OUT, APP)}")
    print("PASS" if all(results) else "FAIL")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
