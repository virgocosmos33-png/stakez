"""Rebuild loading progress bar + falling debris for THE WHITE ROOM.

Replaces Madam Mirror rocky/purple progressBar atlas and Mining-Mayhem purple
loader gems with clinical observation chrome + NON-GLASS clinical debris.

Falling particles = ceramic tile chips, pills, PATIENT 404 paper, padded lint,
fluorescent dust, restraint buckle scraps.
BANNED: glass shards, triangle knives, crystals, Madam Mirror glass.

Outputs (same frame keys LoadingScreen already uses for the bar):
  static/assets/sprites/progressBar/progressBar.{webp,png,json}
  static/assets/sprites/loadingParticles/loadingParticles.{webp,png,json}

Optional Scenario stamps:
  Drop transparent PNGs in assets-raw/loading_particles/ — stamped into the
  particle sheet when present; otherwise procedural White Room debris.
  Never fall back to glass shard sources.

Run:  python tools/make_loading_chrome.py
"""

from __future__ import annotations

import json
import math
import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

APP = Path(__file__).resolve().parents[1]
BAR_DIR = APP / "static" / "assets" / "sprites" / "progressBar"
PART_DIR = APP / "static" / "assets" / "sprites" / "loadingParticles"
RAW_DIR = APP / "assets-raw" / "loading_particles"
BACKUP = APP / "assets-backup" / "loading_chrome"

# Packed atlas cell size (matches existing progressBar.json)
CELL_W, CELL_H = 492, 87
SHEET_H = 89

BONE = (244, 241, 236, 255)
SILVER = (200, 196, 188, 255)
STEEL = (138, 134, 128, 255)
CHARCOAL = (58, 54, 50, 255)
FLUOR = (232, 240, 245, 255)
FLUOR_CORE = (255, 255, 255, 255)
TRACK = (28, 30, 34, 255)
BLOOD = (107, 42, 40, 180)
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def backup(path: Path) -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, BACKUP / (path.name + ".bak"))


# ── progress bar ─────────────────────────────────────────────────────────────

