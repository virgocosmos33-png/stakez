"""Rebuild bonus enter/exit transition Spine atlas for THE WHITE ROOM.

SMOKING GUN: FreeSpin enter/exit broadcasts `transition` → TransitionAnimation
loads spines/transition (rock1..rock8 = falling purple Madam diamonds).

This script OVERWRITES those rock slots with clinical debris ONLY:
  ceramic tile chips, pill capsules, PATIENT 404 paper, padded lint,
  fluorescent dust, restraint buckle scraps.
BANNED: purple diamonds, amethyst crystals, glass shards, triangle knives.

Also:
  - dust* → cool fluorescent clinical mist (no purple)
  - sparks* → cool white/silver fluorescent streaks (no green/violet)
  - quarantines previous purple diamond atlases so they cannot load
  - same rock/dust/sparks pass on anticipation spine (keeps frame/payframe)

Run:  python tools/make_transition_debris.py
"""

from __future__ import annotations

import colorsys
import math
import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

APP = Path(__file__).resolve().parents[1]
ASSETS = APP / "static" / "assets"
BACKUP = APP / "assets-backup" / "transition_debris"
QUARANTINE = APP / "assets-raw" / "_OLD_PURPLE_DIAMONDS"

BONE = (244, 241, 236)
SILVER = (200, 196, 188)
STEEL = (138, 134, 128)
DUST = (220, 218, 212)
CHARCOAL = (58, 54, 50)
PAPER = (236, 232, 224)
FLUOR = (232, 240, 245)
LEATHER = (74, 64, 56)
BLOOD = (107, 42, 40)


def lerp(a, b, f):
    return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))


def backup(path: Path) -> None:
    dest = BACKUP / path.relative_to(ASSETS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() and path.exists():
        shutil.copy2(path, dest)


def quarantine(path: Path, tag: str) -> None:
    """Copy purple diamond source out of load path (keep history)."""
    if not path.exists():
        return
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    dest = QUARANTINE / f"{tag}_{path.name}"
    shutil.copy2(path, dest)
    print(f"[quarantine] {path.name} -> {dest.relative_to(APP)}")


def parse_atlas_regions(atlas_path: Path) -> tuple[tuple[int, int], dict[str, tuple[int, int, int, int]]]:
    lines = atlas_path.read_text(encoding="utf-8").splitlines()
    page_size = (0, 0)
    regions: dict[str, tuple[int, int, int, int]] = {}
    name = None
    bounds: tuple[int, int, int, int] | None = None
    rotated = False

    def commit() -> None:
        nonlocal bounds, rotated
        if name and bounds:
            x, y, w, h = bounds
            if rotated:
                w, h = h, w
            regions[name] = (x, y, w, h)
        bounds, rotated = None, False

    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("size:") and page_size == (0, 0):
            w, h = stripped.split(":")[1].split(",")
            page_size = (int(w), int(h))
        elif ":" not in stripped and stripped:
            commit()
            name = stripped
        elif stripped.startswith("bounds:"):
            x, y, w, h = (int(v) for v in stripped.split(":")[1].split(","))
            bounds = (x, y, w, h)
        elif stripped.startswith("rotate:"):
            rotated = stripped.split(":")[1] in ("90", "270", "true")
    commit()
    return page_size, regions


def scaled_boxes(page_size, regions, image):
    sx = image.width / page_size[0]
    sy = image.height / page_size[1]
    out = {}
    for name, (x, y, w, h) in regions.items():
        out[name] = (
            max(int(x * sx) - 1, 0),
            max(int(y * sy) - 1, 0),
            min(int((x + w) * sx) + 1, image.width),
            min(int((y + h) * sy) + 1, image.height),
        )
    return out


def ceramic_poly(cx: float, cy: float, r: float, n: int, seed: int):
    """Chunky tile-chip — equant, NEVER elongated diamond blades."""
    rng = random.Random(seed)
    pts = []
    for i in range(n):
        ang = (i / n) * math.tau + rng.uniform(-0.18, 0.18)
        rr = r * rng.uniform(0.72, 1.0)
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * rng.uniform(0.85, 1.1)))
    return pts


