"""Prepare the SPIN button rotate icon as a clean WHITE monochrome HUD asset.

Source icon: Flaticon "Rotate" free icon (id 11067218).
    https://www.flaticon.com/free-icon/rotate_11067218

Pipeline:
    1. Read the raw downloaded original (``spin_rotate_src.png``).
    2. Recolor every pixel to pure white (0xFFFFFF) while PRESERVING the alpha
       channel, so anti-aliased edges stay crisp and negative-space holes stay
       transparent.
    3. Trim excess transparent padding (crop to the alpha bounding box).
    4. Re-center on a square, fully-transparent canvas with a small even margin.
    5. Write the HUD-ready ``spin_rotate.png``.

Re-run any time from ``web-sdk/apps/ways``:
    python tools/make_spin_icon.py

Both input and output default to
``static/assets/sprites/hud/`` relative to this script.
"""

from __future__ import annotations

import argparse
import os

from PIL import Image

# tools/ -> ways/ -> static/assets/sprites/hud/
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_HUD_DIR = os.path.normpath(
    os.path.join(_SCRIPT_DIR, "..", "static", "assets", "sprites", "hud")
)

DEFAULT_SRC = os.path.join(_HUD_DIR, "spin_rotate_src.png")
DEFAULT_OUT = os.path.join(_HUD_DIR, "spin_rotate.png")

# Small even margin around the trimmed icon, as a fraction of the icon's
# longest side (per edge).
MARGIN_FRACTION = 0.08


def whiten_preserving_alpha(img: Image.Image) -> Image.Image:
    """Return an RGBA copy with every pixel forced to white, alpha untouched."""
    rgba = img.convert("RGBA")
    alpha = rgba.getchannel("A")
    white = Image.new("L", rgba.size, 255)
    return Image.merge("RGBA", (white, white, white, alpha))


def trim_and_center(img: Image.Image, margin_fraction: float = MARGIN_FRACTION) -> Image.Image:
    """Crop to the opaque content, then center it on a square transparent canvas."""
    bbox = img.getbbox()  # bounds of all non-fully-transparent pixels
    if bbox is None:
        raise ValueError("Source image is fully transparent; nothing to process.")

    cropped = img.crop(bbox)
    cw, ch = cropped.size
    side = max(cw, ch)
    margin = round(side * margin_fraction)
    canvas_size = side + margin * 2

    canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 0))
    offset = ((canvas_size - cw) // 2, (canvas_size - ch) // 2)
    canvas.paste(cropped, offset)
    return canvas


def build(src_path: str, out_path: str) -> None:
    src = Image.open(src_path)
    print(f"[in ] {src_path}  size={src.size}  mode={src.mode}")

    white = whiten_preserving_alpha(src)
    print(f"[trim] content bbox={white.getbbox()}")

    final = trim_and_center(white)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    final.save(out_path, "PNG")

    a = final.getchannel("A")
    print(f"[out] {out_path}  size={final.size}  mode={final.mode}  alpha_extrema={a.getextrema()}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", default=DEFAULT_SRC, help="Raw source PNG (original download).")
    parser.add_argument("--out", default=DEFAULT_OUT, help="HUD-ready white PNG output.")
    args = parser.parse_args()
    build(args.src, args.out)


if __name__ == "__main__":
    main()
