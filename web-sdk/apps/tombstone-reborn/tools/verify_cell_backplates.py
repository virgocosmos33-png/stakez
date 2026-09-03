"""Prove the H/L backplate contract is in the LIVE game files.

Fails if a paying card is still a bare face, if a skeleton is missing the
plate slot / land-win-static tracks, or if H1-L5 spines are not preloaded.

Run: python tools/verify_cell_backplates.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
APP = HERE.parent

ATLAS_JSON = APP / "assets" / "sprites" / "symbolsStatic" / "symbolsStatic.v13.json"
ATLAS_IMG = APP / "assets" / "sprites" / "symbolsStatic" / "symbolsStatic.v13.webp"
SPINE_ATLAS = APP / "assets" / "spines" / "mm_symbols" / "mm_symbols.atlas"
SPINE_IMG = APP / "assets" / "spines" / "mm_symbols" / "mm_symbols.png"
SPINE_DIR = APP / "assets" / "spines" / "mm_symbols"
CONSTANTS = APP / "src" / "game" / "constants.ts"
ASSETS_TS = APP / "src" / "game" / "assets.ts"
PAYTABLE = APP / "static" / "assets" / "paytable"
PREVIEW = APP / "assets-raw" / "cell_backplates" / "preview"

HIGHS = ("h1", "h2", "h3", "h4", "h5")
LOWS = ("l1", "l2", "l3", "l4", "l5")
PAYING = HIGHS + LOWS
ANIMS = ("", "_land", "_postwin", "_static")


def _region(sheet: Image.Image, x: int, y: int, w: int, h: int) -> Image.Image:
    return sheet.crop((x, y, x + w, y + h)).convert("RGBA")


def _atlas_frames() -> dict[str, dict]:
    data = json.loads(ATLAS_JSON.read_text(encoding="utf-8"))
    return data["frames"]


def _spine_bounds() -> dict[str, tuple[int, int, int, int]]:
    lines = SPINE_ATLAS.read_text(encoding="utf-8").splitlines()
    bounds: dict[str, tuple[int, int, int, int]] = {}
    name = None
    for line in lines:
        if line.strip().startswith("bounds:") and name:
            x, y, w, h = (int(v) for v in line.split(":")[1].split(","))
            bounds[name] = (x, y, w, h)
            name = None
        elif line and not line.startswith(" ") and ":" not in line and line not in {
            "mm_symbols.webp",
            "mm_symbols.png",
        }:
            name = line.strip()
    return bounds


def _brown_frac(im: Image.Image) -> float:
    import numpy as np

    a = np.asarray(im.convert("RGBA"))
    rgb, al = a[..., :3].astype(float), a[..., 3]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    brown = (al > 80) & (r > g + 6) & (r > b + 6) & (r > 18) & (r < 160)
    return float(brown.mean())


def _blood_frac(im: Image.Image) -> float:
    import numpy as np

    a = np.asarray(im.convert("RGBA"))
    rgb, al = a[..., :3].astype(float), a[..., 3]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    blood = (al > 80) & (r > g + 30) & (r > b + 20) & (r > 80)
    return float(blood.mean())


def _opaque_black_frac(im: Image.Image) -> float:
    import numpy as np

    a = np.asarray(im.convert("RGBA"))
    lum = a[..., :3].mean(axis=2)
    return float(((a[..., 3] > 240) & (lum < 8)).mean())


def main() -> int:
    problems: list[str] = []
    PREVIEW.mkdir(parents=True, exist_ok=True)

    for path in (ATLAS_JSON, ATLAS_IMG, SPINE_ATLAS, SPINE_IMG, CONSTANTS, ASSETS_TS):
        if not path.is_file():
            problems.append(f"missing {path}")
    if problems:
        print("FAIL")
        for p in problems:
            print(" ", p)
        return 1

    frames = _atlas_frames()
    static_sheet = Image.open(ATLAS_IMG).convert("RGBA")
    spine_sheet = Image.open(SPINE_IMG).convert("RGBA")
    spine_bounds = _spine_bounds()
    constants = CONSTANTS.read_text(encoding="utf-8")
    assets_ts = ASSETS_TS.read_text(encoding="utf-8")

    thumbs: list[Image.Image] = []
    print("=== LIVE v13 atlas (what spin / split / paytable sprites use) ===")
    for gid in PAYING:
        frame = f"{gid}.webp"
        meta = frames.get(frame)
        if not meta:
            problems.append(f"atlas missing frame {frame}")
            continue
        box = meta["frame"]
        tile = _region(static_sheet, box["x"], box["y"], box["w"], box["h"])
        brown, blood, black = _brown_frac(tile), _blood_frac(tile), _opaque_black_frac(tile)
        print(f"  {frame:10s} brown={brown:.3f} blood={blood:.3f} opaque-black={black:.3f}")
        thumbs.append(tile)
        tile.save(PREVIEW / f"live_{gid}.png")
        blur_name = f"{gid}_blur.webp"
        blur_meta = frames.get(blur_name)
        if not blur_meta:
            problems.append(f"atlas missing smear {blur_name}")

    print("=== Spine atlas (faces only, no backboard) ===")
    for gid in PAYING:
        if gid not in spine_bounds:
            problems.append(f"spine atlas missing face {gid}")
            continue
        face = _region(spine_sheet, *spine_bounds[gid])
        print(f"  {gid:3s} face-black={_opaque_black_frac(face):.3f}")
        face.save(PREVIEW / f"spine_{gid}.png")

    print("=== Skeletons ===")
    for gid in PAYING:
        path = SPINE_DIR / f"{gid}.json"
        if not path.is_file():
            problems.append(f"missing {path.name}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        plate_slot = f"{gid}_plate"
        for slot in data.get("slots") or []:
            if slot.get("name") == plate_slot and slot.get("attachment"):
                problems.append(f"{gid}.json still draws {slot.get('attachment')} on {plate_slot}")
        atts = ((data.get("skins") or [{}])[0].get("attachments") or {})
        if plate_slot in atts:
            problems.append(f"{gid}.json skin still has {plate_slot}")
        anims = data.get("animations") or {}
        for suffix in ANIMS:
            name = f"{gid}{suffix}" if suffix else gid
            if name not in anims:
                problems.append(f"{gid}.json missing animation {name}")
        post = anims.get(f"{gid}_postwin") or {}
        if (post.get("attachments") or {}).get("default"):
            problems.append(f"{gid}_postwin still has a mesh wave")
        scales = ((post.get("bones") or {}).get("card") or {}).get("scale") or []
        peak = max((float(k.get("x") or 1) for k in scales), default=1.0)
        if gid.startswith("h"):
            if peak < 1.10:
                problems.append(f"{gid}_postwin has no hold-grow scale (peak={peak})")
            win = anims.get(gid) or {}
            win_scales = ((win.get("bones") or {}).get("card") or {}).get("scale") or []
            win_peak = max((float(k.get("x") or 1) for k in win_scales), default=1.0)
            if win_peak < 1.15:
                problems.append(f"{gid} win has no grow scale (peak={win_peak})")
        elif peak < 1.04:
            problems.append(f"{gid}_postwin has no inhale scale (peak={peak})")

    print("=== Frontend wiring ===")
    for name in ("H1", "H2", "H3", "H4", "H5", "L1", "L2", "L3", "L4", "L5"):
        if not re.search(rf"^\t{name}:\s*platedStates\(", constants, re.M):
            problems.append(f"constants.ts {name} is not platedStates")
        block = re.search(rf"^\t{name}:\s*\{{(.*?)^\t\}},", assets_ts, re.S | re.M)
        if not block or "preload: true" not in block.group(1):
            problems.append(f"assets.ts {name} is not preloaded")
        if not block or "type: 'spine'" not in block.group(1):
            problems.append(f"assets.ts {name} is not a spine")

    print("=== Paytable HTML copies ===")
    for gid in PAYING:
        png = PAYTABLE / f"{gid}.png"
        if not png.is_file():
            problems.append(f"static paytable missing {gid}.png")
            continue
        if not Image.open(png).size[0]:
            problems.append(f"paytable {gid}.png is empty")

    if thumbs:
        sheet = Image.new("RGBA", (300 * 5, 300 * 2), (20, 16, 12, 255))
        for i, tile in enumerate(thumbs):
            sheet.alpha_composite(tile, ((i % 5) * 300, (i // 5) * 300))
        sheet.save(PREVIEW / "live_atlas_contact.png")

    if problems:
        print("FAIL")
        for p in problems:
            print(" ", p)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
