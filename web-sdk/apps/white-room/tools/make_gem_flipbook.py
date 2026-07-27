"""Rebuild win-particle flipbook as THE WHITE ROOM clinical debris cascade.

PRIMARY win-particle concept (assets.winParticles.gems):
  ceramic tile chips, pill capsules, torn PATIENT 404 paper, padded-wall lint,
  fluorescent dust motes, restraint buckle scraps.
BANNED: Madam Mirror glass shards, triangle knives, crystals, coins, purple gems.

Optional Scenario source frames:
  Drop transparent NON-GLASS PNGs into assets-raw/win_particles/debris/.
  Old glass lived in win_particles/shards/ — quarantined to _OLD_GLASS_shards/ and NEVER loaded.
  If debris/ present, stamps tumble frames; otherwise procedural clinical debris.

Sheet layout stays SD2_Coin.json so WinCoins.svelte emitters keep working.

Run:  python tools/make_gem_flipbook.py
"""

from __future__ import annotations

import json
import math
import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

APP = Path(__file__).resolve().parents[1]
COIN_DIR = APP / "static" / "assets" / "sprites" / "coin"
BACKUP = APP / "assets-backup" / "gem_flipbook"
SRC_DIRS = [
    APP / "assets-raw" / "win_particles" / "debris",
]

SUPER = 2

BONE = (244, 241, 236)
SILVER = (200, 196, 188)
STEEL = (138, 134, 128)
DUST = (220, 218, 212)
CHARCOAL = (58, 54, 50)
BLOOD = (107, 42, 40)
PAPER = (236, 232, 224)
FLUOR = (232, 240, 245)
LEATHER = (74, 64, 56)


def lerp(a, b, f):
    return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))


def load_source_debris() -> list[Image.Image]:
    out: list[Image.Image] = []
    seen: set[str] = set()
    for src_dir in SRC_DIRS:
        if not src_dir.is_dir():
            continue
        for p in sorted(src_dir.glob("*.png")):
            # skip quarantined glass leftovers
            if p.name.startswith("_OLD_") or "glass" in p.name.lower():
                continue
            if p.name in seen:
                continue
            try:
                out.append(Image.open(p).convert("RGBA"))
                seen.add(p.name)
            except Exception:
                continue
    return out


def ceramic_poly(cx: float, cy: float, r: float, n: int, seed: int):
    """Chunky tile-chip silhouette — NOT elongated glass blades."""
    rng = random.Random(seed)
    pts = []
    for i in range(n):
        ang = (i / n) * math.tau + rng.uniform(-0.18, 0.18)
        rr = r * rng.uniform(0.72, 1.0)
        # keep roughly equant (tile chip), never needle-blade stretch
        x = cx + math.cos(ang) * rr
        y = cy + math.sin(ang) * rr * rng.uniform(0.85, 1.1)
        pts.append((x, y))
    return pts


def draw_pill(d: ImageDraw.ImageDraw, cx: float, cy: float, size: float, ang: float, dim: float):
    half = size * 0.55
    thick = size * 0.38
    # approximate capsule as two rounded halves via ellipses + body
    dx = math.cos(ang) * half
    dy = math.sin(ang) * half
    px = math.cos(ang + math.pi / 2) * thick
    py = math.sin(ang + math.pi / 2) * thick
    body = [
        (cx - dx + px, cy - dy + py),
        (cx + dx + px, cy + dy + py),
        (cx + dx - px, cy + dy - py),
        (cx - dx - px, cy - dy - py),
    ]
    d.polygon(body, fill=(*BONE, int(230 * dim)))
    # grey half cap
    d.ellipse(
        [cx + dx * 0.2 - thick, cy + dy * 0.2 - thick, cx + dx + thick * 0.9, cy + dy + thick * 0.9],
        fill=(*STEEL, int(220 * dim)),
    )
    d.ellipse(
        [cx - dx - thick * 0.9, cy - dy - thick * 0.9, cx - dx * 0.2 + thick, cy - dy * 0.2 + thick],
        fill=(*BONE, int(235 * dim)),
    )


def draw_paper_scrap(d: ImageDraw.ImageDraw, cx: float, cy: float, size: float, seed: int, dim: float):
    rng = random.Random(seed)
    pts = []
    for i in range(4):
        ang = (i / 4) * math.tau + rng.uniform(-0.2, 0.2)
        rr = size * rng.uniform(0.55, 1.0)
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * 0.75))
    d.polygon(pts, fill=(*PAPER, int(225 * dim)), outline=(*STEEL, int(180 * dim)))
    # typed line scraps / "404" hint as short bars
    for i in range(3):
        y = cy - size * 0.25 + i * size * 0.22
        d.line(
            [(cx - size * 0.35, y), (cx + size * 0.35, y)],
            fill=(*CHARCOAL, int(100 * dim)),
            width=max(1, int(size * 0.04)),
        )


