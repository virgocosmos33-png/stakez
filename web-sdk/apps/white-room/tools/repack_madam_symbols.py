"""Repack the symbolsStatic atlas from tools/symbol_art/ masters.

Reads GAME_CONFIG (threaded by game-builder regenerate_assets) so rethemes
resolve card_<id>_<slug>.png from the active symbol names. Falls back to
newest card_<id>_*.png on disk, then legacy Madam Mirror filenames.

Frame NAMES are unchanged (h1.webp … l5.webp, w/s/hm/me), so no frontend
code needs to change — only the pixels behind each frame.

Also preserves non-blur atlas frames that have no new master (burn sheets,
hm_cracked, explodedW, etc.) so a reskin does not wipe mechanic FX frames.

Run:  python tools/repack_madam_symbols.py
"""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "symbolsStatic"))
SRC_DIR = Path(HERE) / "symbol_art"
BACKUP_DIR = os.path.join(ATLAS_DIR, "backup_pre_reskin")

CELL = 300
PADDING = 2
COLUMNS = 4

# Legacy Madam Mirror card filenames (used when GAME_CONFIG unset / no new card).
_LEGACY_ICONS = {
    "h1": "card_h1_lady_mirror.png",
    "h2": "card_h2_wife.png",
    "h3": "card_h3_man.png",
    "h4": "card_h4_young_woman.png",
    "h5": "card_h5_dog.png",
    "l1": "card_l1_syringe.png",
    "l2": "card_l2_stethoscope.png",
    "l3": "card_l3_restraint_buckle.png",
    "l4": "card_l4_clipboard_404.png",
    "l5": "card_l5_pill_bottle.png",
}

# Mechanic / FX frames never generated as primary card_* masters — carry over
# from the previous atlas UNLESS a dedicated White Room master exists
# (card_hm_cracked.png). explodedW stays atlas-preserved.
ALWAYS_KEEP = ["hm_cracked.png", "explodedW.png"]
OPTIONAL_CARD_OVERRIDES = {
    "hm_cracked.png": "card_hm_cracked.png",
}


def _slug(name: str) -> str:
    s_ = re.sub(r"[^a-z0-9]+", "_", (name or "symbol").lower()).strip("_")
    return s_ or "symbol"


def frame_for_sid(sid: str) -> str:
    sid = sid.lower()
    if sid in {"h1", "h2", "h3", "h4", "h5", "l1", "l2", "l3", "l4", "l5"}:
        return f"{sid}.webp"
    if sid == "hm":
        return "hm_intact.png"
    return f"{sid}.png"


def _expected_from_config() -> dict[str, str]:
    """sid -> expected card filename from GAME_CONFIG (may not exist yet)."""
    path = (os.environ.get("GAME_CONFIG") or "").strip()
    if not path or not Path(path).is_file():
        return {}
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for sym in cfg.get("symbols") or []:
        sid = str(sym.get("id") or "").lower()
        if not sid:
            continue
        name = sym.get("name") or sid.upper()
        out[sid] = f"card_{sid}_{_slug(name)}.png"
    return out


