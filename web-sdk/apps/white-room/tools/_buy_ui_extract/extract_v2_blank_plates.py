"""Build BLANK distressed CTA/ribbon plates from correct refs — NO baked text."""
from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "v2"
OUT.mkdir(exist_ok=True)

CTA_REF = Path(
    r"C:\Users\xheih\.cursor\projects\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
    r"\assets\c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
    r"image-89668409-54d1-48ae-a100-919cb48b3448.png"
)
RIBBON_REF = Path(
    r"C:\Users\xheih\.cursor\projects\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
    r"\assets\c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
    r"image-d0f78a98-b559-4c3f-9eec-e80b82977ddf.png"
)

PKG = Path(
    r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios"
    r"\web-sdk\packages\components-ui-html\src\assets\buyBonus"
)
NM = Path(
    r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios"
    r"\web-sdk\apps\ways\node_modules\components-ui-html\src\assets\buyBonus"
)
MIRROR_DIRS = [
    Path(
        r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios"
        r"\web-sdk\apps\ways\assets\sprites\mirror\buy_ui"
    ),
    Path(
        r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios"
        r"\web-sdk\apps\ways\static\assets\sprites\mirror\buy_ui"
    ),
]

SCALE = 6

RIBBON_ALIASES = [
    "ribbon_blank",
    "ribbon_scatter",
    "ribbon_observation",
    "ribbon_observation_plus",
    "ribbon_observation_plusplus",
    "ribbon_fractured",
    "ribbon_deepness",
]


def trim_alpha(rgba: np.ndarray, pad: int = 1) -> np.ndarray:
    ys, xs = np.where(rgba[:, :, 3] > 0)
    if len(xs) == 0:
        return rgba
    y0 = max(0, ys.min() - pad)
    y1 = min(rgba.shape[0], ys.max() + 1 + pad)
    x0 = max(0, xs.min() - pad)
    x1 = min(rgba.shape[1], xs.max() + 1 + pad)
    return rgba[y0:y1, x0:x1]


def upscale_nn(im: Image.Image, scale: int = SCALE) -> Image.Image:
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def inpaint_dark_text(rgba: np.ndarray, plate_mask: np.ndarray, dark_thr: float) -> np.ndarray:
    """Replace dark lettering with local plate color (distance-weighted fill)."""
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.float32)
    alpha = out[:, :, 3]
    lum = rgb.mean(axis=2)
    text = (lum < dark_thr) & (alpha > 0) & plate_mask
    # Expand a bit so antialiased glyph edges are scrubbed
    text = ndimage.binary_dilation(text, iterations=1)
    text &= plate_mask & (alpha > 0)

    fill_src = plate_mask & (alpha > 0) & ~text & (lum >= dark_thr)
    if not fill_src.any() or not text.any():
        return out

    # For each channel, fill text pixels with mean of nearby non-text plate pixels
    # Use morphological reconstruction via distance transform sampling
    dist, (iy, ix) = ndimage.distance_transform_edt(~fill_src, return_indices=True)
    for c in range(3):
        sampled = rgb[:, :, c][iy, ix]
        rgb[text, c] = sampled[text]
    # Slight noise match: blend with global plate mean so flat glyphs don't look patched
    plate_mean = rgb[fill_src].mean(axis=0)
    rgb[text] = 0.65 * rgb[text] + 0.35 * plate_mean
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return out


def hard_scrub_cta_band(rgba: np.ndarray) -> np.ndarray:
    """Nuke residual lettering ghosts in the CTA center band; keep edge distress."""
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.float32)
    alpha = out[:, :, 3]
    lum = rgb.mean(axis=2)
    plate = alpha > 0
    pink = plate & (rgb[:, :, 0] > 90) & (rgb[:, :, 0] > rgb[:, :, 1] + 20)
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    band = plate & (yy > h * 0.18) & (yy < h * 0.82) & (xx > w * 0.06) & (xx < w * 0.94)
    pink_mean = rgb[pink].mean(axis=0) if pink.any() else np.array([200.0, 40.0, 120.0])
    darker = band & (lum < pink_mean.mean() * 0.97)
    greyish = band & (np.abs(rgb[:, :, 0] - rgb[:, :, 1]) < 40) & (lum < 180)
    scrub = ndimage.binary_dilation(darker | greyish, iterations=1) & band
    edge = plate & ~ndimage.binary_erosion(plate, iterations=2)
    scrub &= ~edge
    rng = np.random.default_rng(7)
    grain = rng.normal(0, 4.0, size=rgb.shape)
    for c in range(3):
        rgb[scrub, c] = pink_mean[c] + grain[scrub, c]
    nonpink = band & ~edge & ~((rgb[:, :, 0] > 110) & (rgb[:, :, 0] > rgb[:, :, 1] + 25))
    for c in range(3):
        rgb[nonpink, c] = pink_mean[c] + grain[nonpink, c]
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return out


