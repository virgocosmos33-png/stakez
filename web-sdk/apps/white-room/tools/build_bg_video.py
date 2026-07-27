"""Bake the base-game backgrounds into seamless looping ambient videos.

The old approach drew candle flames in Svelte at canvas coordinates, which
drifted off their candles whenever the window aspect changed. Baking the
animation into the painting itself makes the coordinates exact forever: the
effects live in image space and ride the same cover-fit transform as the
artwork, so they stay glued to their candles on every screen size.

Per painting (landscape 1536x1024 + portrait 1024x1536) this renders a
10-second loop at 30 fps with:
  - candle flame flicker + wall halos at the painted candle positions
  - the crystal ball breathing violet light
  - slow-drifting dust motes
  - a breathing vignette

Every animated parameter is a sum of sinusoids with an INTEGER number of
cycles over the loop, so frame 0 == frame 300 and the loop is seamless.

Output: static/assets/sprites/mirror/bg_base_anim.mp4 (+ _portrait).
Run:    python tools/build_bg_video.py
"""

import math
import os
import shutil
import subprocess
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR_DIR = os.path.normpath(
    os.path.join(HERE, "..", "static", "assets", "sprites", "mirror")
)

FPS = 30
DURATION = 10.0
FRAMES = int(FPS * DURATION)
TAU = math.tau

# palettes (r, g, b) 0..1
PALETTES = {
    "violet": {"glow": (0.72, 0.53, 1.0), "body": (0.85, 0.70, 1.0), "core": (1.0, 0.97, 1.0)},
    "green": {"glow": (0.17, 1.0, 0.40), "body": (0.55, 1.0, 0.67), "core": (0.92, 1.0, 0.94)},
    "amber": {"glow": (1.0, 0.70, 0.28), "body": (1.0, 0.82, 0.48), "core": (1.0, 0.95, 0.84)},
}

# flame anchors in normalized painting space (u, v) - same points the old
# Svelte code used, now baked at exact pixel positions
LANDSCAPE = {
    "size": (1536, 1024),
    "src": "bg_base.webp",
    "out": "bg_base_anim.mp4",
    "flames": [
        {"u": 0.095, "v": 0.528, "size": 1.1, "palette": "violet"},
        {"u": 0.075, "v": 0.573, "size": 0.85, "palette": "violet"},
        {"u": 0.118, "v": 0.571, "size": 0.8, "palette": "violet"},
        {"u": 0.048, "v": 0.628, "size": 0.65, "palette": "violet"},
        {"u": 0.066, "v": 0.657, "size": 0.4, "palette": "violet"},
        {"u": 0.955, "v": 0.607, "size": 1.05, "palette": "green"},
    ],
    # violet crystal ball on the seance table
    "orbs": [{"u": 0.133, "v": 0.69, "size": 1.0, "palette": "violet"}],
}
PORTRAIT = {
    "size": (1024, 1536),
    "src": "bg_base_portrait.webp",
    "out": "bg_base_anim_portrait.mp4",
    "flames": [
        {"u": 0.385, "v": 0.048, "size": 0.9, "palette": "amber"},
        {"u": 0.605, "v": 0.042, "size": 0.9, "palette": "amber"},
        {"u": 0.345, "v": 0.128, "size": 0.55, "palette": "amber"},
        {"u": 0.06, "v": 0.74, "size": 0.8, "palette": "green"},
        {"u": 0.105, "v": 0.755, "size": 0.65, "palette": "green"},
        {"u": 0.705, "v": 0.752, "size": 0.7, "palette": "green"},
        {"u": 0.945, "v": 0.8, "size": 0.85, "palette": "green"},
    ],
    "orbs": [{"u": 0.5, "v": 0.765, "size": 1.15, "palette": "violet"}],
}

GLOW_SCALE = 4  # glow layer rendered at 1/4 res for softness + speed


def rand(seed: float) -> float:
    value = math.sin(seed * 12.9898 + 78.233) * 43758.5453
    return value - math.floor(value)


def periodic(t: float, harmonics, seed: float) -> float:
    """Sum of sines, each an integer cycle count over DURATION (seamless)."""
    total = 0.0
    for i, (cycles, amp) in enumerate(harmonics):
        phase = rand(seed * 7.13 + i * 3.71) * TAU
        total += amp * math.sin(TAU * cycles * t / DURATION + phase)
    return total


def splat(layer: np.ndarray, x: float, y: float, radius: float, color, intensity: float):
    """Additive gaussian blob on the low-res glow layer."""
    if intensity <= 0 or radius <= 0:
        return
    h, w = layer.shape[:2]
    r = max(radius, 1.5)
    x0, x1 = int(max(x - r * 2.4, 0)), int(min(x + r * 2.4 + 1, w))
    y0, y1 = int(max(y - r * 2.4, 0)), int(min(y + r * 2.4 + 1, h))
    if x0 >= x1 or y0 >= y1:
        return
    ys, xs = np.mgrid[y0:y1, x0:x1]
    d2 = (xs - x) ** 2 + (ys - y) ** 2
    g = np.exp(-d2 / (2 * (r * 0.85) ** 2)) * intensity
    for c in range(3):
        layer[y0:y1, x0:x1, c] += g * color[c]


def splat_ellipse(layer, x, y, rx, ry, color, intensity):
    """Additive elongated gaussian (flame body)."""
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


