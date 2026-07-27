"""Extract BLANK bet-chip ticket plates from user refs (no baked amounts).

Sources (Cursor assets refs):
  idle     — dark fill + distressed red notched border (was "50.00")
  selected — red distressed fill plate (was "5.00")

Outputs:
  web-sdk/packages/components-ui-html/src/assets/betMenu/
    bet_chip_idle.png
    bet_chip_selected.png
  + mirrors under apps/ways/static/assets/bet_menu_ui/ and node_modules package path
"""
from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[4]  # repo root (…/lady mirror drama studios)
ASSETS = Path(
    r"C:\Users\xheih\.cursor\projects"
    r"\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios\assets"
)

IDLE_REF = ASSETS / (
    "c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
    "image-70c76824-13d3-403c-8a69-f422f42a21c1.png"
)
SEL_REF = ASSETS / (
    "c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
    "image-789245fb-4c0f-4f2a-baf0-940946b2a5a3.png"
)

PKG = ROOT / "web-sdk/packages/components-ui-html/src/assets/betMenu"
NM = ROOT / "web-sdk/apps/ways/node_modules/components-ui-html/src/assets/betMenu"
STATIC = ROOT / "web-sdk/apps/ways/static/assets/bet_menu_ui"
SCALE = 5  # nearest upscale so plates stay crisp when CSS-scaled


def trim_alpha(rgba: np.ndarray, pad: int = 2) -> np.ndarray:
    ys, xs = np.where(rgba[:, :, 3] > 0)
    if len(xs) == 0:
        return rgba
    y0 = max(0, int(ys.min()) - pad)
    y1 = min(rgba.shape[0], int(ys.max()) + 1 + pad)
    x0 = max(0, int(xs.min()) - pad)
    x1 = min(rgba.shape[1], int(xs.max()) + 1 + pad)
    return rgba[y0:y1, x0:x1]


def key_black_canvas(rgba: np.ndarray, lum_thr: float = 14.0) -> np.ndarray:
    """Make near-black exterior transparent; keep plate interior + red border."""
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    redish = (r > 70) & (r > g + 20) & (r > b + 20)
    # Dilate red so thin distressed border crumbs aren't keyed out
    red_keep = ndimage.binary_dilation(redish, iterations=2)
    # Plate body: anything that is red-adjacent or clearly above pure black
    body = (lum > lum_thr) | red_keep
    body = ndimage.binary_closing(body, iterations=2)
    body = ndimage.binary_fill_holes(body)
    # Drop tiny exterior speckles
    labeled, n = ndimage.label(body)
    if n:
        sizes = ndimage.sum(body, labeled, range(1, n + 1))
        keep_lab = 1 + int(np.argmax(sizes))
        body = labeled == keep_lab
    out[:, :, 3] = np.where(body, 255, 0).astype(np.uint8)
    out[out[:, :, 3] == 0, :3] = 0
    return out


def inpaint_mask(rgba: np.ndarray, text: np.ndarray, fill_src: np.ndarray) -> np.ndarray:
    out = rgba.copy()
    if not text.any() or not fill_src.any():
        return out
    rgb = out[:, :, :3].astype(np.float32)
    dist, (iy, ix) = ndimage.distance_transform_edt(~fill_src, return_indices=True)
    for c in range(3):
        sampled = rgb[:, :, c][iy, ix]
        rgb[text, c] = sampled[text]
    plate_mean = rgb[fill_src].mean(axis=0)
    # Match local grain so the scrub doesn't look airbrushed
    rng = np.random.default_rng(11)
    grain = rng.normal(0, 3.5, size=rgb[text].shape)
    rgb[text] = 0.72 * rgb[text] + 0.28 * plate_mean + grain
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return out


