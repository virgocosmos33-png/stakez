"""Chroma-key the generated wide gothic frame and prep it as a HUD-ready asset.

Keys out the bright-green background to transparency, keeps the dark interior
recess (acts as the reel backing so no light leaks), desaturates the green
fringe, autocrops to the gold content, and reports the interior-opening ratios
so BoardFrame can size the frame with a uniform (non-distorting) scale.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

RAW = Path(
    r"C:\Users\xheih\.cursor\projects\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios\assets\mirror_frame_wide_raw.png"
)
OUT_DIR = Path(
    r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios\web-sdk\apps\ways\static\assets\sprites\mirror"
)
OUT = OUT_DIR / "mirror_frame_wide.png"
PREVIEW = OUT_DIR / "_wide_preview.png"

img = Image.open(RAW).convert("RGBA")
arr = np.array(img).astype(np.int32)
R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
greenness = G - np.maximum(R, B)

alpha = np.full(G.shape, 255, dtype=np.int32)
alpha[greenness >= 40] = 0
fringe = (greenness > 12) & (greenness < 40)
alpha[fringe] = (255 * (40 - greenness[fringe]) / (40 - 12)).astype(np.int32)

# kill green tint on any kept edge pixel
tint = greenness > 12
newG = G.copy()
newG[tint] = np.maximum(R, B)[tint]

out = np.dstack([R, newG, B, alpha]).astype(np.uint8)
im2 = Image.fromarray(out, "RGBA")
im2 = im2.crop(im2.getbbox())
im2.save(OUT)

# measure the interior opening via longest dark-opaque run per row (robust to
# dark patina scattered through the gold ornament)
a2 = np.array(im2)
W, H = im2.size
darkmask = (a2[..., 3] > 180) & (a2[..., 0] < 80) & (a2[..., 1] < 80) & (a2[..., 2] < 80)


def max_run(bool_row: np.ndarray) -> tuple[int, int]:
    if not bool_row.any():
        return 0, 0
    padded = np.concatenate(([0], bool_row.astype(np.int8), [0]))
    d = np.diff(padded)
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    lengths = ends - starts
    k = int(lengths.argmax())
    return int(lengths[k]), int(starts[k])


runs = [max_run(darkmask[y]) for y in range(H)]
interior = [(y, s, ln) for y, (ln, s) in enumerate(runs) if ln > 0.45 * W]
if interior:
    top = interior[0][0]
    bot = interior[-1][0]
    lefts = [s for _, s, _ in interior]
    rights = [s + ln for _, s, ln in interior]
    left = int(np.median(lefts))
    right = int(np.median(rights))
    open_w, open_h = right - left, bot - top
else:
    open_w = open_h = 0

print(f"asset      = {W} x {H}  (aspect {W/H:.3f})")
print(f"opening    = {open_w} x {open_h}  (aspect {open_w/max(open_h,1):.3f})")
print(f"openWfrac  = {open_w/W:.4f}")
print(f"openHfrac  = {open_h/H:.4f}")

bg = Image.new("RGBA", im2.size, (18, 16, 20, 255))
bg.alpha_composite(im2)
bg.convert("RGB").save(PREVIEW)
print(f"saved  {OUT}")
print(f"preview {PREVIEW}")