def draw_buckle_scrap(d: ImageDraw.ImageDraw, cx: float, cy: float, size: float, dim: float):
    hw, hh = size * 0.7, size * 0.38
    d.rounded_rectangle(
        [cx - hw, cy - hh, cx + hw, cy + hh],
        radius=max(1, int(size * 0.08)),
        fill=(*STEEL, int(230 * dim)),
        outline=(*SILVER, int(200 * dim)),
    )
    d.rounded_rectangle(
        [cx - hw * 0.45, cy - hh * 0.45, cx + hw * 0.45, cy + hh * 0.45],
        radius=max(1, int(size * 0.05)),
        fill=(*CHARCOAL, int(220 * dim)),
    )
    # leather strap stub
    d.rectangle(
        [cx - hw * 1.15, cy - hh * 0.35, cx - hw * 0.85, cy + hh * 0.35],
        fill=(*LEATHER, int(210 * dim)),
    )


def draw_lint(d: ImageDraw.ImageDraw, cx: float, cy: float, size: float, seed: int, dim: float):
    """Soft padded-wall lint tufts — NOT radial glass-crack spikes."""
    rng = random.Random(seed)
    for _ in range(rng.randint(3, 6)):
        ox = cx + rng.uniform(-size * 0.35, size * 0.35)
        oy = cy + rng.uniform(-size * 0.35, size * 0.35)
        r = size * rng.uniform(0.12, 0.28)
        d.ellipse(
            [ox - r, oy - r * 0.85, ox + r, oy + r * 0.85],
            fill=(*DUST, int(rng.randint(70, 140) * dim)),
        )


def draw_procedural_debris_field(width: int, height: int, back: bool, frame_i: int) -> Image.Image:
    """Clinical debris cascade — ZERO glass shards / triangle knives."""
    s = SUPER
    w, h = width * s, height * s
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    dim = 0.68 if back else 1.0
    rng = random.Random(1897 + frame_i * 97)

    # soft fluorescent dust halo
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gx, gy = w * 0.5, h * 0.5
    ImageDraw.Draw(glow).ellipse(
        [gx - w * 0.4, gy - h * 0.4, gx + w * 0.4, gy + h * 0.4],
        fill=(*FLUOR, int(40 * dim)),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(max(4, int(min(w, h) * 0.08))))
    img.alpha_composite(glow)

    # fluorescent dust motes
    for i in range(22 + (frame_i % 6)):
        x = rng.uniform(w * 0.08, w * 0.92)
        y = rng.uniform(h * 0.08, h * 0.92)
        r = rng.uniform(0.5, 2.2) * s
        col = lerp(DUST, FLUOR, rng.random())
        a = int(rng.randint(80, 190) * dim)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(*col, a))

    # ceramic tile chips — OPAQUE porcelain (never translucent glass)
    for i in range(3 + (frame_i % 2)):
        cx = w * rng.uniform(0.22, 0.78)
        cy = h * rng.uniform(0.22, 0.78)
        r = min(w, h) * rng.uniform(0.1, 0.22)
        n = rng.randint(5, 7)
        pts = ceramic_poly(cx, cy, r, n, seed=frame_i * 31 + i)
        face = lerp(BONE, SILVER, rng.uniform(0.05, 0.4))
        d.polygon(pts, fill=(*face, int(245 * dim)))
        # grout/edge lip (tile, not glass specular)
        d.line(pts + [pts[0]], fill=(*STEEL, int(210 * dim)), width=max(2, s))
        # inner body darken to read as thickness
        if len(pts) >= 3:
            mx = sum(p[0] for p in pts) / len(pts)
            my = sum(p[1] for p in pts) / len(pts)
            inner = [((px + mx) * 0.5, (py + my) * 0.5) for px, py in pts]
            d.polygon(inner, fill=(*lerp(face, CHARCOAL, 0.12), int(200 * dim)))

    # pill capsules
    for i in range(1 + (frame_i % 2)):
        draw_pill(
            d,
            w * rng.uniform(0.25, 0.75),
            h * rng.uniform(0.25, 0.75),
            min(w, h) * rng.uniform(0.1, 0.16),
            rng.uniform(0, math.tau),
            dim,
        )

    # PATIENT 404 paper scraps
    if frame_i % 2 == 0:
        draw_paper_scrap(
            d,
            w * rng.uniform(0.3, 0.7),
            h * rng.uniform(0.3, 0.7),
            min(w, h) * rng.uniform(0.12, 0.2),
            seed=frame_i * 7 + 3,
            dim=dim,
        )

    # restraint buckle scrap
    if frame_i % 3 == 0:
        draw_buckle_scrap(
            d,
            w * rng.uniform(0.28, 0.72),
            h * rng.uniform(0.28, 0.72),
            min(w, h) * rng.uniform(0.08, 0.13),
            dim,
        )

    # padded-wall lint
    for i in range(2):
        draw_lint(
            d,
            w * rng.uniform(0.2, 0.8),
            h * rng.uniform(0.2, 0.8),
            min(w, h) * rng.uniform(0.06, 0.12),
            seed=frame_i * 11 + i,
            dim=dim,
        )

    # sparse dried-blood flecks only
    if frame_i % 5 == 0:
        bx = rng.uniform(w * 0.3, w * 0.7)
        by = rng.uniform(h * 0.3, h * 0.7)
        br = rng.uniform(1.0, 2.8) * s
        d.ellipse([bx - br, by - br * 0.7, bx + br, by + br * 0.7], fill=(*BLOOD, int(130 * dim)))

    return img.resize((width, height), Image.Resampling.LANCZOS)