def draw_pill(d: ImageDraw.ImageDraw, cx: float, cy: float, size: float, ang: float):
    half = size * 0.55
    thick = size * 0.38
    dx, dy = math.cos(ang) * half, math.sin(ang) * half
    px, py = math.cos(ang + math.pi / 2) * thick, math.sin(ang + math.pi / 2) * thick
    body = [
        (cx - dx + px, cy - dy + py),
        (cx + dx + px, cy + dy + py),
        (cx + dx - px, cy + dy - py),
        (cx - dx - px, cy - dy - py),
    ]
    d.polygon(body, fill=(*BONE, 235))
    d.ellipse(
        [cx + dx * 0.2 - thick, cy + dy * 0.2 - thick, cx + dx + thick * 0.9, cy + dy + thick * 0.9],
        fill=(*STEEL, 225),
    )
    d.ellipse(
        [cx - dx - thick * 0.9, cy - dy - thick * 0.9, cx - dx * 0.2 + thick, cy - dy * 0.2 + thick],
        fill=(*BONE, 240),
    )


def draw_paper(d: ImageDraw.ImageDraw, cx: float, cy: float, size: float, seed: int):
    """Torn rectangular PATIENT 404 scrap — NOT a diamond rhombus."""
    rng = random.Random(seed)
    hw = size * rng.uniform(0.55, 0.75)
    hh = size * rng.uniform(0.35, 0.5)
    # slight torn corners (still axis-aligned rectangle family)
    pts = [
        (cx - hw + rng.uniform(0, size * 0.08), cy - hh),
        (cx + hw, cy - hh + rng.uniform(0, size * 0.06)),
        (cx + hw - rng.uniform(0, size * 0.1), cy + hh),
        (cx - hw, cy + hh - rng.uniform(0, size * 0.05)),
    ]
    d.polygon(pts, fill=(*PAPER, 235), outline=(*STEEL, 190))
    for i in range(3):
        y = cy - hh * 0.45 + i * (hh * 0.4)
        d.line(
            [(cx - hw * 0.7, y), (cx + hw * 0.7, y)],
            fill=(*CHARCOAL, 120),
            width=max(1, int(size * 0.045)),
        )
    # faint "404" bars
    d.line(
        [(cx - hw * 0.25, cy + hh * 0.55), (cx + hw * 0.25, cy + hh * 0.55)],
        fill=(*BLOOD, 90),
        width=max(1, int(size * 0.03)),
    )


def draw_buckle(d: ImageDraw.ImageDraw, cx: float, cy: float, size: float):
    hw, hh = size * 0.7, size * 0.38
    d.rounded_rectangle(
        [cx - hw, cy - hh, cx + hw, cy + hh],
        radius=max(1, int(size * 0.08)),
        fill=(*STEEL, 235),
        outline=(*SILVER, 200),
    )
    d.rounded_rectangle(
        [cx - hw * 0.45, cy - hh * 0.45, cx + hw * 0.45, cy + hh * 0.45],
        radius=max(1, int(size * 0.05)),
        fill=(*CHARCOAL, 225),
    )
    d.rectangle(
        [cx - hw * 1.15, cy - hh * 0.35, cx - hw * 0.85, cy + hh * 0.35],
        fill=(*LEATHER, 215),
    )


def draw_lint(d: ImageDraw.ImageDraw, cx: float, cy: float, size: float, seed: int):
    rng = random.Random(seed)
    for _ in range(rng.randint(3, 6)):
        ox = cx + rng.uniform(-size * 0.35, size * 0.35)
        oy = cy + rng.uniform(-size * 0.35, size * 0.35)
        r = size * rng.uniform(0.12, 0.28)
        d.ellipse(
            [ox - r, oy - r * 0.85, ox + r, oy + r * 0.85],
            fill=(*DUST, rng.randint(70, 140)),
        )


