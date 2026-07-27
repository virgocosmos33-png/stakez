"""Hard-scrub residual ACTIVATE ghost from blank CTA plates."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

V2 = Path(__file__).resolve().parent / "v2"
SCALE = 6
TARGETS = [
    Path(
        r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios"
        r"\web-sdk\packages\components-ui-html\src\assets\buyBonus"
    ),
    Path(
        r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios"
        r"\web-sdk\apps\ways\node_modules\components-ui-html\src\assets\buyBonus"
    ),
    Path(
        r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios"
        r"\web-sdk\apps\ways\assets\sprites\mirror\buy_ui"
    ),
    Path(
        r"C:\Users\xheih\OneDrive\Documents\lady mirror drama studios"
        r"\web-sdk\apps\ways\static\assets\sprites\mirror\buy_ui"
    ),
    V2,
]


def scrub_activate(src: Path) -> tuple[Image.Image, Image.Image]:
    a = np.array(Image.open(src).convert("RGBA"))
    rgb = a[:, :, :3].astype(np.float32)
    alpha = a[:, :, 3]
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
    a[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    im = Image.fromarray(a)

    # grey buy variant from scrubbed pink
    pink_lum = (0.35 * rgb[:, :, 0] + 0.35 * rgb[:, :, 1] + 0.30 * rgb[:, :, 2]) / 255.0
    base = 118 + 78 * pink_lum
    buy = a.copy()
    brgb = buy[:, :, :3].astype(np.float32)
    is_pink = (brgb[:, :, 0] > 80) & (brgb[:, :, 0] > brgb[:, :, 1] + 15) & plate
    grey = np.stack([base * 0.96, base * 0.98, base * 1.03], axis=2)
    for c in range(3):
        brgb[is_pink, c] = grey[is_pink, c]
    mag = plate & (brgb[:, :, 0] > brgb[:, :, 1] + 25) & (brgb[:, :, 0] > 60)
    for c in range(3):
        brgb[mag, c] = grey[mag, c]
    buy[:, :, :3] = np.clip(brgb, 0, 255).astype(np.uint8)
    return im, Image.fromarray(buy)


def deploy(name: str, img: Image.Image) -> None:
    up = img.resize((img.width * SCALE, img.height * SCALE), Image.NEAREST)
    for d in TARGETS:
        d.mkdir(parents=True, exist_ok=True)
        if d == V2:
            img.save(d / f"{name}_src.png")
        up.save(d / f"{name}.png")
    aa = np.array(img)
    pl = aa[:, :, 3] > 0
    interior = ndimage.binary_erosion(pl, iterations=2)
    dark = int((interior & (aa[:, :, :3].mean(axis=2) < 90)).sum())
    print(f"{name}: dark_interior={dark}")


def main() -> None:
    src = V2 / "cta_activate_src.png"
    act, buy = scrub_activate(src)
    deploy("cta_activate", act)
    deploy("cta_buy", buy)
    print("scrubbed + redeployed")


if __name__ == "__main__":
    main()
