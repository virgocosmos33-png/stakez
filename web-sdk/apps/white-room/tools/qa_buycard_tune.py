"""Tune outer-black removal. Hysteresis flood-fill:

  bg_candidate = (luminance <= T_LO) AND connected to image border
  protect      = dilate(luminance >= T_HI, R)   # halo around real art
  background   = bg_candidate AND NOT protect

Then feather alpha ~1px and defringe dark edges. Preview each candidate over a
checkerboard, a LIGHT bg and a MID bg so we can spot halos/fringe.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage

DIR = Path("static/assets/sprites/mirror")
OUT = Path("tools/_buycard_preview")
OUT.mkdir(parents=True, exist_ok=True)

CROSS = np.array([[0,1,0],[1,1,1],[0,1,0]], bool)

def lum(arr):
    return arr[..., :3].astype(np.int32).max(axis=2)

def border_connected(mask):
    lbl, _ = ndimage.label(mask, structure=CROSS)
    bl = set(lbl[0,:]) | set(lbl[-1,:]) | set(lbl[:,0]) | set(lbl[:,-1])
    bl.discard(0)
    return np.isin(lbl, list(bl))

def make_bg(arr, t_lo, t_hi, r):
    L = lum(arr)
    cand = border_connected(L <= t_lo)
    protect = ndimage.binary_dilation(L >= t_hi, iterations=r)
    bg = cand & ~protect
    # re-flood: keep only bg still connected to border after protection carve-out
    bg = border_connected(bg)
    return bg

def comp_on(rgb, alpha, bg_color):
    a = (alpha[..., None] / 255.0)
    base = np.zeros_like(rgb); base[:] = bg_color
    return (rgb * a + base * (1 - a)).astype(np.uint8)

def checker(w, h, sq=24):
    c = np.zeros((h, w, 3), np.uint8)
    yy, xx = np.mgrid[0:h, 0:w]
    m = (((xx//sq)+(yy//sq)) % 2) == 0
    c[m] = 90; c[~m] = 150
    return c

TESTS = {
    "buy_otherside.webp": [(16, 70, 6), (24, 80, 8), (12, 60, 4)],
    "buy_ante.webp":      [(16, 70, 6), (24, 80, 8), (12, 60, 4)],
}

for name, params in TESTS.items():
    arr = np.asarray(Image.open(DIR/name).convert("RGBA"))
    rgb = arr[..., :3]
    for (t_lo, t_hi, r) in params:
        bg = make_bg(arr, t_lo, t_hi, r)
        alpha = np.where(bg, 0, 255).astype(np.uint8)
        # feather ~1px
        af = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.0))
        alpha = np.asarray(af)
        tag = f"{name}.lo{t_lo}_hi{t_hi}_r{r}"
        ch = checker(arr.shape[1], arr.shape[0])
        a = alpha[..., None]/255.0
        Image.fromarray((rgb*a + ch*(1-a)).astype(np.uint8)).save(OUT/f"{tag}.checker.png")
        Image.fromarray(comp_on(rgb, alpha, (225,225,230))).save(OUT/f"{tag}.light.png")
        print(f"{tag}  bg={bg.mean():5.1%}")
print("done")
