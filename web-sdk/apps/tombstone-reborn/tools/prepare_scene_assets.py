"""Prepare scene stills for the game (backgrounds + host cutouts).

Host character path is now:
  gen_lady_character.py  → assets-raw/lady_masters/
  alpha_crop_lady.py     → scene/lady_character.png + lady_bonus.png + lady_parts/
  gen_lady_spine.py      → spines/lady/

This script still copies optional BG sources and, if present, runs the host
alpha crop so legacy callers keep working. Hardcoded Victorian asset paths
are retired.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

APP = Path(__file__).resolve().parents[1]
OUT_DIR = APP / "static" / "assets" / "sprites" / "scene"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Optional BG masters (repo-local). Skip quietly if missing.
BG_CANDIDATES = [
    APP / "assets-raw" / "scene" / "scene_bg.png",
    APP / "static" / "assets" / "sprites" / "scene" / "scene_bg.png",
]


def prep_background() -> None:
    src = next((p for p in BG_CANDIDATES if p.is_file()), None)
    if src is None:
        print("[bg] skip — no scene_bg master found")
        return
    im = Image.open(src).convert("RGB")
    print(f"[bg] source size = {im.size}  ratio = {im.size[0] / im.size[1]:.3f}")
    im.save(OUT_DIR / "scene_bg.png", optimize=True)
    im.save(OUT_DIR / "scene_bg.webp", quality=90, method=6)
    print(f"[bg] wrote scene_bg.png + scene_bg.webp -> {OUT_DIR}")


def prep_character() -> None:
    """Delegate to alpha_crop_lady (magenta/black key + hole fill + parts)."""
    script = Path(__file__).resolve().parent / "alpha_crop_lady.py"
    print("[char] running alpha_crop_lady.py", flush=True)
    r = subprocess.run([sys.executable, str(script)], cwd=str(APP))
    if r.returncode != 0:
        raise SystemExit(f"alpha_crop_lady failed with code {r.returncode}")


if __name__ == "__main__":
    prep_background()
    prep_character()
    print("done.")
