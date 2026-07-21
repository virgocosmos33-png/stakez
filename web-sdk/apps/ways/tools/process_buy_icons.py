"""Process the fresh transparent feature cutouts into the game's icon slots.

For each source PNG:
  - ensure RGBA + clean a faint alpha fringe (threshold low alpha to 0, which
    removes the semi-transparent halo left by matting),
  - autocrop to the alpha bounding box (drops transparent margins),
  - scale the subject to a consistent height and paste centered onto a fixed
    square canvas so every card icon reads at the same visual size,
  - save as LOSSLESS WebP WITH ALPHA over the existing buy_*.webp filenames the
    bet modes already point to (no other wiring changes).

Run from web-sdk/apps/ways:  python tools/process_buy_icons.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

SRC_DIR = Path(
    r"C:\Users\xheih\.cursor\projects"
    r"\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios\assets"
)
DST_DIR = Path("static/assets/sprites/mirror")

# source PNG stem -> destination webp filename (what betModeData.assets.icon uses)
MAP = {
    "mirror_buy_extrabet": "buy_ante.webp",
    "mirror_buy_mirrorspin": "buy_feature1.webp",
    "mirror_buy_twinmirrors": "buy_feature2.webp",
    "mirror_buy_triplemirrors": "buy_feature3.webp",
    "mirror_buy_seance": "buy_seance.webp",
    "mirror_buy_otherside": "buy_otherside.webp",
    "mirror_buy_bloodmoon": "buy_bloodmoon.webp",
}

CANVAS = 1024          # square output canvas
SUBJECT_FRAC = 0.92    # subject fits within this fraction of the canvas
FRINGE_ALPHA = 12      # alpha <= this becomes fully transparent (kills halo)


def clean_alpha(im: Image.Image) -> Image.Image:
    """Zero out any faint alpha fringe (vectorised via a point LUT on the alpha
    channel) — removes the semi-transparent matting halo without touching RGB."""
    im = im.convert("RGBA")
    r, g, b, a = im.split()
    a = a.point(lambda v: 0 if v <= FRINGE_ALPHA else v)
    return Image.merge("RGBA", (r, g, b, a))


def autocrop(im: Image.Image) -> Image.Image:
    bbox = im.split()[3].getbbox()  # bbox of non-zero alpha
    return im.crop(bbox) if bbox else im


def normalize(im: Image.Image) -> Image.Image:
    im = autocrop(clean_alpha(im))
    w, h = im.size
    target = int(CANVAS * SUBJECT_FRAC)
    scale = min(target / w, target / h)
    new = (max(1, round(w * scale)), max(1, round(h * scale)))
    im = im.resize(new, Image.LANCZOS)
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    ox = (CANVAS - new[0]) // 2
    oy = (CANVAS - new[1]) // 2
    canvas.alpha_composite(im, (ox, oy))
    return canvas


def alpha_stats(im: Image.Image) -> tuple[float, float]:
    a = im.split()[3]
    hist = a.histogram()
    total = sum(hist)
    transparent = hist[0] / total
    opaque = hist[255] / total
    return transparent, opaque


def main() -> None:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    for stem, dst_name in MAP.items():
        src = SRC_DIR / f"{stem}.png"
        if not src.exists():
            print(f"[MISS] {src}")
            continue
        im = Image.open(src)
        print(f"\n{stem}.png  in={im.size} mode={im.mode}", flush=True)
        out = normalize(im)
        tr, op = alpha_stats(out)
        dst = DST_DIR / dst_name
        out.save(dst, "WEBP", lossless=True, method=4)
        print(f"  -> {dst}  {out.size}  transparent={tr:.1%} opaque={op:.1%}", flush=True)
    print("\nDONE", flush=True)


if __name__ == "__main__":
    main()
