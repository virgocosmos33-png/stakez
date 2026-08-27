"""Strip separator-grid remnants from existing pack parts.

Uses island_split.clean_separator_frame (same law as a fresh split).
Does not re-ingest, does not touch raw spritesheets.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from edit_pack import (  # noqa: E402
    FRAME_RE,
    load_manifest,
    remap_loop,
    rewrite_spine,
    write_manifest,
)
from island_split import clean_separator_frame  # noqa: E402
from paths import is_pack_dir, resolve_dest  # noqa: E402
from rebuild_catalog import normalize_loop, rebuild  # noqa: E402
from speed_curve import remap_indexed_list  # noqa: E402

def list_pack_slugs(dest: Path) -> list[str]:
    return sorted(p.name for p in dest.iterdir() if is_pack_dir(p))


def inspect_frame(path: Path) -> dict:
    rgba = np.asarray(Image.open(path).convert("RGBA"))
    cleaned, n_erased = clean_separator_frame(rgba, mode="frame")
    dropped = cleaned is None
    return {
        "name": path.name,
        "src": f"{rgba.shape[1]}x{rgba.shape[0]}",
        "erased": n_erased,
        "dropped": dropped,
        "out": None if dropped else f"{cleaned.shape[1]}x{cleaned.shape[0]}",
    }


def scan_pack(dest: Path, slug: str) -> dict:
    parts = dest / slug / "parts"
    frames = sorted(p for p in parts.glob("frame_*.png") if FRAME_RE.match(p.name))
    rows = [inspect_frame(p) for p in frames]
    dirty = [r for r in rows if r["erased"] or r["dropped"]]
    return {
        "slug": slug,
        "frames": len(frames),
        "dirty": len(dirty),
        "erased_px": sum(r["erased"] for r in rows),
        "dropped": [r["name"] for r in rows if r["dropped"]],
        "rows": rows,
    }


def _restore_backup(dest: Path, slug: str, man: dict) -> bool:
    backup = dest / "_upscale_backup" / slug
    parts = dest / slug / "parts"
    if not backup.is_dir():
        return False
    bframes = sorted(p for p in backup.glob("frame_*.png") if FRAME_RE.match(p.name))
    if not bframes:
        return False
    for src in bframes:
        shutil.copy2(src, parts / src.name)
    scale = 0
    up = man.get("upscale") or {}
    try:
        scale = int(up.get("scale") or 0)
    except (TypeError, ValueError):
        scale = 0
    src = man.get("source_size") or {}
    if scale >= 2 and src.get("w") and src.get("h"):
        man["source_size"] = {
            "w": int(src["w"]) // scale,
            "h": int(src["h"]) // scale,
        }
    man.pop("upscale", None)
    return True


def _write_cleaned_backup(dest: Path, slug: str, parts: Path) -> None:
    backup = dest / "_upscale_backup" / slug
    backup.mkdir(parents=True, exist_ok=True)
    for src in parts.glob("frame_*.png"):
        if FRAME_RE.match(src.name):
            shutil.copy2(src, backup / src.name)


def clean_pack(dest: Path, slug: str, from_backup: bool) -> dict:
    pack_dir = dest / slug
    if not is_pack_dir(pack_dir):
        raise ValueError(f"Unknown pack: {slug}")
    parts = pack_dir / "parts"
    man = load_manifest(pack_dir)
    restored = False
    if from_backup:
        restored = _restore_backup(dest, slug, man)
    records = list(man["parts"])
    old_loop = normalize_loop(man, len(records))
    kept_old: list[int] = []
    written: list[dict] = []
    changed: list[str] = []
    dropped: list[str] = []
    erased_px = 0
    tmp = pack_dir / "_parts_clean"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    for old_i, rec in enumerate(records):
        fname = rec.get("filename", "")
        src = parts / fname
        if not src.is_file():
            shutil.rmtree(tmp, ignore_errors=True)
            raise FileNotFoundError(f"Missing {slug}/{fname}")
        rgba = np.asarray(Image.open(src).convert("RGBA"))
        cleaned, n_erased = clean_separator_frame(rgba, mode="frame")
        erased_px += n_erased
        if cleaned is None:
            dropped.append(fname)
            continue
        if n_erased or cleaned.shape != rgba.shape:
            changed.append(fname)
        new_i = len(written) + 1
        new_name = f"frame_{new_i:02d}.png"
        Image.fromarray(cleaned, "RGBA").save(tmp / new_name)
        rec = dict(rec)
        rec["index"] = new_i
        rec["filename"] = new_name
        rec["width"] = int(cleaned.shape[1])
        rec["height"] = int(cleaned.shape[0])
        rec["area"] = int((cleaned[:, :, 3] > 0).sum())
        written.append(rec)
        kept_old.append(old_i)
    if not written:
        shutil.rmtree(tmp, ignore_errors=True)
        raise ValueError(f"{slug}: every frame was separator-only")
    for old_png in parts.glob("frame_*.png"):
        old_png.unlink()
    for new_png in tmp.glob("frame_*.png"):
        new_png.replace(parts / new_png.name)
    tmp.rmdir()
    loop = remap_loop(old_loop, kept_old)
    phases = remap_indexed_list(man.get("frame_phases"), kept_old)
    if phases is None:
        man.pop("frame_phases", None)
    else:
        man["frame_phases"] = phases
    raw_scales = man.get("frame_scales")
    scales = remap_indexed_list(raw_scales if isinstance(raw_scales, list) else None, kept_old)
    if scales is None:
        man.pop("frame_scales", None)
    else:
        man["frame_scales"] = scales
    man["separator_clean"] = {
        "erased_px": erased_px,
        "dropped": dropped,
        "from_backup": restored,
    }
    write_manifest(pack_dir, man, written, loop)
    rewrite_spine(pack_dir, man, written, loop)
    if restored and erased_px and not dropped:
        # Keep a clean 1x only after this pass actually stripped pixels.
        _write_cleaned_backup(dest, slug, parts)
    return {
        "slug": slug,
        "restored": restored,
        "changed": changed,
        "dropped": dropped,
        "erased_px": erased_px,
        "frames": len(written),
        "needs_upscale": restored and bool(changed or dropped or erased_px),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Strip separator grid remnants from pack parts")
    p.add_argument("--dest", type=Path, default=None)
    p.add_argument("--slug", action="append", default=[])
    p.add_argument("--scan", action="store_true", help="Report only, do not write")
    p.add_argument("--from-backup", action="store_true", help="Restore 1x backup, then clean")
    p.add_argument("--no-catalog", action="store_true")
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    slugs = [s.strip() for s in args.slug if s.strip()]
    if not slugs:
        slugs = list_pack_slugs(dest)
    reports = []
    for slug in slugs:
        if args.scan:
            reports.append(scan_pack(dest, slug))
        else:
            reports.append(clean_pack(dest, slug, from_backup=args.from_backup))
    if args.scan:
        dirty = [r for r in reports if r["dirty"]]
        for r in reports:
            if not r["dirty"]:
                print(f"clean {r['slug']}  frames={r['frames']}")
                continue
            print(
                f"DIRTY {r['slug']}  dirty={r['dirty']}/{r['frames']}  "
                f"erased_px={r['erased_px']}  drop={r['dropped']}"
            )
            for row in r["rows"]:
                if row["erased"] or row["dropped"]:
                    print(
                        f"  {row['name']}  {row['src']}  erased={row['erased']}  "
                        f"drop={row['dropped']}  out={row['out']}"
                    )
        print(f"dirty_packs={len(dirty)}/{len(reports)}")
        return 0
    if not args.no_catalog:
        rebuild(dest)
    for r in reports:
        print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