def resolve_card(sid: str, expected: dict[str, str]) -> Path | None:
    """Pick the best card_<sid>_*.png for this id."""
    if expected.get(sid):
        p = SRC_DIR / expected[sid]
        if p.is_file():
            return p
    matches = sorted(SRC_DIR.glob(f"card_{sid}_*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    if matches:
        return matches[0]
    legacy = _LEGACY_ICONS.get(sid)
    if legacy:
        p = SRC_DIR / legacy
        if p.is_file():
            return p
    return None


def extract_frame(atlas_img: Image.Image, frame: dict) -> Image.Image:
    """Pull a frame out of the current atlas onto a CELLxCELL canvas."""
    f = frame["frame"]
    if frame.get("rotated"):
        region = atlas_img.crop((f["x"], f["y"], f["x"] + f["h"], f["y"] + f["w"]))
        region = region.transpose(Image.ROTATE_90)
    else:
        region = atlas_img.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
    src = frame.get("spriteSourceSize", {"x": 0, "y": 0})
    w = frame.get("sourceSize", {}).get("w", CELL)
    h = frame.get("sourceSize", {}).get("h", CELL)
    cell = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cell.paste(region, (src.get("x", 0), src.get("y", 0)))
    if (w, h) != (CELL, CELL):
        # Non-square legacy frames (should be rare for static masters) — fit to cell.
        cell = cell.resize((CELL, CELL), Image.LANCZOS)
    return cell


if __name__ == "__main__":
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for name in ("symbolsStatic.json", "symbolsStatic.webp", "symbolsStatic.png"):
        src = os.path.join(ATLAS_DIR, name)
        dst = os.path.join(BACKUP_DIR, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"backed up {name}")

    with open(os.path.join(ATLAS_DIR, "symbolsStatic.json"), encoding="utf-8") as f:
        current_json = json.load(f)
    current_img = Image.open(os.path.join(ATLAS_DIR, "symbolsStatic.webp")).convert("RGBA")

    # Start from every non-blur static frame so burn / specials survive until replaced.
    cells: dict[str, Image.Image] = {}
    for frame_name, frame in current_json["frames"].items():
        if "_blur." in frame_name:
            continue
        cells[frame_name] = extract_frame(current_img, frame)

    expected = _expected_from_config()
    sids = list(expected.keys()) if expected else list(_LEGACY_ICONS.keys())
    # Always attempt specials too when present on disk (even without GAME_CONFIG).
    for sid in ("w", "s", "hm", "me"):
        if sid not in sids:
            sids.append(sid)

    for sid in sids:
        card = resolve_card(sid, expected)
        if card is None:
            print(f"  (no new card for {sid})")
            continue
        frame_name = frame_for_sid(sid)
        im = Image.open(card).convert("RGBA").resize((CELL, CELL), Image.LANCZOS)
        cells[frame_name] = im
        print(f"packed new  {card.name} -> {frame_name}")

    for frame_name in ALWAYS_KEEP:
        override = OPTIONAL_CARD_OVERRIDES.get(frame_name)
        if override:
            p = SRC_DIR / override
            if p.is_file():
                cells[frame_name] = Image.open(p).convert("RGBA").resize((CELL, CELL), Image.LANCZOS)
                print(f"packed new  {p.name} -> {frame_name}")
                continue
        if frame_name not in current_json["frames"]:
            print(f"  (skip {frame_name}: not in current atlas)")
            continue
        if frame_name not in cells:
            cells[frame_name] = extract_frame(current_img, current_json["frames"][frame_name])
            print(f"kept        {frame_name}")

    names = sorted(cells.keys())
    rows = (len(names) + COLUMNS - 1) // COLUMNS
    sheet_w = COLUMNS * (CELL + PADDING) + PADDING
    sheet_h = rows * (CELL + PADDING) + PADDING
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

    frames = {}
    for i, name in enumerate(names):
        col, row = i % COLUMNS, i // COLUMNS
        x = PADDING + col * (CELL + PADDING)
        y = PADDING + row * (CELL + PADDING)
        cell = cells[name]
        if cell.size != (CELL, CELL):
            cell = cell.resize((CELL, CELL), Image.LANCZOS)
        sheet.paste(cell, (x, y))
        frames[name] = {
            "frame": {"x": x, "y": y, "w": CELL, "h": CELL},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": CELL, "h": CELL},
            "sourceSize": {"w": CELL, "h": CELL},
            "pivot": {"x": 0.5, "y": 0.5},
        }

    atlas = {
        "frames": frames,
        "meta": {
            "app": "repack_madam_symbols.py",
            "version": "1.0",
            "image": "symbolsStatic.webp",
            "format": "RGBA8888",
            "size": {"w": sheet_w, "h": sheet_h},
            "scale": "1",
        },
    }

    # Atomic writes — OneDrive often locks the live atlas files mid-save (Errno 22).
    def _atomic_save(img: Image.Image, dest: str, **save_kw) -> None:
        root, ext = os.path.splitext(dest)
        tmp = f"{root}.__new__{ext}"
        img.save(tmp, **save_kw)
        os.replace(tmp, dest)

    _atomic_save(sheet, os.path.join(ATLAS_DIR, "symbolsStatic.png"))
    _atomic_save(sheet, os.path.join(ATLAS_DIR, "symbolsStatic.webp"), lossless=True)
    json_path = os.path.join(ATLAS_DIR, "symbolsStatic.json")
    tmp_json = json_path + ".tmp"
    with open(tmp_json, "w", encoding="utf-8") as f:
        json.dump(atlas, f, indent=1)
    os.replace(tmp_json, json_path)

    print(f"\nwrote {sheet_w}x{sheet_h} atlas with {len(frames)} frames -> {ATLAS_DIR}")

    # Bake spin-blur frames after every pack so symbols scope always yields
    # *_blur masters (also covers MCP hosts that have not reloaded pipeline.mjs).
    import subprocess
    import sys

    smear = os.path.join(HERE, "make_spin_smears.py")
    print(f"\n-> chaining {smear}")
    r = subprocess.run([sys.executable, smear], cwd=os.path.dirname(HERE))
    if r.returncode != 0:
        raise SystemExit(f"make_spin_smears.py failed with code {r.returncode}")
