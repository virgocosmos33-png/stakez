"""Bake the WAYS / WIN readout plaque for the left rail.

Input  : assets-raw/special_bar/readout_<pick>.png  (Layer GPT Image 2, ornate
         cast-iron/bronze nameplate with an EMPTY dark inset, on a flat white pad)
Output : static/assets/sprites/tombstone/bar_readout_plaque.png  (key `barReadoutPlaque`)

The gen lands on a ~#fefefe pad. We key the BORDER-CONNECTED white to alpha with a
SOFT matte (so the filigree silhouette has no white halo and no hard jaggies),
un-white the partial-alpha edge pixels, trim to the ornament, and report the dark
inset panel as fractions of the sprite so SpecialBar can seat the gold text inside
it (same opening contract as bar_plaque).

Run:  python tools/make_readout_plaque.py [readout_b]
"""

from __future__ import annotations

import os
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "assets-raw", "special_bar"))
OUT = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "tombstone"))

# background key: a pixel counts as removable pad only if it is bright and nearly
# neutral (grey/white). Warm gold specular on the metal is chromatic and survives.
BG_MIN = 208          # min(r,g,b) at/above this can be background
BG_CHROMA = 26        # max(r,g,b) - min(r,g,b) at/below this is neutral
EDGE_RAMP = 46.0      # soft-matte width: 255->transparent down to (255-RAMP)->opaque


def load(pick: str) -> np.ndarray:
    path = os.path.join(RAW, f"{pick}.png")
    if not os.path.isfile(path):
        raise SystemExit(f"missing plaque gen: {path}")
    return np.asarray(Image.open(path).convert("RGB")).astype(np.float32)


def background_mask(rgb: np.ndarray) -> np.ndarray:
    """Flood from the border through bright neutral pixels — the pad and the white
    showing THROUGH the filigree, never the dark inset (it is not border-reachable
    and not bright)."""
    h, w, _ = rgb.shape
    minc = rgb.min(axis=2)
    maxc = rgb.max(axis=2)
    passable = (minc >= BG_MIN) & ((maxc - minc) <= BG_CHROMA)
    seen = np.zeros((h, w), bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            if passable[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if passable[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny, nx] and passable[ny, nx]:
                seen[ny, nx] = True
                q.append((nx, ny))
    return seen


def key(rgb: np.ndarray) -> Image.Image:
    bg = background_mask(rgb)
    minc = rgb.min(axis=2)
    # soft matte only inside the reachable background: 255->0 alpha, ramp to opaque
    alpha = np.where(bg, np.clip((255.0 - minc) / EDGE_RAMP, 0.0, 1.0), 1.0)
    # un-white the partial edge so no grey/white halo bleeds around the filigree:
    # assume edge = plaque over white pad, recover the plaque colour.
    out = rgb.copy()
    partial = (alpha > 0.02) & (alpha < 0.98)
    a = alpha[partial][:, None]
    out[partial] = np.clip((rgb[partial] - (1.0 - a) * 255.0) / np.clip(a, 0.05, 1.0), 0, 255)
    rgba = np.dstack([out, alpha * 255.0]).astype(np.uint8)
    img = Image.fromarray(rgba, "RGBA")
    # feather the alpha a hair so the flood boundary is not a stair-step
    a_ch = img.getchannel("A").filter(ImageFilter.GaussianBlur(0.6))
    img.putalpha(a_ch)
    return img


def alpha_crop(img: Image.Image, pad: int = 4) -> Image.Image:
    box = img.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    if box is None:
        raise SystemExit("keyed to nothing — check BG thresholds / input")
    l = max(box[0] - pad, 0)
    t = max(box[1] - pad, 0)
    r = min(box[2] + pad, img.width)
    b = min(box[3] + pad, img.height)
    return img.crop((l, t, r, b))


def report_opening(img: Image.Image) -> dict:
    """Dark inset panel bbox as fractions — where the readout text is seated."""
    arr = np.asarray(img)
    lum = 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]
    dark = (arr[..., 3] > 160) & (lum < 70)
    ys, xs = np.where(dark)
    if len(xs) == 0:
        raise SystemExit("no dark inset found — is the panel empty & dark?")
    # largest central cluster: clamp to the middle 80% to ignore stray dark specks
    h, w = lum.shape
    keep = (xs > w * 0.08) & (xs < w * 0.92) & (ys > h * 0.08) & (ys < h * 0.92)
    xs, ys = xs[keep], ys[keep]
    x0, x1 = xs.min() / w, xs.max() / w
    y0, y1 = ys.min() / h, ys.max() / h
    return {"x0": round(float(x0), 4), "x1": round(float(x1), 4),
            "y0": round(float(y0), 4), "y1": round(float(y1), 4)}


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    pick = sys.argv[1] if len(sys.argv) > 1 else "readout_b"
    art = alpha_crop(key(load(pick)))
    out_path = os.path.join(OUT, "bar_readout_plaque.png")
    art.save(out_path, optimize=True)
    opening = report_opening(art)
    print(f"[readout] {pick} -> {out_path} {art.width}x{art.height} "
          f"({os.path.getsize(out_path):,} B)")
    print(f"[readout] aspect {art.width / art.height:.4f}")
    print(f"[readout] opening {opening}")


if __name__ == "__main__":
    main()
