"""Turn the Scenario haunted-mirror texture into a clean counter-glass overlay.

Keeps the cracked scrying-glass + inner sigils, drops the outer oval frame and
corner smoke (which would fight the procedural pill frame), and bakes a soft
radial alpha vignette so the overlay fades to fully transparent before it
reaches the panel edge -- no mask or hard box needed. Alpha is driven by
luminance so the near-black background is invisible and only the violet detail
(smoke, sigils, crack highlights) shows when laid over the dark glass.

Output -> static/assets/sprites/mirror/counter_glass.png (RGBA)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[3] / "qa-shots" / "creatives" / "counter_texture.png"
DEST = HERE.parent / "static" / "assets" / "sprites" / "mirror" / "counter_glass.png"
SIZE = 640


def main() -> None:
    img = Image.open(SRC).convert("RGB")
    w, h = img.size
    # keep the sigil ring + inner glass, drop only the outer oval frame edge
    c = int(min(w, h) * 0.86)
    left, top = (w - c) // 2, (h - c) // 2
    crop = img.crop((left, top, left + c, top + c)).resize((SIZE, SIZE), Image.LANCZOS)
    # blur softens the sharp white crack lines into a smoky violet glow so the
    # overlay reads as haunted-glass atmosphere, not a broken screen
    crop = crop.filter(ImageFilter.GaussianBlur(4))

    arr = np.asarray(crop).astype(np.float32) / 255.0
    # push the palette toward the game's amethyst before deriving alpha
    arr[..., 0] = np.clip(arr[..., 0] * 1.05, 0.0, 1.0)
    arr[..., 2] = np.clip(arr[..., 2] * 1.15, 0.0, 1.0)
    lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    # lift the broad smoke/sigil mid-tones; the thin crack is dimmed by the blur
    alpha = np.clip(lum, 0.0, 1.0) ** 0.95

    # soft radial vignette: opaque core, fully transparent by the edge
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    r = np.sqrt(((xx - SIZE / 2) / (SIZE / 2)) ** 2 + ((yy - SIZE / 2) / (SIZE / 2)) ** 2)
    vignette = np.clip(1.0 - np.clip((r - 0.42) / 0.58, 0.0, 1.0), 0.0, 1.0)
    alpha = np.clip(alpha * vignette * 1.1, 0.0, 1.0)

    out = (np.dstack([arr, alpha]) * 255).astype(np.uint8)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out, "RGBA").save(DEST)
    print(f"wrote {DEST} ({DEST.stat().st_size} bytes, {SIZE}x{SIZE} RGBA)", flush=True)


if __name__ == "__main__":
    main()
