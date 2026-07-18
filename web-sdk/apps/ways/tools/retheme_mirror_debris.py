"""Retheme Mining-Mayhem template atlases for Madam Mirror (haunted seance).

Waves covered (parity with the previous game's retheme_purple_rocks/retheme_ui):
  1. transition spine  — purple mining rocks -> silver-violet mirror-glass shards,
     red sparks -> green candle embers (region-aware via .atlas bounds)
  2. anticipation spine — red-brown rocks / orange glow -> violet glass + violet
     glow; gold reel frames and payframe kept untouched
  3. fsIntro fs_screen — saloon wood panels -> haunted ebony-violet parlor panels
  4. coin flipbook     — gold shiba coins -> antique silver seance tokens

Every touched file is backed up under assets-backup/ once (first run only).
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
BACKUP = APP / "assets-backup" / "retheme_mirror_debris"


# ---------------------------------------------------------------- utilities
def backup(path: Path) -> None:
    dest = BACKUP / path.relative_to(ASSETS)
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def parse_atlas_regions(atlas_path: Path) -> tuple[tuple[int, int], dict[str, tuple[int, int, int, int]]]:
    """Return (page_size, {region: (x, y, w, h)}) — w/h swapped for rotated regions."""
    lines = atlas_path.read_text().splitlines()
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


def transform_region(image: Image.Image, box: tuple[int, int, int, int], pixel_fn) -> None:
    """Apply pixel_fn(r,g,b,a)->(r,g,b,a) to a crop in place."""
    region = image.crop(box)
    pixels = region.load()
    width, height = region.size
    for py in range(height):
        for px in range(width):
            r, g, b, a = pixels[px, py]
            if a == 0:
                continue
            pixels[px, py] = pixel_fn(r, g, b, a)
    image.paste(region, box)


def scaled_boxes(page_size, regions, image):
    """Scale atlas region boxes onto an image page that may differ in size."""
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


# ------------------------------------------------------------ pixel recipes
def purple_rock_to_mirror_glass(r, g, b, a):
    """Saturated purple rock -> silver-lavender faceted glass."""
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if 0.6 < h < 0.87 and sat > 0.12:
        l = min(l * 1.45 + 0.10, 0.97)  # glass is brighter
        sat = sat * 0.32                # and far less saturated
        h = 0.73                        # cool lavender-silver
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


def red_spark_to_ember(r, g, b, a):
    """Red mining sparks -> seance candle embers (green)."""
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if (h < 0.09 or h > 0.93) and sat > 0.25:
        h = 0.38  # 0x2bff66-ish green
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


def rust_to_violet_glass(r, g, b, a):
    """Anticipation red-brown rocks -> violet mirror shards."""
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if h < 0.13 or h > 0.9 or (h < 0.2 and sat < 0.45):
        l = min(l * 1.25 + 0.06, 0.96)
        sat = min(sat * 0.55, 0.5)
        h = 0.75
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


def orange_glow_to_violet(r, g, b, a):
    """Warm mining glow/dust/sparks -> spectral violet (keeps luminance)."""
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if (h < 0.17 or h > 0.86) and sat > 0.05:
        h = 0.76
        sat = min(sat * 1.05, 1.0)
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


def wood_to_haunted_ebony(r, g, b, a):
    """Saloon wood -> near-black violet parlor panel. Silver frame untouched."""
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    is_woodish = (h < 0.16 or h > 0.86) and sat > 0.06
    if is_woodish:
        l = l * 0.55
        sat = min(sat * 0.7 + 0.05, 0.45)
        h = 0.78
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


def gold_coin_to_silver_token(r, g, b, a):
    """Gold coin -> antique silver seance token with a cold violet cast."""
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if 0.05 < h < 0.2 and sat > 0.15:
        sat = sat * 0.16
        h = 0.72
        l = min(l * 1.06, 0.97)
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


# ------------------------------------------------------------------- waves
def retheme_transition() -> None:
    folder = ASSETS / "spines" / "transition"
    page_size, regions = parse_atlas_regions(folder / "transition.atlas")
    for page in ("transition.webp", "transition.png"):
        path = folder / page
        backup(path)
        image = Image.open(path).convert("RGBA")
        boxes = scaled_boxes(page_size, regions, image)
        for name, box in boxes.items():
            if name.startswith("rock"):
                transform_region(image, box, purple_rock_to_mirror_glass)
            elif name.startswith("sparks"):
                transform_region(image, box, red_spark_to_ember)
            # dust stays: pale violet mist already fits the mirror palette
        image.save(path)
        print(f"[transition] rethemed {page}")


def retheme_anticipation() -> None:
    folder = ASSETS / "spines" / "anticipation"
    page_size, regions = parse_atlas_regions(folder / "anticipation.atlas")
    keep = {"frame", "frame1", "frame2", "frame3", "frame4", "payframe", "payframe_particles"}
    for page in ("anticipation.webp", "anticipation.png"):
        path = folder / page
        backup(path)
        image = Image.open(path).convert("RGBA")
        boxes = scaled_boxes(page_size, regions, image)
        for name, box in boxes.items():
            if name in keep:
                continue
            if name.startswith("rock"):
                transform_region(image, box, rust_to_violet_glass)
            else:  # radial*, glow*, sparks_*, dust*
                transform_region(image, box, orange_glow_to_violet)
        image.save(path)
        print(f"[anticipation] rethemed {page}")


def retheme_fs_intro() -> None:
    folder = ASSETS / "spines" / "fsIntro"
    for page in ("fs_screen.webp", "fs_screen.png"):
        path = folder / page
        backup(path)
        image = Image.open(path).convert("RGBA")
        transform_region(image, (0, 0, image.width, image.height), wood_to_haunted_ebony)
        image.save(path)
        print(f"[fsIntro] rethemed {page}")


def retheme_coin() -> None:
    path = ASSETS / "sprites" / "coin" / "SD2_Coin.png"
    backup(path)
    image = Image.open(path).convert("RGBA")
    transform_region(image, (0, 0, image.width, image.height), gold_coin_to_silver_token)
    image.save(path)
    print("[coin] rethemed SD2_Coin.png")


def gold_text_to_spectral_silver(r, g, b, a):
    """Saloon-gold lettering -> antique silver with a violet cast."""
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if 0.02 < h < 0.2 and sat > 0.2:
        sat = sat * 0.22
        h = 0.74
        l = min(l * 1.12 + 0.03, 0.97)
        nr, ng, nb = colorsys.hls_to_rgb(h, l, sat)
        return int(nr * 255), int(ng * 255), int(nb * 255), a
    return r, g, b, a


def retheme_free_spins_text() -> None:
    folder = ASSETS / "sprites" / "freeSpins"
    for page in ("freeSpins.png", "freeSpins.webp"):
        path = folder / page
        if not path.exists():
            continue
        backup(path)
        image = Image.open(path).convert("RGBA")
        transform_region(image, (0, 0, image.width, image.height), gold_text_to_spectral_silver)
        image.save(path)
        print(f"[freeSpins] rethemed {page}")


# ------------------------------------------------- wave 6: true shard art
def draw_glass_shard(width: int, height: int, seed: int) -> Image.Image:
    """Paint an angular mirror-glass shard (with glow) sized width x height.

    Replaces rock textures outright instead of recoloring them, so nothing
    rock-shaped survives. Drawn 4x supersampled.
    """
    rng = random.Random(seed)
    s = 4
    w, h = width * s, height * s
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # long axis corner-to-corner with jitter; sharp tips, jagged flanks
    flip = rng.random() < 0.5
    tip_a = (w * rng.uniform(0.08, 0.3), h * rng.uniform(0.0, 0.14))
    tip_b = (w * rng.uniform(0.7, 0.92), h * rng.uniform(0.86, 1.0))
    if flip:
        tip_a, tip_b = (w - tip_a[0], tip_a[1]), (w - tip_b[0], tip_b[1])
    axis = (tip_b[0] - tip_a[0], tip_b[1] - tip_a[1])
    length = math.hypot(*axis)
    nx, ny = -axis[1] / length, axis[0] / length  # unit normal

    def flank(side: int) -> list[tuple[float, float]]:
        points = []
        for i in range(1, rng.randint(2, 3) + 1):
            f = i / (rng.randint(2, 3) + 1) + rng.uniform(-0.08, 0.08)
            f = min(max(f, 0.12), 0.88)
            spread = (w + h) * 0.5 * rng.uniform(0.1, 0.24)
            points.append(
                (
                    tip_a[0] + axis[0] * f + nx * spread * side,
                    tip_a[1] + axis[1] * f + ny * spread * side,
                )
            )
        return points

    poly = [tip_a, *flank(1), tip_b, *reversed(flank(-1))]

    # glow halo behind the shard
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).polygon(poly, fill=(150, 105, 235, 200))
    glow = glow.filter(ImageFilter.GaussianBlur((w + h) * 0.045))
    img.alpha_composite(glow)

    # body: vertical lilac -> deep violet gradient clipped to the shard
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    body = Image.new("RGBA", (w, h))
    top, bottom = (228, 214, 252, 255), (112, 84, 180, 255)
    px = body.load()
    for y in range(h):
        f = y / max(h - 1, 1)
        row = tuple(int(top[i] + (bottom[i] - top[i]) * f) for i in range(4))
        for x in range(w):
            px[x, y] = row
    img.paste(body, (0, 0), mask)

    # facets: triangles from the centroid, alternating light/shadow
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    facets = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(facets)
    for i, point in enumerate(poly):
        nxt = poly[(i + 1) % len(poly)]
        shade = rng.uniform(-1, 1)
        color = (255, 255, 255, int(70 * abs(shade))) if shade > 0 else (30, 8, 60, int(60 * abs(shade)))
        fdraw.polygon([point, nxt, (cx, cy)], fill=color)
    img.alpha_composite(Image.composite(facets, Image.new("RGBA", (w, h), (0, 0, 0, 0)), mask))

    # crisp white rim + specular streak near the upper tip
    rim = ImageDraw.Draw(img)
    rim.line([*poly, poly[0]], fill=(255, 255, 255, 215), width=max(2, s))
    spec_f = rng.uniform(0.15, 0.35)
    spec = (tip_a[0] + axis[0] * spec_f, tip_a[1] + axis[1] * spec_f)
    spec2 = (spec[0] + axis[0] * 0.22 + nx * 6, spec[1] + axis[1] * 0.22 + ny * 6)
    rim.line([spec, spec2], fill=(255, 255, 255, 235), width=max(3, int(s * 1.5)))

    return img.resize((width, height), Image.LANCZOS)


def draw_mirror_medallion(size: int, seed: int) -> Image.Image:
    """Round hand-mirror medallion: silver rim, violet glass, specular sweep."""
    rng = random.Random(seed)
    s = 4
    d = size * s
    img = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = d / 2
    radius = d / 2 - s

    # silver rim (two tones for bevel)
    draw.circle((cx, cy), radius, fill=(212, 214, 224, 255))
    draw.circle((cx, cy), radius * 0.985, fill=(148, 148, 162, 255))
    # violet glass face: vertical gradient
    face_r = radius * 0.9
    top, bottom = (196, 168, 244), (74, 48, 130)
    steps = 60
    for i in range(steps):
        f = i / (steps - 1)
        color = tuple(int(top[c] + (bottom[c] - top[c]) * f) for c in range(3))
        y0 = cy - face_r + (2 * face_r) * i / steps
        y1 = cy - face_r + (2 * face_r) * (i + 1) / steps
        draw.rectangle([cx - face_r, y0, cx + face_r, y1], fill=(*color, 255))
    # clip face to circle: redraw ring mask
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).circle((cx, cy), face_r, fill=255)
    face = img.copy()
    img = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.circle((cx, cy), radius, fill=(210, 212, 222, 255))
    inner = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    inner.paste(face, (0, 0), mask)
    img.alpha_composite(inner)
    draw = ImageDraw.Draw(img)
    draw.circle((cx, cy), radius, outline=(240, 242, 250, 255), width=max(2, s))
    draw.circle((cx, cy), face_r, outline=(90, 70, 140, 220), width=max(2, s // 2))

    # diagonal specular sweep across the glass
    sweep = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sweep)
    offset = rng.uniform(-0.2, 0.2) * d
    sdraw.polygon(
        [
            (cx - face_r + offset, cy - face_r),
            (cx - face_r * 0.35 + offset, cy - face_r),
            (cx + face_r * 0.1 + offset, cy + face_r),
            (cx - face_r * 0.55 + offset, cy + face_r),
        ],
        fill=(255, 255, 255, 70),
    )
    sdraw.polygon(
        [
            (cx + face_r * 0.3 + offset, cy - face_r),
            (cx + face_r * 0.52 + offset, cy - face_r),
            (cx + face_r * 0.8 + offset, cy + face_r),
            (cx + face_r * 0.58 + offset, cy + face_r),
        ],
        fill=(255, 255, 255, 40),
    )
    sweep_masked = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    sweep_masked.paste(sweep, (0, 0), mask)
    img.alpha_composite(sweep_masked)

    return img.resize((size, size), Image.LANCZOS)


def retheme_symbol_coins() -> None:
    """Swap the royal-win gold coin discs for round mirror medallions."""
    folder = ASSETS / "spines" / "symbols"
    page_size, regions = parse_atlas_regions(folder / "symbols.atlas")
    for page in ("symbols.webp", "symbols.png"):
        path = folder / page
        backup(path)
        image = Image.open(path).convert("RGBA")
        boxes = scaled_boxes(page_size, regions, image)
        for name, box in boxes.items():
            if not name.endswith("_coin"):
                continue
            x0, y0, x1, y1 = box
            w, h = x1 - x0, y1 - y0
            size = min(w, h)
            image.paste(Image.new("RGBA", (w, h), (0, 0, 0, 0)), (x0, y0))
            medallion = draw_mirror_medallion(size, sum(ord(c) for c in name))
            image.alpha_composite(medallion, (x0 + (w - size) // 2, y0 + (h - size) // 2))
        image.save(path)
        print(f"[symbols] coin discs -> mirror medallions in {page}")


def replace_transition_rocks() -> None:
    """Overwrite the transition rock textures with real glass-shard art."""
    folder = ASSETS / "spines" / "transition"
    page_size, regions = parse_atlas_regions(folder / "transition.atlas")
    for page in ("transition.webp", "transition.png"):
        path = folder / page
        backup(path)
        image = Image.open(path).convert("RGBA")
        boxes = scaled_boxes(page_size, regions, image)
        for name, box in boxes.items():
            if not name.startswith("rock"):
                continue
            x0, y0, x1, y1 = box
            # clear the old rock pixels entirely
            image.paste(Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0)), (x0, y0))
            seed = sum(ord(c) for c in name)
            shard = draw_glass_shard(x1 - x0 - 4, y1 - y0 - 4, seed)
            image.alpha_composite(shard, (x0 + 2, y0 + 2))
        image.save(path)
        print(f"[transition] rocks -> glass shards in {page}")


if __name__ == "__main__":
    import sys

    if "shards" in sys.argv:
        replace_transition_rocks()
    elif "medallions" in sys.argv:
        retheme_symbol_coins()
    else:
        retheme_transition()
        retheme_anticipation()
        retheme_fs_intro()
        retheme_coin()
        retheme_free_spins_text()
    print("done")