def scrub_idle_text(rgba: np.ndarray) -> np.ndarray:
    """Remove light stencil numerals from dark idle plate; keep red border."""
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.float32)
    alpha = out[:, :, 3]
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    plate = alpha > 0
    redish = plate & (r > 70) & (r > g + 20) & (r > b + 20)
    # Protect outer rim (distress border)
    rim = plate & ~ndimage.binary_erosion(plate, iterations=4)
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    band = plate & (yy > h * 0.16) & (yy < h * 0.84) & (xx > w * 0.10) & (xx < w * 0.90)

    # Light / off-white stencil glyphs
    text = band & ~rim & ~redish & (lum > 55)
    text = ndimage.binary_dilation(text, iterations=1)
    text &= band & ~rim & ~redish

    fill_src = band & ~rim & ~redish & ~text & (lum < 45)
    out = inpaint_mask(out, text, fill_src)

    # Second pass: mid-grey glyph fringe
    rgb = out[:, :, :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    redish = plate & (r > 70) & (r > g + 20) & (r > b + 20)
    text2 = band & ~rim & ~redish & (lum > 38) & (lum < 160)
    text2 = ndimage.binary_dilation(text2, iterations=1)
    text2 &= band & ~rim & ~redish
    fill2 = band & ~rim & ~redish & ~text2 & (lum < 35)
    out = inpaint_mask(out, text2, fill2)

    # Hard center fill: any remaining brighter-than-fill pixels in the numeral band
    rgb = out[:, :, :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    redish = plate & (r > 70) & (r > g + 20) & (r > b + 20)
    dark_fill = band & ~rim & ~redish & (lum < 32)
    fill_mean = rgb[dark_fill].mean(axis=0) if dark_fill.any() else np.array([18.0, 14.0, 14.0])
    residual = band & ~rim & ~redish & (lum > fill_mean.mean() + 8)
    residual = ndimage.binary_dilation(residual, iterations=1) & band & ~rim & ~redish
    rng = np.random.default_rng(19)
    grain = rng.normal(0, 2.8, size=rgb.shape)
    for c in range(3):
        rgb[residual, c] = fill_mean[c] + grain[residual, c]
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return out


def scrub_selected_text(rgba: np.ndarray) -> np.ndarray:
    """Remove dark numerals from red selected plate; keep distressed red texture."""
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.float32)
    alpha = out[:, :, 3]
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    plate = alpha > 0
    redish = plate & (r > 70) & (r > g + 15) & (r > b + 15)
    rim = plate & ~ndimage.binary_erosion(plate, iterations=3)
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    band = plate & (yy > h * 0.16) & (yy < h * 0.84) & (xx > w * 0.10) & (xx < w * 0.90)

    # Black / near-black stencil on red
    text = band & ~rim & (lum < 48) & (r < 90)
    text = ndimage.binary_dilation(text, iterations=2)
    text &= band & ~rim

    fill_src = band & ~rim & redish & ~text & (lum > 55)
    out = inpaint_mask(out, text, fill_src)

    # Second pass for dark-red glyph shadows
    rgb = out[:, :, :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    r = rgb[:, :, 0]
    text2 = band & ~rim & (lum < 62) & (r < 110)
    text2 = ndimage.binary_dilation(text2, iterations=1)
    text2 &= band & ~rim
    fill2 = band & ~rim & ~text2 & (lum > 70)
    out = inpaint_mask(out, text2, fill2)

    # Hard center: push residual dark blotches toward local red mean + grain
    rgb = out[:, :, :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    redish = plate & (r > 70) & (r > g + 15) & (r > b + 15)
    red_fill = band & ~rim & redish & (lum > 70)
    fill_mean = rgb[red_fill].mean(axis=0) if red_fill.any() else np.array([150.0, 28.0, 32.0])
    residual = band & ~rim & (lum < fill_mean.mean() * 0.78)
    residual = ndimage.binary_dilation(residual, iterations=1) & band & ~rim
    rng = np.random.default_rng(23)
    grain = rng.normal(0, 5.0, size=rgb.shape)
    for c in range(3):
        rgb[residual, c] = fill_mean[c] + grain[residual, c]
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return out


def process(ref: Path, kind: str) -> Image.Image:
    im = Image.open(ref).convert("RGBA")
    arr = np.array(im)
    arr = key_black_canvas(arr, lum_thr=12.0 if kind == "idle" else 10.0)
    arr = trim_alpha(arr, pad=2)
    if kind == "idle":
        arr = scrub_idle_text(arr)
    else:
        arr = scrub_selected_text(arr)
    arr = trim_alpha(arr, pad=1)
    out = Image.fromarray(arr)
    if SCALE > 1:
        out = out.resize((out.width * SCALE, out.height * SCALE), Image.NEAREST)
    return out


def deploy(name: str, im: Image.Image) -> list[Path]:
    written: list[Path] = []
    for d in (PKG, NM, STATIC):
        d.mkdir(parents=True, exist_ok=True)
        dest = d / name
        im.save(dest, optimize=True)
        written.append(dest)
    return written


def main() -> None:
    assert IDLE_REF.is_file(), IDLE_REF
    assert SEL_REF.is_file(), SEL_REF

    idle = process(IDLE_REF, "idle")
    sel = process(SEL_REF, "selected")

    paths = []
    paths += deploy("bet_chip_idle.png", idle)
    paths += deploy("bet_chip_selected.png", sel)

    # Quick QA: center band should not contain bright white (idle) or black glyphs (sel)
    for label, im in (("idle", idle), ("selected", sel)):
        a = np.array(im.convert("RGBA"))
        rgb = a[:, :, :3].astype(np.float32)
        lum = rgb.mean(2)
        alpha = a[:, :, 3]
        h, w = lum.shape
        band = (alpha > 0) & (np.mgrid[0:h, 0:w][0] > h * 0.25) & (np.mgrid[0:h, 0:w][0] < h * 0.75)
        band &= (np.mgrid[0:h, 0:w][1] > w * 0.2) & (np.mgrid[0:h, 0:w][1] < w * 0.8)
        print(
            f"[{label}] size={im.size} band_lum mean={lum[band].mean():.1f} "
            f"p95={np.percentile(lum[band], 95):.1f} p05={np.percentile(lum[band], 5):.1f}"
        )

    for p in paths:
        print("wrote", p, p.stat().st_size)


if __name__ == "__main__":
    main()
