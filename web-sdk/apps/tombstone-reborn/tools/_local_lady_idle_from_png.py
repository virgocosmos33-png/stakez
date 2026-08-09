"""Local high-quality idle loops from Patient stills (Scenario CU exhausted).

Produces blue-screen mp4s suitable for post_lady_idle_video.py chroma-key.
Micro-motion: shallow breath, hem-pinned scale, hair/cloth sway, optional
bonus fluorescent flicker + red blink + darker grade.
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance

APP = Path(__file__).resolve().parents[1]
VIDEO = APP / "assets-raw" / "lady_video"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
TMP = Path(tempfile.gettempdir()) / "lady_idle_local"
TMP.mkdir(parents=True, exist_ok=True)

BLUE = (0, 0, 255)
CANVAS = (720, 1280)
FPS = 24
SECONDS = 5
FIG_H_FRAC = 0.9


def composite_on_blue(fig: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", CANVAS, BLUE + (255,))
    target_h = int(CANVAS[1] * FIG_H_FRAC)
    scale = target_h / fig.height
    target_w = max(2, int(fig.width * scale))
    fig2 = fig.resize((target_w, target_h), Image.LANCZOS)
    x = (CANVAS[0] - target_w) // 2
    y = (CANVAS[1] - target_h) // 2
    canvas.alpha_composite(fig2, (x, y))
    return canvas


def render_variant(src: Path, dest_mp4: Path, *, bonus: bool) -> None:
    fig = Image.open(src).convert("RGBA")
    base = composite_on_blue(fig)
    # hem-pin pivot: bottom-center of figure bbox
    arr0 = np.array(base)
    alpha = arr0[..., 3]
    ys, xs = np.where(alpha > 8)
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    cx = (x0 + x1) / 2.0
    cy = float(y1)  # hem

    n = FPS * SECONDS
    frames_dir = VIDEO / ("_frames_bonus" if bonus else "_frames_base")
    if frames_dir.exists():
        for p in frames_dir.glob("*.png"):
            p.unlink()
    frames_dir.mkdir(parents=True, exist_ok=True)

    for i in range(n):
        t = i / FPS
        # seamless loop: phase over full period
        phase = 2 * math.pi * (i / n)
        breath = math.sin(phase)  # -1..1
        sway = math.sin(phase * 0.5 + 0.3)
        twitch = 0.0
        if bonus:
            # rare head-twitch pulses mid-loop
            pulse = math.exp(-(((i / n) - 0.42) ** 2) / 0.0008) + math.exp(
                -(((i / n) - 0.78) ** 2) / 0.0006
            )
            twitch = 0.012 * pulse

        # Single clean affine only (no stacked warps → no double-body ghosts)
        scale_y = 1.0 + 0.010 * breath + (0.003 * abs(breath) if bonus else 0.0)
        scale_x = 1.0 - 0.005 * breath
        rot = 0.22 * sway + (1.6 * twitch if bonus else 0.0)  # degrees
        # tiny hem-locked sway (pixels) — keeps one chair silhouette
        dx = 1.2 * sway + (2.0 * twitch if bonus else 0.0)
        dy = -0.6 * breath

        im = base
        ang = math.radians(rot)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        a = scale_x * cos_a
        b = -scale_y * sin_a
        c = cx - a * cx - b * cy + dx
        d = scale_x * sin_a
        e = scale_y * cos_a
        f = cy - d * cx - e * cy + dy
        warped = im.transform(
            CANVAS,
            Image.AFFINE,
            (a, b, c, d, e, f),
            resample=Image.BILINEAR,
            fillcolor=BLUE + (255,),
        )

        rgb = warped.convert("RGB")
        if bonus:
            # darker clinical grade + fluorescent flicker + rare red blink
            rgb = ImageEnhance.Brightness(rgb).enhance(0.88)
            rgb = ImageEnhance.Contrast(rgb).enhance(1.12)
            flick = 1.0
            # hard fluoro strobe bursts
            if math.sin(t * 13.5) > 0.72:
                flick = 1.18
            elif math.sin(t * 13.5 + 1.7) > 0.85:
                flick = 0.78
            rgb = ImageEnhance.Brightness(rgb).enhance(flick)
            # red recording blink (~2 frames)
            if 0.55 <= (i / n) <= 0.56 or 0.91 <= (i / n) <= 0.92:
                r, g, b = rgb.split()
                r = r.point(lambda v: min(255, int(v * 1.25 + 18)))
                g = g.point(lambda v: int(v * 0.82))
                b = b.point(lambda v: int(v * 0.82))
                rgb = Image.merge("RGB", (r, g, b))

        # force pure blue outside character (re-key friendly)
        out = np.array(rgb)
        a_mask = np.array(warped.split()[-1])
        # pixels that became empty from warp → blue
        empty = a_mask < 8
        out[empty] = BLUE
        # also crush near-blue fringe toward key color for cleaner chromakey
        bch = out.astype(np.int16)
        is_blueish = (bch[..., 2] > 180) & (bch[..., 0] < 90) & (bch[..., 1] < 90)
        out[is_blueish] = BLUE

        Image.fromarray(out).save(frames_dir / f"f_{i:04d}.png")

    dest_mp4.parent.mkdir(parents=True, exist_ok=True)
    tmp_mp4 = TMP / dest_mp4.name
    if tmp_mp4.exists():
        tmp_mp4.unlink()
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-framerate",
        str(FPS),
        "-i",
        str(frames_dir / "f_%04d.png"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        str(tmp_mp4),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-2000:])
    for i in range(10):
        try:
            if dest_mp4.exists():
                dest_mp4.unlink()
            shutil.copy2(tmp_mp4, dest_mp4)
            break
        except OSError:
            time.sleep(0.4 * (i + 1))
    else:
        dest_mp4.write_bytes(tmp_mp4.read_bytes())
    print(f"[mp4] {dest_mp4.name} ({dest_mp4.stat().st_size // 1024} KB)", flush=True)


def main() -> None:
    base_src = STATIC / "lady_character.png"
    bonus_src = STATIC / "lady_bonus.png"
    if not base_src.is_file():
        raise SystemExit(f"missing {base_src}")
    render_variant(base_src, VIDEO / "lady_idle_base.mp4", bonus=False)
    render_variant(bonus_src, VIDEO / "lady_idle_bonus.mp4", bonus=True)
    print("[done] local idles", flush=True)


if __name__ == "__main__":
    main()
