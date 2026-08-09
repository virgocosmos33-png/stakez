"""Rebuild symbols3 explosion flipbook for THE WHITE ROOM (no amber/gold Madam Mirror).

Uses tools/symbol_art/fx_explosion_white_room.png (Scenario porcelain/silver burst)
to synthesize symbexpl_01..13 frames, then rewrites symbols3.webp/.atlas regions
in place. Skeleton JSON animation timing is preserved.

Run via DramaStudioMCP regenerate_assets scope=spines (or python this file).
"""
from __future__ import annotations

import io
import os
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
APP = HERE.parent
ART = HERE / "symbol_art" / "fx_explosion_white_room.png"
OUT = APP / "static" / "assets" / "spines" / "symbols3"
ATLAS = OUT / "symbols3.atlas"
WEBP = OUT / "symbols3.webp"
PNG = OUT / "symbols3.png"

CELL = 240
N_FRAMES = 13


def robust_write(path: Path, data: bytes, attempts: int = 8) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    for i in range(attempts):
        try:
            with open(tmp, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
            return
        except OSError:
            time.sleep(0.6 * (i + 1))
    raise SystemExit(f"could not write {path}")


def parse_atlas(text: str):
    lines = text.splitlines()
    page = lines[0]
    meta = []
    regions = {}
    i = 1
    while i < len(lines) and ":" in lines[i] and not lines[i].startswith("bounds"):
        meta.append(lines[i])
        i += 1
    while i < len(lines):
        name = lines[i].strip()
        i += 1
        props = {}
        while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t") or ":" in lines[i]):
            if ":" not in lines[i]:
                break
            # region props are unindented "key:val" in this atlas style
            if lines[i][0] not in " \t" and lines[i].split(":", 1)[0] not in (
                "bounds", "offsets", "rotate", "size", "filter", "scale",
            ):
                break
            k, v = lines[i].split(":", 1)
            props[k.strip()] = v.strip()
            i += 1
        if name:
            regions[name] = props
    return page, meta, regions


def make_frames(master: Image.Image) -> list[Image.Image]:
    """Synthesize 13-frame porcelain burst from a mid-burst master plate."""
    base = master.convert("RGBA")
    # key near-black bg
    arr = np.array(base).astype(np.float32)
    rgb = arr[..., :3]
    a = arr[..., 3]
    lum = rgb.mean(axis=2)
    # dark void -> transparent
    a = np.where(lum < 18, 0, a)
    # desaturate any warm leftover toward silver
    grey = lum
    cool = np.stack([
        np.clip(grey * 0.98 + 8, 0, 255),
        np.clip(grey * 0.96 + 6, 0, 255),
        np.clip(grey * 0.92 + 4, 0, 255),
    ], axis=2)
    # kill gold/amber: where R>>B, pull toward grey
    warm = (rgb[..., 0] > rgb[..., 2] + 25) & (rgb[..., 0] > rgb[..., 1] + 10)
    cool[warm] = np.stack([grey, grey, grey], axis=2)[warm]
    arr = np.dstack([cool, a]).astype(np.uint8)
    plate = Image.fromarray(arr, "RGBA")
    # center-crop / fit into CELL
    plate = plate.resize((CELL, CELL), Image.LANCZOS)

    frames = []
    for i in range(N_FRAMES):
        t = i / (N_FRAMES - 1)  # 0..1
        # scale envelope: small -> peak mid -> fade
        if t < 0.45:
            scale = 0.25 + 0.95 * (t / 0.45)
            alpha = 0.35 + 0.65 * (t / 0.45)
        else:
            u = (t - 0.45) / 0.55
            scale = 1.2 + 0.55 * u
            alpha = max(0.0, 1.0 - u * 1.05)
        w = max(8, int(CELL * scale))
        resized = plate.resize((w, w), Image.LANCZOS)
        canvas = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
        x = (CELL - w) // 2
        y = (CELL - w) // 2
        # apply global alpha
        r = np.array(resized).astype(np.float32)
        r[..., 3] *= alpha
        resized = Image.fromarray(r.astype(np.uint8), "RGBA")
        if t > 0.55:
            resized = resized.filter(ImageFilter.GaussianBlur(radius=0.6 + 2.2 * (t - 0.55)))
        canvas.alpha_composite(resized, (x, y))
        frames.append(canvas)
    return frames


def main() -> None:
    if not ART.is_file():
        raise SystemExit(f"missing {ART} — generate via Scenario first")
    master = Image.open(ART)
    frames = make_frames(master)

    page_name, meta, regions = parse_atlas(ATLAS.read_text(encoding="utf-8"))
    sheet = Image.open(WEBP).convert("RGBA") if WEBP.is_file() else Image.open(PNG).convert("RGBA")

    for idx in range(1, N_FRAMES + 1):
        name = f"symbexpl_{idx:02d}"
        props = regions.get(name)
        if not props or "bounds" not in props:
            print(f"[warn] no atlas region {name}")
            continue
        x, y, w, h = map(int, props["bounds"].split(","))
        # paste resized frame into existing cell (may be smaller than CELL)
        cell = frames[idx - 1].resize((w, h), Image.LANCZOS)
        sheet.paste(cell, (x, y))
        print(f"[ok] {name} @ {x},{y} {w}x{h}")

    # also recolor exp_circle / radial / rays if present — force cool silver
    for name in ("exp_circle", "radial", "rays1", "rays2"):
        props = regions.get(name)
        if not props or "bounds" not in props:
            continue
        x, y, w, h = map(int, props["bounds"].split(","))
        region = sheet.crop((x, y, x + w, y + h))
        a = np.array(region).astype(np.float32)
        rgb, alpha = a[..., :3], a[..., 3:4]
        lum = rgb.mean(axis=2, keepdims=True)
        cool = np.concatenate([
            np.clip(lum * 0.98 + 10, 0, 255),
            np.clip(lum * 0.96 + 8, 0, 255),
            np.clip(lum * 0.93 + 6, 0, 255),
            alpha,
        ], axis=2).astype(np.uint8)
        sheet.paste(Image.fromarray(cool, "RGBA"), (x, y))
        print(f"[recolor] {name}")

    buf = io.BytesIO()
    sheet.save(buf, "WEBP", lossless=True, quality=100)
    robust_write(WEBP, buf.getvalue())
    buf = io.BytesIO()
    sheet.save(buf, "PNG", optimize=True)
    robust_write(PNG, buf.getvalue())
    print(f"wrote {WEBP} and {PNG}")


if __name__ == "__main__":
    main()
