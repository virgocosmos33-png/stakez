"""Copy bundled VFX scripts + viewer into a project library if missing."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from paths import SKILL_DIR, SKILL_ROOT, resolve_dest

RUNTIME = (
    "island_split.py",
    "pack_frames.py",
    "ingest_sheet.py",
    "contact_sheet.py",
    "apply_audit.py",
    "rebuild_catalog.py",
    "verify_library.py",
    "stage_band.py",
    "edit_pack.py",
    "serve_preview.py",
    "speed_curve.py",
    "local_upscale.py",
    "clean_separators.py",
    "paths.py",
    "bootstrap.py",
)


def bootstrap(dest: Path) -> Path:
    dest = dest.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    tools = dest / "_vfx_sprites"
    tools.mkdir(exist_ok=True)
    copied = []
    for name in RUNTIME:
        src = SKILL_DIR / name
        if not src.is_file():
            continue
        target = tools / name
        shutil.copy2(src, target)
        copied.append(name)
    viewer_src = SKILL_ROOT / "templates" / "viewer.html"
    viewer_dest = dest / "viewer.html"
    if viewer_src.is_file():
        shutil.copy2(viewer_src, viewer_dest)
        copied.append("viewer.html")
    req_src = SKILL_ROOT / "requirements.txt"
    if req_src.is_file():
        shutil.copy2(req_src, dest / "requirements.txt")
    print(f"spawned {len(copied)} files into {tools}")
    print(f"library: {dest}")
    return tools


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", type=Path, default=None)
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    bootstrap(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