def build_motes(width, height, count, seed_base):
    motes = []
    for i in range(count):
        s = seed_base + i * 17.31
        motes.append(
            {
                "x": rand(s + 1) * width,
                "y": rand(s + 2) * height,
                # oscillation: integer cycle counts keep the loop seamless
                "ax": 14 + rand(s + 3) * 30,
                "ay": 10 + rand(s + 4) * 26,
                "kx": 1 + int(rand(s + 5) * 2),
                "ky": 1 + int(rand(s + 6) * 2),
                "phx": rand(s + 7) * TAU,
                "phy": rand(s + 8) * TAU,
                "r": 0.9 + rand(s + 9) * 1.9,
                "tw": 2 + int(rand(s + 10) * 4),  # twinkle cycles
                "pht": rand(s + 11) * TAU,
                "base": 0.06 + rand(s + 12) * 0.16,
            }
        )
    return motes


def render_video(spec):
    width, height = spec["size"]
    src = os.path.join(MIRROR_DIR, spec["src"])
    out_path = os.path.join(MIRROR_DIR, spec["out"])

    base = np.asarray(Image.open(src).convert("RGB"), dtype=np.float32) / 255.0

    gw, gh = width // GLOW_SCALE, height // GLOW_SCALE
    flames = [
        {**f, "x": f["u"] * gw, "y": f["v"] * gh, "px": f["size"] * gw / 170.0}
        for f in spec["flames"]
    ]
    orbs = [
        {**o, "x": o["u"] * gw, "y": o["v"] * gh, "px": o["size"] * gw / 170.0}
        for o in spec["orbs"]
    ]
    motes = build_motes(width, height, 42, seed_base=width * 0.001)

    # breathing vignette mask (precomputed): 1 at center, darker at corners
    ys, xs = np.mgrid[0:height, 0:width]
    nx = (xs / width - 0.5) * 2
    ny = (ys / height - 0.5) * 2
    vig = np.sqrt(nx**2 + ny**2) / math.sqrt(2)
    vig = (vig**2.2)[..., None].astype(np.float32)

    tmp = tempfile.mkdtemp(prefix="bgvid_")
    try:
        for frame in range(FRAMES):
            t = frame / FPS
            glow = np.zeros((gh, gw, 3), dtype=np.float32)

            for i, flame in enumerate(flames):
                pal = PALETTES[flame["palette"]]
                px = flame["px"]
                breath = 0.78 + periodic(
                    t, [(31, 0.14), (53, 0.09), (17, 0.10), (7, 0.06)], seed=i * 3.7 + 1
                )
                sway = periodic(t, [(13, 1.0), (29, 0.5)], seed=i * 5.1 + 2) * px * 1.4
                stretch = 1.0 + periodic(t, [(41, 0.18), (23, 0.14)], seed=i * 7.9 + 3)
                x = flame["x"] + sway * 0.35
                y = flame["y"]

                # wall halo
                splat(glow, x, y, px * 10.5 * breath, pal["glow"], 0.10 + 0.06 * breath)
                splat(glow, x, y, px * 5.5 * breath, pal["glow"], 0.14 + 0.08 * breath)
                # flame body (teardrop leaning into the sway) + hot core
                splat_ellipse(
                    glow, x + sway * 0.4, y, px * 1.9 * breath, px * 3.4 * stretch,
                    pal["body"], 0.55 * breath,
                )
                splat_ellipse(
                    glow, x + sway * 0.55, y - px * stretch * 0.7,
                    px * 1.0, px * 2.0 * stretch, pal["core"], 0.8 * breath,
                )

            for i, orb in enumerate(orbs):
                pal = PALETTES[orb["palette"]]
                px = orb["px"]
                pulse = 0.7 + periodic(t, [(2, 0.16), (5, 0.10), (11, 0.06)], seed=90 + i)
                splat(glow, orb["x"], orb["y"], px * 9 * pulse, pal["glow"], 0.10 * pulse)
                splat(glow, orb["x"], orb["y"], px * 4.5 * pulse, pal["body"], 0.16 * pulse)

            glow_full = np.asarray(
                Image.fromarray(
                    (np.clip(glow, 0, 1.6) * 159).astype(np.uint8), mode="RGB"
                ).resize((width, height), Image.BILINEAR),
                dtype=np.float32,
            ) / 159.0

            frame_img = base + glow_full * 1.6

            # dust motes at full res (tiny additive points)
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
                frame_img[y0:y1, x0:x1, :] += g[..., None] * np.array(
                    [0.85, 0.8, 1.0], dtype=np.float32
                )

            # breathing vignette
            breathe = 0.10 + 0.025 * math.sin(TAU * 2 * t / DURATION)
            frame_img *= 1.0 - vig * breathe

            Image.fromarray(
                (np.clip(frame_img, 0, 1) * 255).astype(np.uint8), mode="RGB"
            ).save(os.path.join(tmp, f"{frame:04d}.jpg"), quality=95)

            if frame % 60 == 0:
                print(f"  {spec['out']}: frame {frame}/{FRAMES}")

        subprocess.run(
            [
                "ffmpeg", "-y", "-framerate", str(FPS),
                "-i", os.path.join(tmp, "%04d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
                "-crf", "22", "-preset", "slow", "-movflags", "+faststart", "-an",
                out_path,
            ],
            check=True,
            capture_output=True,
        )
        size_mb = os.path.getsize(out_path) / 1e6
        print(f"wrote {out_path} ({size_mb:.1f} MB)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    for spec in (LANDSCAPE, PORTRAIT):
        render_video(spec)
    print("done")
