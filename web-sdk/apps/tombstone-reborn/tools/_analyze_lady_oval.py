"""Locate Patient oval artifact across still + idle frames."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance
from scipy import ndimage

APP = Path(__file__).resolve().parents[1]
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
QA = APP / "assets-raw" / "lady_video" / "_qa"
FRAMES = APP / "assets-raw" / "lady_video" / "_frames_base"
QA.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # restore bak for analysis
    for name in ("lady_character.png", "lady_bonus.png"):
        bak = STATIC / f"{name}.pre_oval_clean.bak"
        if bak.is_file():
            shutil.copy2(bak, STATIC / name)
            shutil.copy2(bak, VITE / name)

    im = Image.open(STATIC / "lady_character.png").convert("RGBA")
    white = Image.new("RGBA", im.size, (245, 245, 240, 255))
    white.alpha_composite(im)
    white.save(QA / "lady_on_white.png")
    crop = white.crop((180, 620, 480, 980))
    ImageEnhance.Contrast(crop.convert("RGB"),).enhance(2.5).save(QA / "lady_on_white_amp.png")

    # still: mid-alpha islands
    a = np.array(im)
    alpha = a[:, :, 3]
    labeled, n = ndimage.label(alpha > 16)
    sizes = sorted([(k, int((labeled == k).sum())) for k in range(1, n + 1)], key=lambda x: -x[1])
    print("still islands", sizes[:8])
    for k, s in sizes[1:]:
        if s < 20:
            continue
        ys, xs = np.where(labeled == k)
        print(f"  island {k}: n={s} c=({xs.mean():.0f},{ys.mean():.0f}) bbox=({xs.min()},{ys.min()})-({xs.max()},{ys.max()}) meanA={alpha[ys,xs].mean():.1f}")

    # scan frames
    print("frame soft extras:")
    for i in range(0, 120, 4):
        fp = FRAMES / f"f_{i:04d}.png"
        if not fp.exists():
            continue
        fr = np.array(Image.open(fp).convert("RGB"))
        b = fr.astype(np.int16)
        is_blue = (b[:, :, 2] > 180) & (b[:, :, 0] < 90) & (b[:, :, 1] < 90)
        al = (~is_blue).astype(np.uint8) * 255
        labeled, n = ndimage.label(al > 128)
        sizes = sorted([(k, int((labeled == k).sum())) for k in range(1, n + 1)], key=lambda x: -x[1])
        extra = [(k, s) for k, s in sizes[1:] if s > 80]
        gray = fr.mean(2).astype(np.float32)
        y0, y1, x0, x1 = 700, 1000, 220, 480
        roi = gray[y0:y1, x0:x1]
        roi_a = al[y0:y1, x0:x1] > 128
        mu = cv2.GaussianBlur(roi, (0, 0), 5)
        var = cv2.GaussianBlur(roi**2, (0, 0), 5) - mu**2
        soft_n = int(((var < 40) & roi_a).sum())
        if extra or soft_n > 8000:
            print(f"  f_{i:04d} soft={soft_n} extras={extra[:4]}")

    webm = STATIC / "lady_idle_base.webm"
    for t in ("0.0", "1.0", "2.0", "3.5", "4.5"):
        out = QA / f"webm_t{t.replace('.', '')}.png"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-c:v", "libvpx-vp9", "-ss", t, "-i", str(webm),
                "-frames:v", "1", "-pix_fmt", "rgba", str(out),
            ],
            check=False,
        )
        if not out.exists():
            print(f"webm t={t} MISSING")
            continue
        wa = np.array(Image.open(out).convert("RGBA"))
        al = wa[:, :, 3]
        labeled, n = ndimage.label(al > 20)
        sizes = sorted([(k, int((labeled == k).sum())) for k in range(1, n + 1)], key=lambda x: -x[1])
        extras = []
        for k, s in sizes[1:]:
            if s < 40:
                continue
            ys, xs = np.where(labeled == k)
            extras.append((s, float(xs.mean()), float(ys.mean()), float(al[ys, xs].mean())))
        mid = int(((al > 20) & (al < 200)).sum())
        print(f"webm t={t} extras={extras[:6]} midA={mid}")


if __name__ == "__main__":
    main()