def draw_bar_background(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # recessed ceramic track inside chrome well
    pad_x, pad_y = 38, 22
    d.rounded_rectangle([pad_x, pad_y, w - pad_x, h - pad_y], radius=8, fill=TRACK)
    # faint inner steel lip
    d.rounded_rectangle(
        [pad_x + 2, pad_y + 2, w - pad_x - 2, h - pad_y - 2],
        radius=6,
        outline=(70, 72, 78, 220),
        width=2,
    )
    return img


def draw_bar_fill(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad_x, pad_y = 38, 22
    x0, y0, x1, y1 = pad_x + 3, pad_y + 3, w - pad_x - 3, h - pad_y - 3
    # fluorescent tube fill — cool clinical white → pale silver, NOT purple
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        if t < 0.35:
            c = lerp(FLUOR_CORE, FLUOR, t / 0.35)
        elif t < 0.7:
            c = lerp(FLUOR, SILVER[:3] + (255,), (t - 0.35) / 0.35)
        else:
            c = lerp(SILVER[:3] + (255,), STEEL[:3] + (255,), (t - 0.7) / 0.3)
        d.line([(x0, y), (x1, y)], fill=c)
    # top highlight seam (tube glass)
    d.rectangle([x0, y0, x1, y0 + 3], fill=(255, 255, 255, 160))
    # soft bloom
    glow = img.filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(img)
    return out


def draw_bar_frame(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # observation-chrome bezel (brushed silver / steel), padded-cell clinical
    outer = [6, 8, w - 7, h - 9]
    inner = [34, 18, w - 35, h - 19]
    d.rounded_rectangle(outer, radius=12, fill=STEEL[:3] + (245,))
    # brushed striations
    rng = random.Random(1897)
    for i in range(40):
        y = rng.randint(outer[1] + 2, outer[3] - 2)
        alpha = rng.randint(18, 55)
        col = SILVER[:3] + (alpha,) if i % 2 == 0 else BONE[:3] + (alpha,)
        d.line([(outer[0] + 8, y), (outer[2] - 8, y)], fill=col)
    # outer rim highlight / shadow
    d.rounded_rectangle(outer, radius=12, outline=BONE[:3] + (220,), width=2)
    d.rounded_rectangle(
        [outer[0] + 2, outer[1] + 2, outer[2] - 2, outer[3] - 2],
        radius=10,
        outline=CHARCOAL[:3] + (180,),
        width=2,
    )
    # cut out the well (transparent interior)
    cut = Image.new("L", (w, h), 0)
    cd = ImageDraw.Draw(cut)
    cd.rounded_rectangle(inner, radius=7, fill=255)
    # invert cut: keep frame, clear well
    alpha = img.split()[3]
    # where cut is white, zero alpha
    from PIL import ImageChops

    keep = ImageChops.invert(cut)
    img.putalpha(ImageChops.multiply(alpha, keep))
    # thin steel lip around well
    d2 = ImageDraw.Draw(img)
    d2.rounded_rectangle(inner, radius=7, outline=SILVER[:3] + (230,), width=2)
    d2.rounded_rectangle(
        [inner[0] + 2, inner[1] + 2, inner[2] - 2, inner[3] - 2],
        radius=5,
        outline=CHARCOAL[:3] + (160,),
        width=1,
    )
    # corner observation studs
    for cx, cy in [
        (outer[0] + 16, outer[1] + 14),
        (outer[2] - 16, outer[1] + 14),
        (outer[0] + 16, outer[3] - 14),
        (outer[2] - 16, outer[3] - 14),
    ]:
        d2.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=BONE[:3] + (255,))
        d2.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=STEEL)
    # sparse dried-blood fleck (White Room accent only)
    d2.ellipse([w * 0.72, h * 0.22, w * 0.72 + 3, h * 0.22 + 2], fill=BLOOD)
    return img


def write_progress_bar() -> None:
    BAR_DIR.mkdir(parents=True, exist_ok=True)
    fill = draw_bar_fill(CELL_W, CELL_H)
    bg = draw_bar_background(CELL_W, CELL_H)
    frame = draw_bar_frame(CELL_W, CELL_H)

    sheet_w = CELL_W * 3 + 4  # 1px gutters like TexturePacker
    sheet = Image.new("RGBA", (sheet_w, SHEET_H), (0, 0, 0, 0))
    # layout matches existing progressBar.json: fill | background | frame
    positions = {
        "progressBar.png": 1,
        "progressBarBackground.png": CELL_W + 2,
        "progressBarFrame.png": CELL_W * 2 + 3,
    }
    sheet.paste(fill, (positions["progressBar.png"], 1), fill)
    sheet.paste(bg, (positions["progressBarBackground.png"], 1), bg)
    sheet.paste(frame, (positions["progressBarFrame.png"], 1), frame)

    meta = {
        "frames": {
            name: {
                "frame": {"x": x, "y": 1, "w": CELL_W, "h": CELL_H},
                "rotated": False,
                "trimmed": False,
                "spriteSourceSize": {"x": 0, "y": 0, "w": CELL_W, "h": CELL_H},
                "sourceSize": {"w": CELL_W, "h": CELL_H},
            }
            for name, x in positions.items()
        },
        "meta": {
            "app": "game-builder/make_loading_chrome.py",
            "version": "1.0",
            "image": "progressBar.webp",
            "format": "RGBA8888",
            "size": {"w": sheet_w, "h": SHEET_H},
            "scale": "0.25",
        },
    }

    for p in (BAR_DIR / "progressBar.webp", BAR_DIR / "progressBar.png", BAR_DIR / "progressBar.json"):
        backup(p)

    png_path = BAR_DIR / "progressBar.png"
    webp_path = BAR_DIR / "progressBar.webp"
    json_path = BAR_DIR / "progressBar.json"
    sheet.save(png_path, format="PNG")
    sheet.save(webp_path, format="WEBP", quality=92, method=6)
    json_path.write_text(json.dumps(meta, indent=0) + "\n", encoding="utf-8")
    print(f"Wrote White Room progress bar -> {webp_path}")


# ── falling loading particles ────────────────────────────────────────────────

def load_sources() -> list[Image.Image]:
    """Prefer assets-raw/loading_particles; then win_particles/debris (NON-glass only)."""
    dirs = [
        RAW_DIR,
        APP / "assets-raw" / "win_particles" / "debris",
    ]
    out = []
    seen = set()
    for d in dirs:
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.png")):
            if p.name in seen or p.name.startswith("_OLD_") or "glass" in p.name.lower():
                continue
            try:
                out.append(Image.open(p).convert("RGBA"))
                seen.add(p.name)
            except Exception:
                continue
    return out


def draw_ceramic_chip(size: int, seed: int) -> Image.Image:
    """Equant porcelain tile chip — NOT elongated glass triangle knives."""
    rng = random.Random(seed)
    s = size * 2
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = cy = s / 2
    n = rng.randint(5, 7)
    pts = []
    for i in range(n):
        ang = (i / n) * math.tau + rng.uniform(-0.18, 0.18)
        rr = s * rng.uniform(0.28, 0.4)
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    d.polygon(pts, fill=BONE, outline=STEEL[:3] + (230,))
    if len(pts) >= 2:
        d.line([pts[0], pts[1]], fill=SILVER[:3] + (220,), width=2)
    if seed % 7 == 0:
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 1], fill=BLOOD)
    return img.resize((size, size), Image.Resampling.LANCZOS).rotate(
        rng.uniform(-40, 40), expand=True, resample=Image.Resampling.BICUBIC
    )


