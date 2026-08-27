"""Resolve the VFX library folder in any project."""
from __future__ import annotations

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SKILL_DIR.parent
HOME_LIBRARY = Path(r"C:\Users\Emex33\Documents\fire frame vfx\VFXPACKSHEETS")
LIBRARY_NAMES = ("VFXPACKSHEETS", "VFXSHEETS")
RAW_SHEETS_DIRNAME = "raw spritesheets"
SKIP_LIBRARY_DIRS = {RAW_SHEETS_DIRNAME, "_review", "_vfx_sprites"}


def is_pack_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and not path.name.startswith("_")
        and path.name not in SKIP_LIBRARY_DIRS
        and (path / "parts" / "manifest.json").is_file()
    )


def raw_sheets_dir(dest: Path) -> Path:
    return dest / RAW_SHEETS_DIRNAME


def resolve_dest(explicit: Path | None = None, cwd: Path | None = None) -> Path:
    if explicit is not None:
        return Path(explicit).resolve()
    here = Path(cwd or Path.cwd()).resolve()
    if here.name in LIBRARY_NAMES:
        return here
    for name in LIBRARY_NAMES:
        candidate = here / name
        if candidate.is_dir():
            return candidate
    parent = here / LIBRARY_NAMES[0]
    if HOME_LIBRARY.is_dir() and (
        HOME_LIBRARY == here or HOME_LIBRARY.parent == here
    ):
        return HOME_LIBRARY
    return parent
