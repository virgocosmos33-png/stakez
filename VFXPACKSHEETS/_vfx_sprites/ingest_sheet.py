"""First-pass island split of one sheet into the VFX library."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from bootstrap import bootstrap  # noqa: E402
from pack_frames import pack_one  # noqa: E402
from paths import resolve_dest  # noqa: E402
from rebuild_catalog import rebuild  # noqa: E402


def ingest(
    dest: Path,
    sheet: Path,
    slug: str,
    title: str,
    fps: int,
    blend: str,
    pivot: str,
    kind: str = "sequence",
    speed_curve: str = "linear",
) -> dict:
    dest = dest.resolve()
    bootstrap(dest)
    dest_dir = dest / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    sheet_dest = dest_dir / f"{slug}-sheet.png"
    src = sheet.resolve()
    if src != sheet_dest.resolve():
        shutil.copy2(src, sheet_dest)
    pack = {
        "uuid": "",
        "slug": slug,
        "title": title,
        "fps": fps,
        "blend": blend,
        "pivot": pivot,
        "kind": kind,
        "sheet": str(sheet_dest),
        "speed_curve": speed_curve,
    }
    entry = pack_one(dest, pack)
    if not slug.startswith("_"):
        rebuild(dest)
    return entry


def main() -> int:
    p = argparse.ArgumentParser(description="Ingest one VFX sprite sheet")
    p.add_argument("--dest", type=Path, default=None)
    p.add_argument("--sheet", type=Path, required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--fps", type=int, default=16)
    p.add_argument("--blend", choices=("add", "normal"), default="add")
    p.add_argument("--pivot", choices=("center", "bottom"), default="center")
    p.add_argument("--kind", choices=("sequence", "props"), default="sequence")
    p.add_argument(
        "--speed-curve",
        choices=("linear", "easeIn", "easeOut", "easeInOut", "attack"),
        default="linear",
    )
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    if not args.sheet.is_file():
        raise SystemExit(f"missing sheet: {args.sheet}")
    entry = ingest(
        dest,
        args.sheet,
        args.slug.strip(),
        args.title.strip(),
        args.fps,
        args.blend,
        args.pivot,
        args.kind,
        args.speed_curve,
    )
    print(f"ingested {entry['id']}: {entry['frameCount']} first-pass frames")
    print("AUDIT REQUIRED. Do not ship this pack until apply_audit.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