def extract_cta_blank() -> Image.Image:
    im = Image.open(CTA_REF).convert("RGBA")
    a = np.array(im)
    rgb = a[:, :, :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    pinkish = (rgb[:, :, 0] > 90) & (rgb[:, :, 0] > rgb[:, :, 1] + 25)
    pink_d = ndimage.binary_dilation(pinkish, iterations=2)
    is_canvas = (lum < 18) & ~pink_d
    out = a.copy()
    out[:, :, 3] = np.where(is_canvas, 0, 255).astype(np.uint8)
    out[out[:, :, 3] == 0, :3] = 0
    out = trim_alpha(out, pad=1)

    plate = out[:, :, 3] > 0
    # Scrub ACTIVATE lettering
    out = inpaint_dark_text(out, plate, dark_thr=70)
    # Second pass for residual mid-grey glyph fringe
    out = inpaint_dark_text(out, plate, dark_thr=95)
    out = hard_scrub_cta_band(out)
    return Image.fromarray(out)


def make_buy_blank(activate_blank: Image.Image) -> Image.Image:
    a = np.array(activate_blank.convert("RGBA"))
    rgb = a[:, :, :3].astype(np.float32)
    alpha = a[:, :, 3]
    plate = alpha > 0
    # Recolor pink → cool grey, preserve luminance/distress
    pink_lum = (0.35 * rgb[:, :, 0] + 0.35 * rgb[:, :, 1] + 0.30 * rgb[:, :, 2]) / 255.0
    base = 118 + 78 * pink_lum
    grey = np.stack([base * 0.96, base * 0.98, base * 1.03], axis=2)
    # Keep non-pink edge splatters (near-black crumbs) as-is
    is_pink = (rgb[:, :, 0] > 80) & (rgb[:, :, 0] > rgb[:, :, 1] + 15) & plate
    for c in range(3):
        ch = rgb[:, :, c]
        ch[is_pink] = grey[:, :, c][is_pink]
        rgb[:, :, c] = ch
    # Soften residual magenta in edge crumbs toward grey
    magenta_edge = plate & (rgb[:, :, 0] > rgb[:, :, 1] + 25) & (rgb[:, :, 0] > 60)
    for c in range(3):
        rgb[magenta_edge, c] = grey[magenta_edge, c]
    a[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(a)


def extract_ribbon_blank() -> Image.Image:
    im = Image.open(RIBBON_REF).convert("RGBA")
    a = np.array(im)
    rgb = a[:, :, :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    paper = lum > 85
    paper_d = ndimage.binary_dilation(paper, iterations=2)
    is_canvas = (lum < 28) & ~paper_d
    out = a.copy()
    out[:, :, 3] = np.where(is_canvas, 0, 255).astype(np.uint8)
    out[out[:, :, 3] == 0, :3] = 0
    out = trim_alpha(out, pad=1)
    plate = out[:, :, 3] > 0
    # Scrub OBSERVATION+ (and any edge ink that is lettering)
    out = inpaint_dark_text(out, plate, dark_thr=85)
    out = inpaint_dark_text(out, plate, dark_thr=110)
    # Final: force remaining dark interior pixels toward paper mean (keep edge grit)
    rgb = out[:, :, :3].astype(np.float32)
    alpha = out[:, :, 3]
    lum = rgb.mean(axis=2)
    h, w = lum.shape
    # Interior = eroded plate (protect organic edge silhouette)
    interior = ndimage.binary_erosion(plate, iterations=3)
    paper_px = interior & (lum > 120)
    paper_mean = rgb[paper_px].mean(axis=0) if paper_px.any() else np.array([220.0, 218.0, 214.0])
    residual = interior & (lum < 130)
    for c in range(3):
        rgb[residual, c] = paper_mean[c]
    # Add tiny grain so fill isn't flat plastic
    rng = np.random.default_rng(42)
    grain = rng.normal(0, 3.5, size=rgb.shape)
    rgb[residual] = np.clip(rgb[residual] + grain[residual], 0, 255)
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(out)


def write_all(name: str, im: Image.Image) -> Path:
    src = OUT / f"{name}_src.png"
    up = upscale_nn(im)
    up_path = OUT / f"{name}.png"
    im.save(src)
    up.save(up_path)
    return up_path


def deploy(path: Path, name: str) -> None:
    targets = [PKG, NM, *MIRROR_DIRS]
    for d in targets:
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, d / f"{name}.png")


def main() -> None:
    cta = extract_cta_blank()
    buy = make_buy_blank(cta)
    rib = extract_ribbon_blank()

    cta_p = write_all("cta_activate", cta)
    buy_p = write_all("cta_buy", buy)
    rib_p = write_all("ribbon_blank", rib)

    deploy(cta_p, "cta_activate")
    deploy(buy_p, "cta_buy")
    # All ribbon names = same blank plate (HTML labels supply text)
    for alias in RIBBON_ALIASES:
        write_all(alias, rib) if alias != "ribbon_blank" else None
        deploy(rib_p, alias)

    # Sanity: count dark interior pixels remaining
    for label, im in (("cta", cta), ("buy", buy), ("rib", rib)):
        a = np.array(im)
        plate = a[:, :, 3] > 0
        interior = ndimage.binary_erosion(plate, iterations=2)
        dark = interior & (a[:, :, :3].mean(axis=2) < 80)
        print(f"{label}: size={im.size} dark_interior_px={int(dark.sum())}")

    print("BLANK plates deployed to", PKG)


if __name__ == "__main__":
    main()
