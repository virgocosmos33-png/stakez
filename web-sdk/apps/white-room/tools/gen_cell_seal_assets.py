"""Build Cell Seal full-reel stills + expand gifs for H1–H5 (THE WHITE ROOM).

Priority (never ship empty silhouette / paytable stubs):
  1) Scenario / GodMode masters in assets-raw/cellSeal/{id}_full.(png|webp)
     — keep if >= 200KB (real gens); skip tiny stubs
  2) Compose from tools/symbol_art/card_h*_*.png medallions → tall reel
  3) Expand: assets-raw/cellSeal/{id}_expand.(mp4|webm) → gif via ffmpeg
     else synthesize medallion→full expand gif

Installs:
  static/assets/sprites/cellSeal/{id}_full.webp
  static/assets/sprites/cellSeal/{id}_expand.gif
  static/assets/sprites/cellSeal/{id}_idle.webm   (from expand mp4 or still→breath)

Env:
  CELL_SEAL_IDS=H1,H2
  CELL_SEAL_FORCE=1
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageOps
except ImportError as e:
    raise SystemExit(f"Pillow required: {e}")

APP = Path(__file__).resolve().parents[1]
OUT = APP / "static" / "assets" / "sprites" / "cellSeal"
# Vite import.meta.url loads from assets/ (must be a real dir, not a junction into static/)
OUT_ASSETS = APP / "assets" / "sprites" / "cellSeal"
RAW = APP / "assets-raw" / "cellSeal"
SYMBOL_ART = APP / "tools" / "symbol_art"

W, H = 512, 1680
SYMBOLS = ["H1", "H2", "H3", "H4", "H5"]

MASTERS = {
    "H1": "card_h1_the_patient.png",
    "H2": "card_h2_the_doctor.png",
    "H3": "card_h3_the_grin.png",
    "H4": "card_h4_the_doorway.png",
    "H5": "card_h5_file_404.png",
}

PAD_TOP = (232, 228, 220, 255)
PAD_BOT = (58, 56, 52, 255)
BEZEL = (200, 196, 188, 255)
FRAME = (232, 212, 77, 230)


def _load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def _looks_like_medallion_composite(im: Image.Image) -> bool:
    """Detect circular-medallion + ghost-body composites (H2–H5 bug).

    Real Scenario full-bodies are dense padded-cell scenes (~700KB+ PNG).
    Medallion composites have a bright circular disk in the upper third and
    a mostly flat/grid lower body — reject those so FORCE can replace them.
    """
    if im.size[0] < 400 or im.size[1] < 1200:
        return True
    # Sample a horizontal strip across the upper medallion zone
    w, h = im.size
    y0, y1 = int(h * 0.12), int(h * 0.28)
    band = im.convert("L").crop((0, y0, w, y1))
    px = list(band.getdata())
    if not px:
        return False
    # High contrast center vs edges often means a circular badge on a panel
    mid = [px[i] for i in range(len(px)) if (w // 4) <= (i % w) < (3 * w // 4)]
    edge = [px[i] for i in range(len(px)) if (i % w) < w // 8 or (i % w) > 7 * w // 8]
    if not mid or not edge:
        return False
    mid_avg = sum(mid) / len(mid)
    edge_avg = sum(edge) / len(edge)
    # Medallion composites: bright circular face zone, duller panel edges
    return (mid_avg - edge_avg) > 35 and mid_avg > 90


def _is_real_raw(path: Path) -> bool:
    """Reject paytable stubs, empty silhouettes, and medallion composites."""
    if not path.exists():
        return False
    # Real Flux full-bodies land ~700KB–1.2MB; medallion composites ~300–500KB
    if path.stat().st_size < 600_000:
        return False
    try:
        im = Image.open(path)
        if im.size[0] < 400 or im.size[1] < 1200:
            return False
        return not _looks_like_medallion_composite(im.convert("RGBA"))
    except Exception:
        return False


def _output_complete(sym: str) -> bool:
    full = OUT / f"{sym}_full.webp"
    gif = OUT / f"{sym}_expand.gif"
    idle = OUT / f"{sym}_idle.webm"
    if not full.exists() or not gif.exists() or not idle.exists():
        return False
    if full.stat().st_size < 40_000:
        return False
    # Expand must be multi-frame motion (broken 1-frame gifs were ~1.1–1.4MB
    # but only 0.14s / 1–2 frames — require idle webm with real loop size).
    if gif.stat().st_size < 80_000:
        return False
    if idle.stat().st_size < 80_000:
        return False
    return True


def _gradient_panel() -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = im.load()
    for y in range(H):
        t = y / max(1, H - 1)
        r = int(PAD_TOP[0] * (1 - t) + PAD_BOT[0] * t)
        g = int(PAD_TOP[1] * (1 - t) + PAD_BOT[1] * t)
        b = int(PAD_TOP[2] * (1 - t) + PAD_BOT[2] * t)
        for x in range(W):
            edge = min(x, W - 1 - x) / (W * 0.5)
            vig = 0.55 + 0.45 * max(0.0, min(1.0, edge * 1.4))
            px[x, y] = (int(r * vig), int(g * vig), int(b * vig), 245)
    d = ImageDraw.Draw(im)
    step = 48
    for yy in range(80, H - 80, step):
        d.line([(36, yy), (W - 36, yy)], fill=(180, 176, 168, 28), width=1)
    for xx in range(40, W - 40, step):
        d.line([(xx, 80), (xx, H - 80)], fill=(180, 176, 168, 22), width=1)
    return im


def _circular_crop(src: Image.Image, diameter: int) -> Image.Image:
    side = min(src.size)
    left = (src.width - side) // 2
    top = (src.height - side) // 2
    sq = src.crop((left, top, left + side, top + side)).resize(
        (diameter, diameter), Image.Resampling.LANCZOS
    )
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diameter - 1, diameter - 1], fill=255)
    out = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    out.paste(sq, (0, 0), mask)
    rim = ImageDraw.Draw(out)
    rim.ellipse([2, 2, diameter - 3, diameter - 3], outline=BEZEL, width=6)
    rim.ellipse([8, 8, diameter - 9, diameter - 9], outline=(244, 241, 236, 90), width=2)
    return out


def compose_full_from_master(sym: str) -> Image.Image:
    master_path = SYMBOL_ART / MASTERS[sym]
    if not master_path.exists():
        raise FileNotFoundError(f"Missing symbol master: {master_path}")
    master = _load_rgba(master_path)
    panel = _gradient_panel()

    med = _circular_crop(master, 420)
    mx, my = (W - med.width) // 2, int(H * 0.10)
    panel.paste(med, (mx, my), med)

    body_src = master.resize((380, 900), Image.Resampling.LANCZOS)
    fade = Image.new("L", body_src.size, 0)
    fd = ImageDraw.Draw(fade)
    for y in range(body_src.height):
        t = y / max(1, body_src.height - 1)
        a = int(max(0, min(255, (t - 0.18) * 320)))
        fd.line([(0, y), (body_src.width, y)], fill=a)
    body = Image.new("RGBA", body_src.size, (0, 0, 0, 0))
    body.paste(body_src, (0, 0), fade)
    body = ImageEnhance.Brightness(body).enhance(0.78)
    body = ImageEnhance.Color(body).enhance(0.55)
    panel.paste(body, ((W - body.width) // 2, int(H * 0.38)), body)

    d = ImageDraw.Draw(panel)
    margin = 18
    d.rounded_rectangle([margin, margin, W - margin, H - margin], radius=28, outline=FRAME, width=5)
    d.rounded_rectangle(
        [margin + 8, margin + 8, W - margin - 8, H - margin - 8],
        radius=22,
        outline=(244, 241, 236, 70),
        width=2,
    )
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    for i in range(90):
        a = int(110 * (1 - i / 90))
        vd.rectangle([0, i, W, i + 1], fill=(20, 22, 26, a))
        vd.rectangle([0, H - 1 - i, W, H - i], fill=(20, 22, 26, a))
    return Image.alpha_composite(panel, vig)


def resolve_full_still(sym: str) -> tuple[Image.Image, str]:
    for name in (f"{sym}_full.png", f"{sym}_full.webp", f"{sym}_scenario.png"):
        p = RAW / name
        if _is_real_raw(p):
            im = _load_rgba(p)
            if im.size != (W, H):
                im = ImageOps.fit(im, (W, H), Image.Resampling.LANCZOS)
            return im, "scenario_raw"
    return compose_full_from_master(sym), "compose_master"


def make_expand_gif_from_still(sym: str, still: Image.Image, master: Image.Image) -> None:
    frames: list[Image.Image] = []
    n = 12
    med = _circular_crop(master, 360)
    for i in range(n):
        t = (i + 1) / n
        ease = 1 - (1 - t) ** 2.4
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        h = int(420 + (H - 420) * ease)
        w = int(360 + (W - 360) * ease * 0.85)
        w = max(8, min(W, w))
        h = max(8, min(H, h))
        plate = still.copy()
        if t < 0.55:
            canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            scale = 0.55 + 0.45 * ease
            mw = max(8, int(med.width * scale))
            mh = max(8, int(med.height * scale))
            m = med.resize((mw, mh), Image.Resampling.LANCZOS)
            canvas.paste(m, ((W - mw) // 2, (H - mh) // 2 - int(80 * (1 - ease))), m)
            clip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            cropped = plate.resize((w, h), Image.Resampling.LANCZOS)
            clip.paste(cropped, ((W - w) // 2, (H - h) // 2), cropped)
            alpha = ImageEnhance.Brightness(clip).enhance(0.35 + 0.65 * ease)
            frame = Image.alpha_composite(canvas, alpha)
        else:
            cropped = plate.resize((w, h), Image.Resampling.LANCZOS)
            frame.paste(cropped, ((W - w) // 2, (H - h) // 2), cropped)
        if i % 3 == 1:
            frame = ImageEnhance.Brightness(frame).enhance(1.08)
        elif i % 3 == 2:
            frame = ImageEnhance.Brightness(frame).enhance(0.94)
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=192))

    path = OUT / f"{sym}_expand.gif"
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        disposal=2,
        optimize=True,
    )


def try_video_to_gif(sym: str) -> bool:
    video = None
    for name in (f"{sym}_expand.mp4", f"{sym}_expand.webm", f"{sym}_expand_raw.mp4"):
        p = RAW / name
        if p.exists() and p.stat().st_size > 10_000:
            video = p
            break
    if video is None:
        return False
    out = OUT / f"{sym}_expand.gif"
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False
    cmd = [
        ffmpeg, "-y", "-i", str(video), "-t", "1.0",
        "-vf",
        f"{_cover_vf(W, H, fps=12)},"
        "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        str(out),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except (subprocess.CalledProcessError, OSError):
        return False
    return out.exists() and out.stat().st_size > 20_000


def _ensure_real_dir(path: Path) -> None:
    """Create path as a real directory. Replace accidental junctions/symlinks."""
    if path.exists() and path.is_symlink():
        path.unlink()
    elif path.exists() and not path.is_dir():
        path.unlink()
    # Windows junctions report as dirs but os.path.islink is often False; detect via resolve
    if path.exists() and path.is_dir():
        try:
            if path.resolve() != path and "static" in str(path.resolve()) and "assets" in str(path):
                # junction into static — remove and recreate as real dir
                if os.name == "nt":
                    os.rmdir(path)
                else:
                    path.unlink()
        except OSError:
            pass
    path.mkdir(parents=True, exist_ok=True)


def _mirror_to_assets() -> None:
    """Keep assets/sprites/cellSeal in sync for Vite import.meta.url loading."""
    _ensure_real_dir(OUT_ASSETS)
    if not OUT.exists():
        return
    for f in OUT.iterdir():
        if f.is_file():
            shutil.copy2(f, OUT_ASSETS / f.name)


IDLE_FPS = 12
IDLE_SECONDS = 4  # seamless loop period
EXPAND_GIF_FRAMES = 14  # ~1.1s intro / presence loop


def _cover_vf(w: int, h: int, *, fps: int | None = None) -> str:
    """Scale+crop to exact reel size — NEVER pad with black letterbox.

    Seedance/Kling masters are often wider/shorter than the reel column.
    `decrease`+`pad=black` left huge bars (content ~280x892 in 512x1680).
    `increase`+`crop` fills edge-to-edge (CSS object-fit: cover).
    """
    parts: list[str] = []
    if fps is not None:
        parts.append(f"fps={fps}")
    parts.append(f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos")
    parts.append(f"crop={w}:{h}")
    return ",".join(parts)


def _render_breath_frames(still: Image.Image, frames_dir: Path, n: int) -> None:
    """Clinical horror idle: shallow breath + micro sway + fluoro flicker.

    Pillow affine (hem-pinned) — same approach as _local_lady_idle_from_png.py.
    Scenario Seedance img2video is preferred when CU/rate-limit allows; this is
    the offline fallback so Storybook never ships static-only expands.
    """
    import math

    from PIL import ImageEnhance

    base = still.convert("RGBA")
    if base.size != (W, H):
        base = ImageOps.fit(base, (W, H), Image.Resampling.LANCZOS)
    # hem pivot: bottom-center of reel
    cx, cy = W / 2.0, float(H - 8)

    if frames_dir.exists():
        for p in frames_dir.glob("*.png"):
            p.unlink()
    frames_dir.mkdir(parents=True, exist_ok=True)

    for i in range(n):
        phase = 2 * math.pi * (i / n)
        breath = math.sin(phase)
        sway = math.sin(phase * 0.5 + 0.35)
        # restraint tension: tiny mid-loop twitch
        pulse = math.exp(-(((i / n) - 0.55) ** 2) / 0.0012)
        twitch = 0.006 * pulse

        scale_y = 1.0 + 0.014 * breath
        scale_x = 1.0 - 0.007 * breath
        rot = 0.18 * sway + 0.9 * twitch  # degrees
        dx = 1.4 * sway
        dy = -1.1 * breath

        ang = math.radians(rot)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        a = scale_x * cos_a
        b = -scale_y * sin_a
        c = cx - a * cx - b * cy + dx
        d = scale_x * sin_a
        e = scale_y * cos_a
        f = cy - d * cx - e * cy + dy
        warped = base.transform(
            (W, H),
            Image.AFFINE,
            (a, b, c, d, e, f),
            resample=Image.BILINEAR,
            fillcolor=(18, 18, 16, 255),
        )
        rgb = warped.convert("RGB")
        # fluorescent observation flicker (hard, sparse)
        t = i / IDLE_FPS
        flick = 1.0
        if math.sin(t * 13.5) > 0.78:
            flick = 1.10
        elif math.sin(t * 13.5 + 1.7) > 0.88:
            flick = 0.90
        if flick != 1.0:
            rgb = ImageEnhance.Brightness(rgb).enhance(flick)
        rgb.save(frames_dir / f"f_{i:04d}.png")


def _ffmpeg_ok(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def install_idle_webm(sym: str, still: Image.Image) -> str:
    """Looping idle for HOLD. Prefer Scenario/raw idle mp4; else local breath frames."""
    ffmpeg = shutil.which("ffmpeg")
    out = OUT / f"{sym}_idle.webm"
    raw_mp4 = RAW / f"{sym}_idle.mp4"
    if not ffmpeg:
        return "none"

    # Prefer a Scenario (or prior) idle master if present and non-tiny.
    # Env CELL_SEAL_FORCE_LOCAL=1 skips masters and rebuilds breath from still.
    force_local = os.environ.get("CELL_SEAL_FORCE_LOCAL", "").strip() in ("1", "true", "yes")
    video = None
    if not force_local:
        for name in (f"{sym}_idle.mp4", f"{sym}_idle_seedance.mp4"):
            p = RAW / name
            if p.exists() and p.stat().st_size > 80_000:
                video = p
                break
    if video is not None:
        cmd = [
            ffmpeg, "-y", "-stream_loop", "2", "-i", str(video), "-t", str(IDLE_SECONDS),
            "-vf", _cover_vf(W, H, fps=IDLE_FPS),
            "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "30", "-an",
            str(out),
        ]
        if _ffmpeg_ok(cmd) and out.exists() and out.stat().st_size > 30_000:
            return "scenario_or_raw_idle"

    # Local breath from full-body still (Scenario CU / rate-limit fallback)
    frames_dir = RAW / f"_idle_frames_{sym}"
    n = IDLE_FPS * IDLE_SECONDS
    _render_breath_frames(still, frames_dir, n)

    # Intermediate H.264 master (debug / re-encode)
    mp4_cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
        "-framerate", str(IDLE_FPS),
        "-i", str(frames_dir / "f_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
        "-movflags", "+faststart",
        str(raw_mp4),
    ]
    if not _ffmpeg_ok(mp4_cmd):
        return "none"

    webm_cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(raw_mp4),
        "-vf", f"fps={IDLE_FPS},scale={W}:{H}",
        "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "32", "-an",
        str(out),
    ]
    if not _ffmpeg_ok(webm_cmd):
        return "none"
    return "local_breath" if out.exists() and out.stat().st_size > 30_000 else "none"


def make_expand_gif_from_idle(sym: str, still: Image.Image) -> bool:
    """Build looping expand.gif from breath frames (or idle mp4) — not a 1-frame still."""
    ffmpeg = shutil.which("ffmpeg")
    out = OUT / f"{sym}_expand.gif"
    if not ffmpeg:
        return False
    raw_mp4 = RAW / f"{sym}_idle.mp4"
    src_video = None
    for name in (f"{sym}_idle.mp4", f"{sym}_expand.mp4", f"{sym}_idle_seedance.mp4"):
        p = RAW / name
        if p.exists() and p.stat().st_size > 30_000:
            src_video = p
            break
    if src_video is None and (RAW / f"_idle_frames_{sym}" / "f_0000.png").exists():
        # encode a short clip from frames if mp4 missing
        frames_dir = RAW / f"_idle_frames_{sym}"
        tmp = RAW / f"{sym}_expand_tmp.mp4"
        if _ffmpeg_ok([
            ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(IDLE_FPS),
            "-i", str(frames_dir / "f_%04d.png"),
            "-frames:v", str(EXPAND_GIF_FRAMES),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22",
            str(tmp),
        ]):
            src_video = tmp
    if src_video is None:
        return False
    # Lean looping gif for expand intro (Pixi cover-scales). Full-res motion
    # lives in idle.webm — keep gif ≤ ~1.5MB for Storybook / mobile.
    # Cover-crop so Seedance pillarbox never survives as letterbox bars.
    gw, gh = W // 2, H // 2  # 256x840
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src_video),
        "-t", "0.95",
        "-vf",
        (
            f"{_cover_vf(gw, gh, fps=10)},"
            "split[s0][s1];[s0]palettegen=max_colors=96:stats_mode=diff[p];"
            "[s1][p]paletteuse=dither=bayer:bayer_scale=4"
        ),
        "-loop", "0",
        str(out),
    ]
    ok = _ffmpeg_ok(cmd) and out.exists() and out.stat().st_size > 80_000
    tmp = RAW / f"{sym}_expand_tmp.mp4"
    if tmp.exists():
        try:
            tmp.unlink()
        except OSError:
            pass
    return ok


def install_symbol(sym: str) -> dict:
    still, source = resolve_full_still(sym)
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    # Only overwrite raw if we composed (preserve large Scenario masters)
    raw_png = RAW / f"{sym}_full.png"
    if source == "compose_master" or not _is_real_raw(raw_png):
        still.save(raw_png, "PNG")
    full_path = OUT / f"{sym}_full.webp"
    still.save(full_path, "WEBP", quality=92, method=4)

    # Idle FIRST so expand.gif can reuse breath frames / idle.mp4
    idle_src = install_idle_webm(sym, still)
    idle_path = OUT / f"{sym}_idle.webm"

    expand_src = "none"
    if make_expand_gif_from_idle(sym, still):
        expand_src = "idle_breath_gif"
    elif try_video_to_gif(sym):
        expand_src = "expand_video"
    else:
        master = _load_rgba(SYMBOL_ART / MASTERS[sym])
        make_expand_gif_from_still(sym, still, master)
        expand_src = "synth_medallion_gif"

    return {
        "symbol": sym,
        "full": f"static/assets/sprites/cellSeal/{sym}_full.webp",
        "expand": f"static/assets/sprites/cellSeal/{sym}_expand.gif",
        "idle": f"static/assets/sprites/cellSeal/{sym}_idle.webm",
        "source": source,
        "expandSource": expand_src,
        "idleSource": idle_src,
        "bytes": {
            "full": full_path.stat().st_size,
            "expand": (OUT / f"{sym}_expand.gif").stat().st_size,
            "idle": idle_path.stat().st_size if idle_path.exists() else 0,
            "raw": raw_png.stat().st_size,
        },
        "note": (
            "Scenario Seedance img2video preferred for idle; "
            "local Pillow breath used when CU/rate-limited."
        ),
    }


def main() -> None:
    ids = os.environ.get("CELL_SEAL_IDS", "").strip()
    force = os.environ.get("CELL_SEAL_FORCE", "").strip() in ("1", "true", "yes")
    syms = [s.strip().upper() for s in ids.split(",") if s.strip()] if ids else list(SYMBOLS)
    written = []
    for sym in syms:
        if sym not in SYMBOLS:
            continue
        if not force and _output_complete(sym):
            written.append({"symbol": sym, "skipped": True,
                            "full": f"static/assets/sprites/cellSeal/{sym}_full.webp",
                            "expand": f"static/assets/sprites/cellSeal/{sym}_expand.gif"})
            continue
        written.append(install_symbol(sym))
    _mirror_to_assets()
    print(json.dumps({"ok": True, "symbols": written, "out": str(OUT), "assetsOut": str(OUT_ASSETS)}, indent=2))


if __name__ == "__main__":
    main()