def draw_clinical_debris_piece(width: int, height: int, seed: int) -> Image.Image:
    """Single debris stamp sized to a Spine rock slot — ZERO diamonds/crystals."""
    rng = random.Random(seed)
    s = 3
    w, h = max(8, width * s), max(8, height * s)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = w * 0.5, h * 0.5
    m = min(w, h)

    # Cycle clinical kinds — NEVER nested-facet gem / elongated diamond
    kind = seed % 6
    if kind == 0:
        # flat ceramic TILE chip (hex-ish), grout edge only — no inner facet ring
        r = m * rng.uniform(0.34, 0.46)
        pts = ceramic_poly(cx, cy, r, 6, seed)
        face = lerp(BONE, SILVER, rng.uniform(0.05, 0.35))
        d.polygon(pts, fill=(*face, 250))
        d.line(pts + [pts[0]], fill=(*STEEL, 220), width=max(2, s))
        # matte grout scratch (tile, not gem specular)
        d.line(
            [(cx - r * 0.35, cy - r * 0.1), (cx + r * 0.4, cy + r * 0.15)],
            fill=(*STEEL, 90),
            width=max(1, s // 2),
        )
    elif kind == 1:
        draw_pill(d, cx, cy, m * 0.4, rng.uniform(-0.4, 0.4))
    elif kind == 2:
        draw_paper(d, cx, cy, m * 0.42, seed)
    elif kind == 3:
        draw_buckle(d, cx, cy, m * 0.34)
    elif kind == 4:
        draw_lint(d, cx, cy, m * 0.44, seed)
        # small round ceramic fleck (circle — cannot read as diamond)
        rr = m * 0.14
        d.ellipse([cx - rr, cy - rr * 0.9, cx + rr, cy + rr * 0.9], fill=(*SILVER, 230))
        d.ellipse(
            [cx - rr * 0.5, cy - rr * 0.45, cx + rr * 0.5, cy + rr * 0.45],
            fill=(*STEEL, 120),
        )
    else:
        # fluorescent dust mote cluster only (no crystal centerpiece)
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse(
            [cx - m * 0.35, cy - m * 0.35, cx + m * 0.35, cy + m * 0.35],
            fill=(*FLUOR, 55),
        )
        glow = glow.filter(ImageFilter.GaussianBlur(max(3, int(m * 0.08))))
        img.alpha_composite(glow)
        for i in range(14):
            x = cx + rng.uniform(-m * 0.32, m * 0.32)
            y = cy + rng.uniform(-m * 0.32, m * 0.32)
            rr = rng.uniform(0.8, 2.6) * s
            col = lerp(DUST, FLUOR, rng.random())
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(*col, rng.randint(100, 200)))
        # tiny pill fleck so slot isn't empty dust only
        draw_pill(d, cx, cy, m * 0.18, rng.uniform(0, math.tau))

    # sparse dried-blood fleck only on larger pieces
    if m > 40 and seed % 7 == 0:
        br = m * 0.04
        d.ellipse(
            [cx + m * 0.15 - br, cy + m * 0.1 - br * 0.7, cx + m * 0.15 + br, cy + m * 0.1 + br * 0.7],
            fill=(*BLOOD, 120),
        )

    return img.resize((width, height), Image.Resampling.LANCZOS)


def purple_to_clinical_dust(r, g, b, a):
    """Any purple/violet mist → cool fluorescent clinical dust (keeps alpha/luma)."""
    if a < 4:
        return r, g, b, a
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    # purple / magenta / violet bands
    if sat > 0.08 and 0.55 < h < 0.92:
        # cool steel-white fluorescent
        l = min(l * 1.15 + 0.05, 0.96)
        sat = sat * 0.08
        h = 0.55  # slight cool cyan-grey
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    # warm brown dust → pale clinical grey
    if sat > 0.08 and (h < 0.12 or h > 0.92):
        l = min(l * 1.1 + 0.04, 0.94)
        sat = sat * 0.12
        h = 0.12
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


def spark_to_fluorescent(r, g, b, a):
    """Green/violet sparks → cool white fluorescent streaks."""
    if a < 4:
        return r, g, b, a
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if sat > 0.12:
        l = min(l * 1.2 + 0.08, 0.98)
        sat = sat * 0.1
        h = 0.55
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


def transform_region(image: Image.Image, box, pixel_fn) -> None:
    region = image.crop(box)
    pixels = region.load()
    w, h = region.size
    for py in range(h):
        for px in range(w):
            r, g, b, a = pixels[px, py]
            if a == 0:
                continue
            pixels[px, py] = pixel_fn(r, g, b, a)
    image.paste(region, box[:2])


def is_purple_pixel(r, g, b, a) -> bool:
    """Detect Madam amethyst / lavender diamond hues (including desaturated glass)."""
    if a < 20:
        return False
    # blue/red channel dominance typical of lavender (B and R both high vs G)
    if b > g + 12 and r > g + 4 and (r + b) > 180:
        return True
    hh, ll, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if sat > 0.10 and 0.55 < hh < 0.92 and 0.12 < ll < 0.97:
        return True
    return False


def purple_pixel_ratio(image: Image.Image, box) -> float:
    region = image.crop(box)
    pixels = region.load()
    w, h = region.size
    total = 0
    purple = 0
    for py in range(h):
        for px in range(w):
            r, g, b, a = pixels[px, py]
            if a < 20:
                continue
            total += 1
            if is_purple_pixel(r, g, b, a):
                purple += 1
    return (purple / total) if total else 0.0


