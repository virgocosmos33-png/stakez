"""Extract distressed CTA/ribbon plates from correct user refs (NOT zigzag)."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

SCALE = 6  # nearest-neighbor upscale for crisp pixel look


def key_black_bg(rgba: np.ndarray, thr: int = 22) -> np.ndarray:
    rgb = rgba[:, :, :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    is_bg = (lum < thr) & (rgb[:, :, 0] < thr + 12) & (rgb[:, :, 1] < thr + 12) & (rgb[:, :, 2] < thr + 12)
    out = rgba.copy()
    out[:, :, 3] = np.where(is_bg, 0, 255).astype(np.uint8)
    out[out[:, :, 3] == 0, :3] = 0
    return out


def trim_alpha(rgba: np.ndarray, pad: int = 2) -> np.ndarray:
    ys, xs = np.where(rgba[:, :, 3] > 0)
    if len(xs) == 0:
        return rgba
    y0, y1 = max(0, ys.min() - pad), min(rgba.shape[0], ys.max() + 1 + pad)
    x0, x1 = max(0, xs.min() - pad), min(rgba.shape[1], xs.max() + 1 + pad)
    return rgba[y0:y1, x0:x1]


def upscale_nn(im: Image.Image, scale: int = SCALE) -> Image.Image:
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def extract_cta() -> Image.Image:
    im = Image.open(CTA_REF).convert("RGBA")
    a = np.array(im)
    # Keep pink plate + black text; drop pure black canvas.
    # Also keep dark splatters that sit on / near pink (not pure canvas).
    rgb = a[:, :, :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    pinkish = (rgb[:, :, 0] > 90) & (rgb[:, :, 0] > rgb[:, :, 1] + 25)
    # Dilate pink to keep edge splatters / stencil crumbs
    from scipy import ndimage

    pink_d = ndimage.binary_dilation(pinkish, iterations=2)
    # Black text / splatters inside pink_d stay
    is_canvas = (lum < 18) & ~pink_d
    out = a.copy()
    out[:, :, 3] = np.where(is_canvas, 0, 255).astype(np.uint8)
    out[out[:, :, 3] == 0, :3] = 0
    out = trim_alpha(out, pad=1)
    return Image.fromarray(out)


def make_buy_from_activate(activate: Image.Image) -> Image.Image:
    """Same distressed side-edge silhouette; recolor pink→grey; replace text ACTIVATE→BUY."""
    a = np.array(activate.convert("RGBA"))
    rgb = a[:, :, :3].astype(np.float32)
    alpha = a[:, :, 3]

    # Detect pink fill (not black text)
    is_pink = (rgb[:, :, 0] > 100) & (rgb[:, :, 0] > rgb[:, :, 1] + 20) & (rgb[:, :, 0] > rgb[:, :, 2] * 0.55)
    is_text = (rgb.mean(axis=2) < 55) & (alpha > 0) & ~is_pink

    # Map pink → cool grey plate (keep luminance variation of original pink)
    pink_lum = (0.35 * rgb[:, :, 0] + 0.35 * rgb[:, :, 1] + 0.30 * rgb[:, :, 2]) / 255.0
    # Target grey around #9A9A9A with slight cool cast
    grey = np.zeros_like(rgb)
    base = 120 + 70 * pink_lum  # 120..190
    grey[:, :, 0] = base * 0.95
    grey[:, :, 1] = base * 0.97
    grey[:, :, 2] = base * 1.02

    out = a.copy()
    for c in range(3):
        ch = out[:, :, c].astype(np.float32)
        ch[is_pink] = grey[:, :, c][is_pink]
        out[:, :, c] = np.clip(ch, 0, 255).astype(np.uint8)

    # Clear ACTIVATE text region and redraw BUY with similar bold condensed look
    # Estimate text bbox from dark pixels
    ys, xs = np.where(is_text)
    if len(xs) == 0:
        return Image.fromarray(out)

    # Fill text pixels with local grey (neighbor median of pink→grey)
    out_rgb = out[:, :, :3].astype(np.float32)
    # Replace text with interpolated grey from plate mean
    plate_mean = out_rgb[is_pink].mean(axis=0) if is_pink.any() else np.array([150, 152, 158])
    for c in range(3):
        out_rgb[is_text, c] = plate_mean[c]
    out[:, :, :3] = np.clip(out_rgb, 0, 255).astype(np.uint8)

    im = Image.fromarray(out)
    # Draw BUY
    draw = ImageDraw.Draw(im)
    # Prefer Impact / Arial Black / condensed bold
    font = None
    for candidate in (
        r"C:\Windows\Fonts\impact.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        if os.path.exists(candidate):
            # Size relative to plate height
            size = max(14, int(im.height * 0.55))
            font = ImageFont.truetype(candidate, size=size)
            break
    if font is None:
        font = ImageFont.load_default()

    text = "BUY"
    # Center
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (im.width - tw) // 2 - bbox[0]
    y = (im.height - th) // 2 - bbox[1] - 1
    draw.text((x, y), text, fill=(0, 0, 0, 255), font=font)
    return im


def extract_ribbon() -> Image.Image:
    im = Image.open(RIBBON_REF).convert("RGBA")
    a = np.array(im)
    rgb = a[:, :, :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    from scipy import ndimage

    # Paper / sticker body
    paper = lum > 85
    paper_d = ndimage.binary_dilation(paper, iterations=2)
    # Keep black text holes inside paper
    is_canvas = (lum < 28) & ~paper_d
    out = a.copy()
    out[:, :, 3] = np.where(is_canvas, 0, 255).astype(np.uint8)
    out[out[:, :, 3] == 0, :3] = 0
    out = trim_alpha(out, pad=1)
    return Image.fromarray(out)


def deskew_ribbon(im: Image.Image) -> Image.Image:
    """Optional slight deskew — keep mild tilt as in ref; do nothing heavy."""
    return im


def blank_ribbon_from(labeled: Image.Image) -> Image.Image:
    """Remove baked title text → blank distressed plate for overlay / re-label."""
    a = np.array(labeled.convert("RGBA"))
    rgb = a[:, :, :3].astype(np.float32)
    alpha = a[:, :, 3]
    lum = rgb.mean(axis=2)
    # Text = dark on light paper
    is_text = (lum < 70) & (alpha > 0) & (rgb[:, :, 0] < 90)
    paper_mean = rgb[(lum > 100) & (alpha > 0)].mean(axis=0) if ((lum > 100) & (alpha > 0)).any() else np.array([220, 218, 214])
    for c in range(3):
        rgb[is_text, c] = paper_mean[c]
    # Soften text erasure seams
    out = a.copy()
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    im = Image.fromarray(out)
    # Mild blur only on former text region via paste
    return im


def paint_label(blank: Image.Image, text: str) -> Image.Image:
    im = blank.copy()
    draw = ImageDraw.Draw(im)
    font = None
    for candidate in (
        r"C:\Windows\Fonts\impact.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        if os.path.exists(candidate):
            # Fit width ~78% of plate
            size = max(10, int(im.height * 0.48))
            font = ImageFont.truetype(candidate, size=size)
            # shrink until fits
            while size > 8:
                bbox = draw.textbbox((0, 0), text, font=font)
                if bbox[2] - bbox[0] <= im.width * 0.86:
                    break
                size -= 1
                font = ImageFont.truetype(candidate, size=size)
            break
    if font is None:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (im.width - tw) // 2 - bbox[0]
    y = (im.height - th) // 2 - bbox[1]
    draw.text((x, y), text, fill=(0, 0, 0, 255), font=font)
    return im


def save_pair(name: str, im: Image.Image, also_pkg: bool = True) -> None:
    raw = OUT / f"{name}_src.png"
    up = upscale_nn(im)
    up_path = OUT / f"{name}.png"
    im.save(raw)
    up.save(up_path)
    if also_pkg:
        PKG.mkdir(parents=True, exist_ok=True)
        up.save(PKG / f"{name}.png")
    print(f"{name}: src={im.size} up={up.size} -> {up_path}")


def main() -> None:
    cta = extract_cta()
    save_pair("cta_activate", cta)

    buy = make_buy_from_activate(cta)
    save_pair("cta_buy", buy)

    rib = deskew_ribbon(extract_ribbon())
    # Keep OBSERVATION+ as direct extract (authentic text from ref)
    save_pair("ribbon_observation_plus", rib)

    blank = blank_ribbon_from(rib)
    save_pair("ribbon_blank", blank)

    labels = {
        "ribbon_scatter": "SCATTER",
        "ribbon_observation": "OBSERVATION",
        "ribbon_observation_plusplus": "OBSERVATION++",
        "ribbon_fractured": "FRACTURED",
        "ribbon_deepness": "DEEPNESS",
    }
    for fname, label in labels.items():
        save_pair(fname, paint_label(blank, label))

    print("DONE ->", PKG)


if __name__ == "__main__":
    main()
