"""Rebuild catalog.json + catalog.js from every pack manifest."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import is_pack_dir, resolve_dest  # noqa: E402
from speed_curve import catalog_timing  # noqa: E402


def normalize_loop(data: dict, count: int) -> tuple[int, int] | None:
    ls = data.get("loop_start", data.get("loopStart"))
    le = data.get("loop_end", data.get("loopEnd"))
    if ls is None or le is None:
        return None
    try:
        ls_i = int(ls)
        le_i = int(le)
    except (TypeError, ValueError):
        return None
    if count <= 0 or ls_i < 0 or le_i < ls_i or le_i >= count:
        return None
    return ls_i, le_i


def pack_entry(dest: Path, slug: str) -> dict | None:
    man_path = dest / slug / "parts" / "manifest.json"
    if not man_path.is_file():
        return None
    man = json.loads(man_path.read_text(encoding="utf-8"))
    size = man.get("source_size") or {}
    frames = [p["filename"] for p in man.get("parts", [])]
    entry = {
        "id": man.get("id", slug),
        "title": man.get("title", slug),
        "sheet": f"{slug}/{slug}-sheet.png",
        "partsDir": f"{slug}/parts",
        "spine": f"{slug}/spine/skeleton.json",
        "fps": man.get("fps", 16),
        "blend": man.get("blend", "add"),
        "pivot": man.get("pivot", "center"),
        "kind": man.get("kind", "sequence"),
        "frameCount": len(frames),
        "peakFrame": man.get("peak_frame", frames[0] if frames else ""),
        "frames": frames,
        "sheetSize": {"w": size.get("w", 0), "h": size.get("h", 0)},
    }
    loop = normalize_loop(man, len(frames))
    if loop:
        entry["loopStart"] = loop[0]
        entry["loopEnd"] = loop[1]
    entry.update(catalog_timing(man, len(frames), loop))
    return entry


def preferred_order(dest: Path) -> list[str]:
    packer = dest / "pack_vfx.py"
    slugs: list[str] = []
    if packer.is_file():
        sys.path.insert(0, str(dest))
        try:
            import pack_vfx  # noqa: WPS433

            slugs = [p["slug"] for p in getattr(pack_vfx, "PACKS", [])]
        except Exception:
            slugs = []
    on_disk = [p.name for p in sorted(dest.iterdir()) if is_pack_dir(p)]
    ordered = [s for s in slugs if s in on_disk]
    ordered.extend(s for s in on_disk if s not in ordered)
    return ordered


def rebuild(dest: Path) -> list[dict]:
    entries = []
    for slug in preferred_order(dest):
        entry = pack_entry(dest, slug)
        if entry:
            entries.append(entry)
    catalog = {"packs": entries}
    (dest / "catalog.json").write_text(
        json.dumps(catalog, indent=2), encoding="utf-8"
    )
    (dest / "catalog.js").write_text(
        "window.VFX_CATALOG = " + json.dumps(catalog, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"catalog: {len(entries)} packs")
    return entries


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", type=Path, default=None)
    args = p.parse_args()
    rebuild(resolve_dest(args.dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
