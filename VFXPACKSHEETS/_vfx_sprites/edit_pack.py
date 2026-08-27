"""Delete frames, remove a pack, or set an intro+hold loop range."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pack_frames import write_spine  # noqa: E402
from paths import is_pack_dir, resolve_dest  # noqa: E402
from rebuild_catalog import normalize_loop, pack_entry, rebuild  # noqa: E402
from speed_curve import (  # noqa: E402
    NAMED_CURVES,
    NAMED_PHASES,
    hazard_hood_phases,
    normalize_phase_name,
    normalize_scale,
    remap_indexed_list,
)

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}$")
FRAME_RE = re.compile(r"^frame_\d{2,3}\.png$")


def resolve_pack(dest: Path, slug: str) -> Path:
    if not SLUG_RE.match(slug or ""):
        raise ValueError("Invalid pack id")
    pack_dir = (dest / slug).resolve()
    dest_r = dest.resolve()
    if pack_dir.parent != dest_r or not is_pack_dir(pack_dir):
        raise ValueError("Unknown pack")
    return pack_dir


def load_manifest(pack_dir: Path) -> dict:
    path = pack_dir / "parts" / "manifest.json"
    man = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(man, dict) or not isinstance(man.get("parts"), list):
        raise ValueError("Pack manifest is damaged")
    return man


def write_manifest(pack_dir: Path, man: dict, records: list[dict], loop: tuple[int, int] | None) -> None:
    peak = max(records, key=lambda r: r.get("area", 0))["filename"] if records else ""
    man["parts"] = records
    man["saved_count"] = len(records)
    man["peak_frame"] = peak
    if loop:
        man["loop_start"] = loop[0]
        man["loop_end"] = loop[1]
    else:
        man.pop("loop_start", None)
        man.pop("loop_end", None)
    (pack_dir / "parts" / "manifest.json").write_text(
        json.dumps(man, indent=2), encoding="utf-8"
    )


def rewrite_spine(pack_dir: Path, man: dict, records: list[dict], loop: tuple[int, int] | None) -> None:
    size = man.get("source_size") or {}
    pack = {
        "slug": man.get("id", pack_dir.name),
        "fps": man.get("fps", 16),
        "blend": man.get("blend", "add"),
        "pivot": man.get("pivot", "center"),
        "speed_curve": man.get("speed_curve", man.get("speedCurve", "linear")),
    }
    if loop:
        pack["loop_start"] = loop[0]
        pack["loop_end"] = loop[1]
    if man.get("frame_phases") or man.get("framePhases"):
        pack["frame_phases"] = man.get("frame_phases", man.get("framePhases"))
    if man.get("frame_scales") is not None or man.get("frameScales") is not None:
        pack["frame_scales"] = man.get("frame_scales", man.get("frameScales"))
    write_spine(pack, pack_dir, records, int(size.get("w") or 0), int(size.get("h") or 0))


def remap_loop(old_loop: tuple[int, int] | None, kept_old: list[int]) -> tuple[int, int] | None:
    if not old_loop or not kept_old:
        return None
    old_to_new = {old: new for new, old in enumerate(kept_old)}
    ls, le = old_loop
    after_start = [old_to_new[i] for i in kept_old if i >= ls]
    before_end = [old_to_new[i] for i in kept_old if i <= le]
    if not after_start or not before_end:
        return None
    new_ls = min(after_start)
    new_le = max(before_end)
    if new_ls > new_le:
        return None
    return new_ls, new_le


def delete_frames(dest: Path, slug: str, names: list[str]) -> dict:
    pack_dir = resolve_pack(dest, slug)
    parts_dir = pack_dir / "parts"
    man = load_manifest(pack_dir)
    records = list(man["parts"])
    drop = {n for n in names if FRAME_RE.match(n or "")}
    if not drop:
        raise ValueError("No frames to delete")
    kept_old: list[int] = []
    kept: list[dict] = []
    for i, rec in enumerate(records):
        fname = rec.get("filename", "")
        if fname in drop:
            continue
        kept_old.append(i)
        kept.append(dict(rec))
    if not kept:
        raise ValueError("A pack needs at least one frame")
    if len(kept) == len(records):
        raise ValueError("Those frames are not in this pack")
    old_loop = normalize_loop(man, len(records))
    tmp = pack_dir / "_parts_new"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    written: list[dict] = []
    for i, rec in enumerate(kept, start=1):
        src_name = rec["filename"]
        new_name = f"frame_{i:02d}.png"
        src = parts_dir / src_name
        if not src.is_file():
            shutil.rmtree(tmp, ignore_errors=True)
            raise ValueError(f"Missing {src_name}")
        shutil.copy2(src, tmp / new_name)
        rec["index"] = i
        rec["filename"] = new_name
        written.append(rec)
    for old_png in parts_dir.glob("frame_*.png"):
        old_png.unlink()
    for new_png in tmp.glob("frame_*.png"):
        new_png.replace(parts_dir / new_png.name)
    tmp.rmdir()
    loop = remap_loop(old_loop, kept_old)
    phases = remap_indexed_list(man.get("frame_phases"), kept_old)
    if phases is None:
        man.pop("frame_phases", None)
    else:
        man["frame_phases"] = phases
    scales = remap_indexed_list(man.get("frame_scales") if isinstance(man.get("frame_scales"), list) else None, kept_old)
    if scales is None:
        man.pop("frame_scales", None)
    else:
        man["frame_scales"] = scales
    write_manifest(pack_dir, man, written, loop)
    rewrite_spine(pack_dir, man, written, loop)
    rebuild(dest)
    entry = pack_entry(dest, slug)
    if not entry:
        raise ValueError("Pack catalog rebuild failed")
    return entry


def delete_pack(dest: Path, slug: str) -> dict:
    pack_dir = resolve_pack(dest, slug)
    shutil.rmtree(pack_dir)
    packs = rebuild(dest)
    return {"id": slug, "removed": True, "packCount": len(packs)}


def set_loop(dest: Path, slug: str, start: int | None, end: int | None) -> dict:
    pack_dir = resolve_pack(dest, slug)
    man = load_manifest(pack_dir)
    records = list(man["parts"])
    if start is None or end is None:
        loop = None
    else:
        loop = normalize_loop({"loop_start": start, "loop_end": end}, len(records))
        if loop is None:
            raise ValueError("Loop range is outside this pack")
    write_manifest(pack_dir, man, records, loop)
    rewrite_spine(pack_dir, man, records, loop)
    rebuild(dest)
    entry = pack_entry(dest, slug)
    if not entry:
        raise ValueError("Pack catalog rebuild failed")
    return entry


def parse_phase_list(raw: str | list | None, count: int) -> list[str] | None:
    if raw is None:
        return None
    items = raw.split(",") if isinstance(raw, str) else list(raw)
    items = [normalize_phase_name(item.strip() if isinstance(item, str) else item) for item in items]
    if len(items) != count:
        raise ValueError("frame_phases must match the frame count")
    if any(item not in NAMED_PHASES for item in items):
        raise ValueError("Unknown frame phase")
    return items


def parse_scale_list(raw: str | list | None, count: int) -> list[float] | None:
    if raw is None:
        return None
    items = raw.split(",") if isinstance(raw, str) else list(raw)
    scales = [normalize_scale(item.strip() if isinstance(item, str) else item) for item in items]
    if len(scales) != count or any(scale is None for scale in scales):
        raise ValueError("frame_scales must be positive numbers, one per frame")
    return [float(scale) for scale in scales]


def set_curve(
    dest: Path,
    slug: str,
    curve: str,
    phases: list[str] | None = None,
    scales: list[float] | None = None,
    do_rebuild: bool = True,
) -> dict:
    pack_dir = resolve_pack(dest, slug)
    man = load_manifest(pack_dir)
    records = list(man["parts"])
    count = len(records)
    raw_name = str(curve or "").strip()
    if raw_name not in NAMED_CURVES:
        raise ValueError("Unknown speed curve")
    man["speed_curve"] = raw_name
    if phases is None:
        if raw_name != "attack":
            man.pop("frame_phases", None)
        elif not man.get("frame_phases"):
            hood = hazard_hood_phases(slug, count)
            if hood:
                man["frame_phases"] = hood
    else:
        man["frame_phases"] = parse_phase_list(phases, count)
    if scales is None:
        man.pop("frame_scales", None)
    else:
        man["frame_scales"] = parse_scale_list(scales, count)
    loop = normalize_loop(man, count)
    write_manifest(pack_dir, man, records, loop)
    rewrite_spine(pack_dir, man, records, loop)
    if do_rebuild:
        rebuild(dest)
    entry = pack_entry(dest, slug)
    if not entry:
        raise ValueError("Pack catalog rebuild failed")
    return entry


def apply_hazard_hood_curve(dest: Path, slug: str, do_rebuild: bool = False) -> dict:
    pack_dir = resolve_pack(dest, slug)
    man = load_manifest(pack_dir)
    count = len(man["parts"])
    phases = hazard_hood_phases(slug, count)
    if phases is None:
        raise ValueError(f"No Hazard Hood curve for {slug} with {count} frames")
    return set_curve(dest, slug, "attack", phases, None, do_rebuild=do_rebuild)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", type=Path, default=None)
    p.add_argument("--slug", required=True)
    p.add_argument("--delete", nargs="*", default=[])
    p.add_argument("--loop-start", type=int, default=None)
    p.add_argument("--loop-end", type=int, default=None)
    p.add_argument("--clear-loop", action="store_true")
    p.add_argument("--remove-pack", action="store_true")
    p.add_argument("--speed-curve", default=None)
    p.add_argument("--frame-phases", default=None)
    p.add_argument("--frame-scales", default=None)
    p.add_argument("--hazard-hood-curve", action="store_true")
    p.add_argument("--no-rebuild", action="store_true")
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    if args.remove_pack:
        entry = delete_pack(dest, args.slug)
        print(json.dumps(entry, indent=2))
        return 0
    if args.delete:
        entry = delete_frames(dest, args.slug, args.delete)
    elif args.clear_loop:
        entry = set_loop(dest, args.slug, None, None)
    elif args.loop_start is not None and args.loop_end is not None:
        entry = set_loop(dest, args.slug, args.loop_start, args.loop_end)
    elif args.hazard_hood_curve:
        entry = apply_hazard_hood_curve(dest, args.slug, do_rebuild=not args.no_rebuild)
    elif args.speed_curve:
        phases = args.frame_phases.split(",") if args.frame_phases else None
        scales = args.frame_scales.split(",") if args.frame_scales else None
        entry = set_curve(
            dest,
            args.slug,
            args.speed_curve,
            phases,
            scales,
            do_rebuild=not args.no_rebuild,
        )
    else:
        raise SystemExit("pass --delete, --loop-start/--loop-end, or --speed-curve")
    print(json.dumps({"id": entry["id"], "frameCount": entry["frameCount"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
