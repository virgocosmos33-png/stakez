"""Extract BLANK bet-stepper plates from user refs (no baked $ / − / +).

Sources (Cursor assets refs):
  rail  — full dark distressed bar with white border (was "$5.00" + −/+)
  plus  — red distressed square plate close-up (was light +)
  minus — red distressed square plate close-up (was light − bar)

Outputs:
  web-sdk/packages/components-ui-html/src/assets/betMenu/
    bet_stepper_rail.png
    bet_btn_minus.png
    bet_btn_plus.png
  + mirrors under apps/ways/static/assets/bet_menu_ui/ and node_modules package path

Blank centers — − / + / amount are HTML overlays in BetMenuAmountToggle.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[4]
ASSETS = Path(
    r"C:\Users\xheih\.cursor\projects"
    r"\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios\assets"
)

RAIL_REF = ASSETS / (
    "c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
    "image-75531ee4-819b-4bfd-acc9-ca95e11084fd.png"
)
PLUS_REF = ASSETS / (
    "c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
    "image-89120417-5ec4-4881-b3f6-2f87e5e146e6.png"
)
MINUS_REF = ASSETS / (
    "c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
    "image-63439c56-27ec-4c49-904f-df75fec20fff.png"
)

PKG = ROOT / "web-sdk/packages/components-ui-html/src/assets/betMenu"
NM = ROOT / "web-sdk/apps/ways/node_modules/components-ui-html/src/assets/betMenu"
STATIC = ROOT / "web-sdk/apps/ways/static/assets/bet_menu_ui"
SCALE = 4


def trim_alpha(rgba: np.ndarray, pad: int = 2) -> np.ndarray:
    ys, xs = np.where(rgba[:, :, 3] > 0)
    if len(xs) == 0:
        return rgba
    y0 = max(0, int(ys.min()) - pad)
    y1 = min(rgba.shape[0], int(ys.max()) + 1 + pad)
    x0 = max(0, int(xs.min()) - pad)
    x1 = min(rgba.shape[1], int(xs.max()) + 1 + pad)
    return rgba[y0:y1, x0:x1]


def key_rail_body(rgba: np.ndarray) -> np.ndarray:
    """Keep full horizontal rail (dark fill is near-black — can't lum-threshold).

    Button squares close via fill_holes and win as the 'largest' blob, so we
    instead take the bbox of the white/red edge (the outer rail frame).
    """
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    white = (lum > 35) & ~((r > g + 35) & (r > b + 35))
    red = (r > 70) & (r > g + 18) & (r > b + 18)
    edge = ndimage.binary_dilation(white | red, iterations=1)
    ys, xs = np.where(edge)
    if len(xs) == 0:
        return out
    pad = 2
    y0 = max(0, int(ys.min()) - pad)
    y1 = min(out.shape[0], int(ys.max()) + 1 + pad)
    x0 = max(0, int(xs.min()) - pad)
    x1 = min(out.shape[1], int(xs.max()) + 1 + pad)
    body = np.zeros(lum.shape, dtype=bool)
    body[y0:y1, x0:x1] = True
    out[:, :, 3] = np.where(body, 255, 0).astype(np.uint8)
    out[out[:, :, 3] == 0, :3] = 0
    return out


def key_btn_body(rgba: np.ndarray) -> np.ndarray:
    """Square plate: keep red border + dark fill inside."""
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    red = (r > 70) & (r > g + 18) & (r > b + 18)
    light = (lum > 40) & ~red
    edge = ndimage.binary_closing(red | light, iterations=2)
    body = ndimage.binary_fill_holes(ndimage.binary_dilation(edge, iterations=2))
    labeled, n = ndimage.label(body)
    if n:
        sizes = ndimage.sum(body, labeled, range(1, n + 1))
        body = labeled == (1 + int(np.argmax(sizes)))
    out[:, :, 3] = np.where(body, 255, 0).astype(np.uint8)
    out[out[:, :, 3] == 0, :3] = 0
    return out


def hard_fill(rgba: np.ndarray, mask: np.ndarray, seed: int = 11) -> np.ndarray:
    """Paint mask with local dark-fill mean + grain."""
    out = rgba.copy()
    if not mask.any():
        return out
    rgb = out[:, :, :3].astype(np.float32)
    alpha = out[:, :, 3]
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    plate = alpha > 0
    redish = (r > 80) & (r > g + 20) & (r > b + 20)
    fill_src = plate & ~mask & (lum < 28) & ~redish
    fill_mean = rgb[fill_src].mean(axis=0) if fill_src.any() else np.array([12.0, 10.0, 10.0])
    rng = np.random.default_rng(seed)
    grain = rng.normal(0, 3.0, size=rgb.shape)
    for c in range(3):
        rgb[mask, c] = fill_mean[c] + grain[mask, c]
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return out


def scrub_rail(rgba: np.ndarray) -> np.ndarray:
    """Blank rail: keep white outer border + dark texture; remove $ / − / + / button frames."""
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.float32)
    alpha = out[:, :, 3]
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    plate = alpha > 0
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]

    # Protect thin outer white rim only
    rim = plate & ~ndimage.binary_erosion(plate, iterations=5)

    # Interior between outer white rim — wipe amount, −/+, and baked button frames
    # so HTML can sit on separate bet_btn_* plates without double borders.
    interior = ndimage.binary_erosion(plate, iterations=5)
    # Keep subtle dark-red splatters near the far-right edge of the rail (brand texture)
    # by only hard-wiping left/center/right content bands, not the whole interior once.
    left = interior & (xx < w * 0.26)
    right = interior & (xx > w * 0.74)
    center = interior & (xx >= w * 0.26) & (xx <= w * 0.74)

    redish = (r > 70) & (r > g + 18) & (r > b + 18)
    light = lum > 32
    red_amount = (r > 100) & (r > g + 35) & (r > b + 35)

    # Button zones: wipe everything (frames + glyphs) to dark fill
    btn_wipe = (left | right)
    # Center: wipe amount + any leftover light/red glyphs; leave dark grain
    center_wipe = center & (light | red_amount | redish)
    erase = ndimage.binary_dilation(btn_wipe | center_wipe, iterations=1) & interior
    out = hard_fill(out, erase, seed=21)

    # Second pass: residual bright / red in content bands
    rgb = out[:, :, :3].astype(np.float32)
    lum = rgb.mean(axis=2)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    plate = out[:, :, 3] > 0
    interior = ndimage.binary_erosion(plate, iterations=5)
    left = interior & (xx < w * 0.26)
    right = interior & (xx > w * 0.74)
    center = interior & (xx >= w * 0.26) & (xx <= w * 0.74)
    residual = (left | right) | (
        center & ((lum > 28) | ((r > 85) & (r > g + 25) & (r > b + 25)))
    )
    residual = ndimage.binary_dilation(residual, iterations=1) & interior
    out = hard_fill(out, residual, seed=27)
    return out


def scrub_btn(rgba: np.ndarray) -> np.ndarray:
    """Blank square: keep red distressed border; scrub center glyph hard.

    Glyphs carry red speckles, so color-based 'redish' protect wrongly keeps them.
    Use a morphological rim only — wipe everything inside that rim.
    """
    out = rgba.copy()
    plate = out[:, :, 3] > 0
    # ~6px rim keeps the distressed red frame; interior is forced blank
    interior = ndimage.binary_erosion(plate, iterations=6)
    if not interior.any():
        interior = ndimage.binary_erosion(plate, iterations=3)
    out = hard_fill(out, interior, seed=41)
    return out


def upscale(im: Image.Image) -> Image.Image:
    if SCALE <= 1:
        return im
    return im.resize((im.width * SCALE, im.height * SCALE), Image.NEAREST)


def process_rail(ref: Path) -> Image.Image:
    arr = np.array(Image.open(ref).convert("RGBA"))
    arr = key_rail_body(arr)
    arr = trim_alpha(arr, pad=2)
    arr = scrub_rail(arr)
    arr = trim_alpha(arr, pad=1)
    return upscale(Image.fromarray(arr))


def process_btn(ref: Path) -> Image.Image:
    arr = np.array(Image.open(ref).convert("RGBA"))
    arr = key_btn_body(arr)
    arr = trim_alpha(arr, pad=2)
    arr = scrub_btn(arr)
    arr = trim_alpha(arr, pad=1)
    return upscale(Image.fromarray(arr))


def pad_square(im: Image.Image, side: int) -> Image.Image:
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return canvas


def deploy(name: str, im: Image.Image) -> list[Path]:
    written: list[Path] = []
    for d in (PKG, NM, STATIC):
        d.mkdir(parents=True, exist_ok=True)
        dest = d / name
        im.save(dest, optimize=True)
        written.append(dest)
    return written


def qa_band(label: str, im: Image.Image) -> None:
    a = np.array(im.convert("RGBA"))
    rgb = a[:, :, :3].astype(np.float32)
    lum = rgb.mean(2)
    alpha = a[:, :, 3]
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    band = (alpha > 0) & (yy > h * 0.30) & (yy < h * 0.70) & (xx > w * 0.30) & (xx < w * 0.70)
    print(
        f"[{label}] size={im.size} band_lum mean={lum[band].mean():.1f} "
        f"p95={np.percentile(lum[band], 95):.1f} p05={np.percentile(lum[band], 5):.1f}"
    )


def main() -> None:
    assert RAIL_REF.is_file(), RAIL_REF
    assert PLUS_REF.is_file(), PLUS_REF
    assert MINUS_REF.is_file(), MINUS_REF

    rail = process_rail(RAIL_REF)
    minus = process_btn(MINUS_REF)
    plus = process_btn(PLUS_REF)

    side = max(minus.width, plus.width, minus.height, plus.height)
    minus = pad_square(minus, side)
    plus = pad_square(plus, side)

    paths = []
    paths += deploy("bet_stepper_rail.png", rail)
    paths += deploy("bet_btn_minus.png", minus)
    paths += deploy("bet_btn_plus.png", plus)

    for label, im in (("rail", rail), ("minus", minus), ("plus", plus)):
        qa_band(label, im)

    for p in paths:
        print("wrote", p, p.stat().st_size)


if __name__ == "__main__":
    main()
