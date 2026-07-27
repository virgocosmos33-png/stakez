"""Bake THE WHITE ROOM padded-cell stills into seamless ambient BG loops.

Clinical fluorescent flicker + drifting dust (no Madam candles/orbs/purple).
Outputs replace bg_base_anim.mp4, bg_base_anim_portrait.mp4, bg_freespin_anim.mp4.
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "mirror"))

FPS = 30
DURATION = 8.0
FRAMES = int(FPS * DURATION)
TAU = math.tau
GLOW_SCALE = 4

SPECS = [
    {
        "src": "bg_base.webp",
        "out": "bg_base_anim.mp4",
        "size": (1536, 1024),
        # soft overhead fluorescent pulses (normalized u,v)
        "tubes": [
            {"u": 0.50, "v": 0.08, "w": 0.55, "h": 0.10, "gain": 0.14},
            {"u": 0.22, "v": 0.12, "w": 0.22, "h": 0.08, "gain": 0.08},
            {"u": 0.78, "v": 0.12, "w": 0.22, "h": 0.08, "gain": 0.08},
        ],
        "camera_red": {"u": 0.92, "v": 0.10, "gain": 0.22},
        "motes": 56,
        "vignette": 0.08,
        "dust_rgb": (0.92, 0.90, 0.86),
    },
    {
        "src": "bg_base_portrait.webp",
        "out": "bg_base_anim_portrait.mp4",
        "size": (1024, 1536),
        "tubes": [
            {"u": 0.50, "v": 0.06, "w": 0.70, "h": 0.08, "gain": 0.12},
        ],
        "camera_red": None,
        "motes": 48,
        "vignette": 0.10,
        "dust_rgb": (0.93, 0.91, 0.88),
    },
    {
        "src": "bg_freespin.webp",
        "out": "bg_freespin_anim.mp4",
        "size": (1536, 1024),
        "tubes": [
            {"u": 0.50, "v": 0.10, "w": 0.60, "h": 0.12, "gain": 0.18},
            {"u": 0.18, "v": 0.14, "w": 0.20, "h": 0.08, "gain": 0.10},
            {"u": 0.82, "v": 0.14, "w": 0.20, "h": 0.08, "gain": 0.10},
        ],
        "camera_red": {"u": 0.90, "v": 0.09, "gain": 0.35},
        "motes": 70,
        "vignette": 0.12,
        "dust_rgb": (0.90, 0.88, 0.84),
    },
]


def rand(seed: float) -> float:
    value = math.sin(seed * 12.9898 + 78.233) * 43758.5453
    return value - math.floor(value)


def periodic(t: float, harmonics, seed: float) -> float:
    total = 0.0
    for i, (cycles, amp) in enumerate(harmonics):
        phase = rand(seed * 7.13 + i * 3.71) * TAU
        total += amp * math.sin(TAU * cycles * t / DURATION + phase)
    return total


def build_motes(width, height, count, seed_base):
    motes = []
    for i in range(count):
        s = seed_base + i * 17.31
        motes.append(
            {
                "x": rand(s + 1) * width,
                "y": rand(s + 2) * height,
                "ax": 10 + rand(s + 3) * 22,
                "ay": 8 + rand(s + 4) * 18,
                "kx": 1 + int(rand(s + 5) * 2),
                "ky": 1 + int(rand(s + 6) * 2),
                "phx": rand(s + 7) * TAU,
                "phy": rand(s + 8) * TAU,
                "r": 0.7 + rand(s + 9) * 1.6,
                "tw": 2 + int(rand(s + 10) * 4),
                "pht": rand(s + 11) * TAU,
                "base": 0.04 + rand(s + 12) * 0.12,
            }
        )
    return motes


def splat_ellipse(layer, x, y, rx, ry, color, intensity):
    if intensity <= 0:
        return
    h, w = layer.shape[:2]
    ex, ey = max(rx, 1.0), max(ry, 1.0)
    x0, x1 = int(max(x - ex * 2.6, 0)), int(min(x + ex * 2.6 + 1, w))
    y0, y1 = int(max(y - ey * 2.6, 0)), int(min(y + ey * 2.6 + 1, h))
    if x0 >= x1 or y0 >= y1:
        return
    ys, xs = np.mgrid[y0:y1, x0:x1]
    d2 = ((xs - x) / ex) ** 2 + ((ys - y) / ey) ** 2
    g = np.exp(-d2 / 0.9) * intensity
    for c in range(3):
        layer[y0:y1, x0:x1, c] += g * color[c]


def render_video(spec):
    src_path = os.path.join(MIRROR_DIR, spec["src"])
    out_path = os.path.join(MIRROR_DIR, spec["out"])
    width, height = spec["size"]

    base_im = Image.open(src_path).convert("RGB").resize((width, height), Image.LANCZOS)
    base = np.asarray(base_im, dtype=np.float32) / 255.0

    gw, gh = width // GLOW_SCALE, height // GLOW_SCALE
    motes = build_motes(width, height, spec["motes"], seed_base=width * 0.001 + height * 0.0007)
    dust = np.array(spec["dust_rgb"], dtype=np.float32)

    ys, xs = np.mgrid[0:height, 0:width]
    nx = (xs / width - 0.5) * 2
    ny = (ys / height - 0.5) * 2
    vig = (np.sqrt(nx**2 + ny**2) / math.sqrt(2)) ** 2.2
    vig = vig[..., None].astype(np.float32)

    tmp = tempfile.mkdtemp(prefix="wr_bgvid_")
    try:
        for frame in range(FRAMES):
            t = frame / FPS
            glow = np.zeros((gh, gw, 3), dtype=np.float32)

            # fluorescent tubes — cool white/silver, slight flicker blackouts
            flicker = 0.82 + periodic(t, [(11, 0.10), (23, 0.05), (47, 0.03)], seed=3.1)
            if rand(frame * 0.37 + 2.2) < 0.03:
                flicker *= 0.35
            for i, tube in enumerate(spec["tubes"]):
                x = tube["u"] * gw
                y = tube["v"] * gh
                rx = tube["w"] * gw * 0.5
                ry = tube["h"] * gh * 0.5
                gain = tube["gain"] * flicker
                splat_ellipse(glow, x, y, rx, ry, (0.95, 0.94, 0.90), gain)
                splat_ellipse(glow, x, y, rx * 1.6, ry * 2.2, (0.85, 0.84, 0.80), gain * 0.45)

            cam = spec.get("camera_red")
            if cam:
                pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(TAU * 2 * t / DURATION))
                splat_ellipse(
                    glow,
                    cam["u"] * gw,
                    cam["v"] * gh,
                    max(gw * 0.012, 1.5),
                    max(gh * 0.012, 1.5),
                    (0.75, 0.12, 0.10),
                    cam["gain"] * pulse,
                )

            glow_full = (
                np.asarray(
                    Image.fromarray((np.clip(glow, 0, 1.5) * 160).astype(np.uint8), mode="RGB").resize(
                        (width, height), Image.BILINEAR
                    ),
                    dtype=np.float32,
                )
                / 160.0
            )
            frame_img = base + glow_full * 1.35

            for m in motes:
                mx = m["x"] + m["ax"] * math.sin(TAU * m["kx"] * t / DURATION + m["phx"])
                my = m["y"] + m["ay"] * math.sin(TAU * m["ky"] * t / DURATION + m["phy"])
                al = m["base"] * (0.5 + 0.5 * math.sin(TAU * m["tw"] * t / DURATION + m["pht"]))
                if al <= 0.01:
                    continue
                r = m["r"]
                x0, x1 = int(max(mx - r * 3, 0)), int(min(mx + r * 3 + 1, width))
                y0, y1 = int(max(my - r * 3, 0)), int(min(my + r * 3 + 1, height))
                if x0 >= x1 or y0 >= y1:
                    continue
                yy, xx = np.mgrid[y0:y1, x0:x1]
                g = np.exp(-((xx - mx) ** 2 + (yy - my) ** 2) / (2 * r * r)) * al
                frame_img[y0:y1, x0:x1, :] += g[..., None] * dust

            breathe = spec["vignette"] + 0.02 * math.sin(TAU * 2 * t / DURATION)
            frame_img *= 1.0 - vig * breathe

            Image.fromarray((np.clip(frame_img, 0, 1) * 255).astype(np.uint8), mode="RGB").save(
                os.path.join(tmp, f"{frame:04d}.jpg"), quality=94
            )
            if frame % 60 == 0:
                print(f"  {spec['out']}: frame {frame}/{FRAMES}")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                os.path.join(tmp, "%04d.jpg"),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-profile:v",
                "high",
                "-crf",
                "22",
                "-preset",
                "fast",
                "-movflags",
                "+faststart",
                "-an",
                out_path,
            ],
            check=True,
            capture_output=True,
        )
        print(f"wrote {out_path} ({os.path.getsize(out_path) / 1e6:.1f} MB)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    for spec in SPECS:
        render_video(spec)
    print("done")