def draw_buckle_scrap(size: int, seed: int) -> Image.Image:
    rng = random.Random(seed + 33)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = size // 5
    d.rounded_rectangle([m, size // 3, size - m, size - size // 3], radius=2, fill=STEEL)
    d.rounded_rectangle(
        [size // 3, size // 2 - 4, size - size // 3, size // 2 + 4],
        radius=1,
        fill=CHARCOAL[:3] + (230,),
    )
    return img.rotate(rng.uniform(-35, 35), expand=True, resample=Image.Resampling.BICUBIC)


def draw_ceramic_dust(size: int, seed: int) -> Image.Image:
    rng = random.Random(seed + 99)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for _ in range(rng.randint(4, 9)):
        x = rng.randint(2, size - 4)
        y = rng.randint(2, size - 4)
        r = rng.randint(1, 3)
        col = BONE if rng.random() > 0.4 else SILVER
        d.ellipse([x, y, x + r, y + r], fill=col[:3] + (rng.randint(140, 230),))
    return img


def draw_pill(size: int, seed: int) -> Image.Image:
    rng = random.Random(seed + 404)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = size // 6
    # capsule: white + pale grey halves
    d.rounded_rectangle([m, size // 3, size // 2, size - size // 3], radius=size // 6, fill=BONE)
    d.rounded_rectangle([size // 2 - 1, size // 3, size - m, size - size // 3], radius=size // 6, fill=STEEL[:3] + (240,))
    d.line([(size // 2, size // 3 + 2), (size // 2, size - size // 3 - 2)], fill=CHARCOAL[:3] + (120,), width=1)
    return img.rotate(rng.uniform(-50, 50), expand=True, resample=Image.Resampling.BICUBIC)


def draw_file_scrap(size: int, seed: int) -> Image.Image:
    rng = random.Random(seed + 77)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [
        (rng.randint(4, 10), rng.randint(6, 14)),
        (size - rng.randint(4, 12), rng.randint(4, 10)),
        (size - rng.randint(6, 14), size - rng.randint(6, 12)),
        (rng.randint(6, 14), size - rng.randint(4, 10)),
    ]
    d.polygon(pts, fill=(236, 232, 224, 230), outline=STEEL[:3] + (200,))
    # typed line scraps
    for i in range(3):
        y = pts[0][1] + 6 + i * 5
        d.line([(pts[0][0] + 4, y), (pts[1][0] - 6, y)], fill=CHARCOAL[:3] + (90,), width=1)
    return img.rotate(rng.uniform(-25, 25), expand=True, resample=Image.Resampling.BICUBIC)


def draw_fluorescent_mote(size: int, seed: int) -> Image.Image:
    rng = random.Random(seed + 11)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = size // 2
    r = max(2, size // 5)
    d.ellipse([c - r, c - r, c + r, c + r], fill=FLUOR_CORE[:3] + (180,))
    d.ellipse([c - r // 2, c - r // 2, c + r // 2, c + r // 2], fill=(255, 255, 255, 230))
    return img.filter(ImageFilter.GaussianBlur(0.6))


def stamp_source(size: int, seed: int, sources: list[Image.Image]) -> Image.Image:
    src = sources[seed % len(sources)]
    scale = size * 0.85 / max(src.width, src.height)
    sw = max(8, int(src.width * scale))
    sh = max(8, int(src.height * scale))
    chip = src.resize((sw, sh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(chip, ((size - sw) // 2, (size - sh) // 2))
    return canvas


def build_particle_cell(size: int, kind: str, seed: int, sources: list[Image.Image]) -> Image.Image:
    # Scenario clinical stamps for chip+dust; procedural pills/scraps/motes/buckles.
    # ZERO glass shards.
    if sources and kind in ("chip", "dust"):
        return stamp_source(size, seed, sources)
    makers = {
        "chip": draw_ceramic_chip,
        "dust": draw_ceramic_dust,
        "pill": draw_pill,
        "scrap": draw_file_scrap,
        "mote": draw_fluorescent_mote,
        "buckle": draw_buckle_scrap,
    }
    return makers[kind](size, seed)


def write_loading_particles() -> None:
    PART_DIR.mkdir(parents=True, exist_ok=True)
    sources = load_sources()
    kinds = ["chip", "dust", "pill", "scrap", "mote", "buckle", "chip", "pill"]
    cell = 128
    cols, rows = 4, 2
    sheet_w, sheet_h = cols * cell, rows * cell
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    frames = {}
    for i, kind in enumerate(kinds):
        col, row = i % cols, i // cols
        chip = build_particle_cell(cell - 8, kind, 1897 + i * 17, sources)
        # center in cell
        cx = col * cell + (cell - chip.width) // 2
        cy = row * cell + (cell - chip.height) // 2
        name = f"{i + 1}.png"
        sheet.paste(chip, (cx, cy), chip)
        frames[name] = {
            "frame": {"x": col * cell, "y": row * cell, "w": cell, "h": cell},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": cell, "h": cell},
            "sourceSize": {"w": cell, "h": cell},
        }

    meta = {
        "frames": frames,
        "animations": {"fall": list(frames.keys())},
        "meta": {
            "app": "game-builder/make_loading_chrome.py",
            "version": "1.0",
            "image": "loadingParticles.webp",
            "format": "RGBA8888",
            "size": {"w": sheet_w, "h": sheet_h},
            "scale": "1",
        },
    }

    for p in (
        PART_DIR / "loadingParticles.webp",
        PART_DIR / "loadingParticles.png",
        PART_DIR / "loadingParticles.json",
    ):
        backup(p)

    png_path = PART_DIR / "loadingParticles.png"
    webp_path = PART_DIR / "loadingParticles.webp"
    json_path = PART_DIR / "loadingParticles.json"
    sheet.save(png_path, format="PNG")
    sheet.save(webp_path, format="WEBP", quality=90, method=6)
    json_path.write_text(json.dumps(meta, indent=0) + "\n", encoding="utf-8")
    mode = f"scenario-sources({len(sources)})" if sources else "procedural"
    print(f"Wrote White Room loading particles -> {webp_path} ({mode})")


def main() -> None:
    write_progress_bar()
    write_loading_particles()
    print("OK — loading chrome rebuilt for THE WHITE ROOM")


if __name__ == "__main__":
    main()