def draw_from_sources(
    width: int, height: int, back: bool, frame_i: int, sources: list[Image.Image]
) -> Image.Image:
    """Stamp Scenario (or hand-authored) NON-glass debris into a tumbling cell."""
    s = SUPER
    w, h = width * s, height * s
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dim = 0.68 if back else 1.0
    rng = random.Random(404 + frame_i * 13)

    base = draw_procedural_debris_field(width, height, back, frame_i).resize((w, h), Image.Resampling.BILINEAR)
    muted = base.copy()
    muted.putalpha(muted.split()[3].point(lambda a: int(a * 0.3)))
    img.alpha_composite(muted)

    n_stamps = 3 + (frame_i % 3)
    for i in range(n_stamps):
        src = sources[(frame_i + i) % len(sources)]
        scale = rng.uniform(0.28, 0.55) * min(w, h) / max(src.width, src.height)
        sw = max(8, int(src.width * scale))
        sh = max(8, int(src.height * scale))
        chip = src.resize((sw, sh), Image.Resampling.LANCZOS)
        if back:
            dark = Image.new("RGBA", chip.size, (0, 0, 0, int(70 * dim)))
            chip = Image.alpha_composite(chip, dark)
        angle = rng.uniform(-55, 55) + frame_i * 15
        chip = chip.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
        px = int(rng.uniform(w * 0.08, max(w * 0.08, w - chip.width - w * 0.08)))
        py = int(rng.uniform(h * 0.08, max(h * 0.08, h - chip.height - h * 0.08)))
        img.alpha_composite(chip, (px, py))

    return img.resize((width, height), Image.Resampling.LANCZOS)


def draw_cell(width: int, height: int, back: bool, frame_i: int, sources: list[Image.Image]) -> Image.Image:
    if sources:
        return draw_from_sources(width, height, back, frame_i, sources)
    return draw_procedural_debris_field(width, height, back, frame_i)


def main() -> None:
    meta_path = COIN_DIR / "SD2_Coin.json"
    png_path = COIN_DIR / "SD2_Coin.png"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    frames = meta["frames"]
    with Image.open(png_path) as src:
        sheet_w, sheet_h = src.size

    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(png_path, BACKUP / "SD2_Coin.png.bak")

    sources = load_source_debris()
    mode = f"scenario-sources({len(sources)})" if sources else "procedural"

    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    names = sorted(frames.keys(), key=lambda n: int("".join(ch for ch in n if ch.isdigit()) or "0"))
    for i, name in enumerate(names):
        fr = frames[name]["frame"]
        x, y, w, h = fr["x"], fr["y"], fr["w"], fr["h"]
        back = i >= len(names) // 2
        chip = draw_cell(w, h, back=back, frame_i=i, sources=sources)
        sheet.paste(chip, (x, y), chip)

    tmp_path = png_path.parent / (png_path.stem + ".tmp.png")
    sheet.save(tmp_path, format="PNG")
    tmp_path.replace(png_path)
    print(f"Wrote White Room clinical debris flipbook -> {png_path} ({len(names)} frames, {mode})")


if __name__ == "__main__":
    main()
