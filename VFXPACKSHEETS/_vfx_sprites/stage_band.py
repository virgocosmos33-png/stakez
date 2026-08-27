"""Crop a sheet band and island-split it (no leftover dilate).

Use when the packer glued a mixed bottom kit (snowflakes + wisps +
flares) into one strip. Raw 8-connected islands keep each icon separate.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from island_split import split_sheet  # noqa: E402
from paths import resolve_dest  # noqa: E402


def stage_band(
    dest: Path,
    sheet: Path,
    slug: str,
    title: str,
    y0: int,
    y1: int | None = None,
    x0: int = 0,
    x1: int | None = None,
    min_area: int = 200,
    alpha_threshold: int | None = None,
) -> Path:
    dest = dest.resolve()
    raw = Image.open(sheet).convert("RGBA")
    w, h = raw.size
    x1 = w if x1 is None else x1
    y1 = h if y1 is None else y1
    crop = raw.crop((x0, y0, x1, y1))
    dest_dir = dest / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    sheet_dest = dest_dir / f"{slug}-sheet.png"
    crop.save(sheet_dest)
    parts = dest_dir / "parts"
    if parts.exists():
        shutil.rmtree(parts)
    kwargs = {"min_area": min_area, "gutter_split": True}
    if alpha_threshold is not None:
        kwargs["alpha_threshold"] = alpha_threshold
    split_sheet(sheet_dest, parts, **kwargs)
    records = []
    for prop in sorted(parts.glob("prop_*.png")):
        idx = int(prop.stem.split("_")[1])
        name = f"frame_{idx:02d}.png"
        target = parts / name
        if target.exists():
            target.unlink()
        prop.rename(target)
        records.append(idx)
    man_path = parts / "manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    for rec in man.get("parts", []):
        rec["filename"] = f"frame_{int(rec['index']):02d}.png"
    man["id"] = slug
    man["title"] = title
    man["fps"] = 8
    man["blend"] = "add"
    man["pivot"] = "center"
    man["kind"] = "props"
    man["source_uuid"] = ""
    man_path.write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(f"{slug}: {len(records)} raw islands from band y={y0}:{y1}")
    return dest_dir


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", type=Path, default=None)
    p.add_argument("--sheet", type=Path, required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--title", default="STAGE band")
    p.add_argument("--y0", type=int, required=True)
    p.add_argument("--y1", type=int, default=None)
    p.add_argument("--x0", type=int, default=0)
    p.add_argument("--x1", type=int, default=None)
    p.add_argument("--min-area", type=int, default=200)
    p.add_argument("--alpha-threshold", type=int, default=None)
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    if not args.sheet.is_file():
        raise SystemExit(f"missing sheet: {args.sheet}")
    stage_band(
        dest,
        args.sheet,
        args.slug.strip(),
        args.title.strip(),
        args.y0,
        args.y1,
        args.x0,
        args.x1,
        args.min_area,
        args.alpha_threshold,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