def scrub_purple_in_box(image: Image.Image, box) -> None:
    """Force any leftover purple in a region to clinical grey (alpha preserved)."""
    region = image.crop(box)
    pixels = region.load()
    w, h = region.size
    for py in range(h):
        for px in range(w):
            r, g, b, a = pixels[px, py]
            if not is_purple_pixel(r, g, b, a):
                continue
            # map luma to bone/steel clinical grey
            luma = int(0.299 * r + 0.587 * g + 0.114 * b)
            if luma > 200:
                pixels[px, py] = (*BONE, a)
            elif luma > 140:
                pixels[px, py] = (*SILVER, a)
            else:
                pixels[px, py] = (*STEEL, a)
    image.paste(region, box[:2])


def rebuild_spine_atlas(folder: Path, atlas_name: str, keep: set[str] | None = None) -> None:
    keep = keep or set()
    atlas_path = folder / atlas_name
    page_size, regions = parse_atlas_regions(atlas_path)
    tag = folder.name

    for page in (f"{folder.name}.webp", f"{folder.name}.png"):
        path = folder / page
        if not path.exists():
            continue
        # quarantine once per page name (skip if already quarantined this run)
        qdest = QUARANTINE / f"{tag}_{path.name}"
        if not qdest.exists():
            quarantine(path, tag)
        backup(path)
        image = Image.open(path).convert("RGBA")
        boxes = scaled_boxes(page_size, regions, image)

        # 1) dust/sparks first so padded rock checks don't see purple mist
        for name, box in boxes.items():
            if name in keep:
                continue
            if name.startswith("dust") or name.startswith("glow") or name.startswith("radial"):
                transform_region(image, box, purple_to_clinical_dust)
                scrub_purple_in_box(image, box)
            elif name.startswith("sparks") or name.startswith("payframe_particles"):
                transform_region(image, box, spark_to_fluorescent)
                scrub_purple_in_box(image, box)

        # 2) rocks: full wipe + clinical debris stamp + purple scrub
        for name, box in boxes.items():
            if name in keep or not name.startswith("rock"):
                continue
            x0, y0, x1, y1 = box
            w, h = x1 - x0, y1 - y0
            if w < 2 or h < 2:
                continue
            image.paste(Image.new("RGBA", (w, h), (0, 0, 0, 0)), (x0, y0))
            piece = draw_clinical_debris_piece(
                max(4, w - 2), max(4, h - 2), seed=sum(ord(c) for c in name) * 17 + w + h
            )
            image.alpha_composite(piece, (x0 + 1, y0 + 1))
            scrub_purple_in_box(image, box)

        # HARD FAIL if rock regions still read purple
        for name, box in boxes.items():
            if not name.startswith("rock"):
                continue
            ratio = purple_pixel_ratio(image, box)
            if ratio > 0.005:
                raise SystemExit(
                    f"HARD FAIL: {path.name}:{name} still {ratio:.1%} purple diamond pixels"
                )

        # atomic write — OneDrive/Windows sometimes locks *.webp mid-save
        fmt = "WEBP" if path.suffix.lower() == ".webp" else "PNG"
        tmp = path.parent / f"{path.stem}.tmp{path.suffix}"
        image.save(tmp, format=fmt)
        tmp.replace(path)
        print(f"[{tag}] clinical debris wrote {page}")


def quarantine_loose_purple_scans() -> None:
    """Move known purple gem QA scans out of static load paths."""
    scans = [
        ASSETS / "sprites" / "mirror" / "_qa_scan" / "loader_gems.png",
    ]
    for p in scans:
        if not p.exists():
            continue
        quarantine(p, "qa_scan")
        # neutralize in place so accidental loads show nothing purple
        Image.new("RGBA", (8, 8), (0, 0, 0, 0)).save(p)
        print(f"[quarantine] neutralized {p.relative_to(APP)}")


def main() -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    # PRIMARY: bonus enter/exit shower
    rebuild_spine_atlas(ASSETS / "spines" / "transition", "transition.atlas")

    # SAME purple rock set used on anticipation — kill diamonds there too
    rebuild_spine_atlas(
        ASSETS / "spines" / "anticipation",
        "anticipation.atlas",
        keep={"frame", "frame1", "frame2", "frame3", "frame4", "payframe"},
    )

    quarantine_loose_purple_scans()
    print("done — transition + anticipation rocks are White Room clinical debris")


if __name__ == "__main__":
    main()
