"""Apply a visual-audit ops list: keep / split / merge, then renumber."""
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

from island_split import (  # noqa: E402
    ALPHA_THRESHOLD,
    PAD_PX,
    crop_island,
    ensure_alpha,
    erase_separator_grid,
)
from pack_frames import write_spine  # noqa: E402
from paths import resolve_dest  # noqa: E402
from rebuild_catalog import rebuild  # noqa: E402


def load_deps(_dest: Path):
    return write_spine, ALPHA_THRESHOLD, PAD_PX, crop_island, ensure_alpha


def rec_from_crop(idx: int, name: str, image: Image.Image, meta: dict) -> dict:
    return {
        "index": idx,
        "filename": name,
        "bbox": meta["bbox"],
        "area": meta["area"],
        "width": image.size[0],
        "height": image.size[1],
    }


def gap_index(fill: np.ndarray, lo_frac: float = 0.18, hi_frac: float = 0.82) -> int:
    n = int(fill.size)
    lo = max(1, int(n * lo_frac))
    hi = min(n - 1, int(n * hi_frac))
    band = fill[lo:hi]
    if band.size == 0:
        return n // 2
    return lo + int(np.argmin(band))


def split_region(detect: np.ndarray, bbox: dict, axis: str, which: str) -> np.ndarray:
    x, y, w, h = int(bbox["x"]), int(bbox["y"]), int(bbox["w"]), int(bbox["h"])
    region = detect[y : y + h, x : x + w]
    mask = np.zeros_like(detect, dtype=bool)
    if axis == "v":
        cut = gap_index(region.sum(axis=1).astype(np.int32))
        if which == "top":
            mask[y : y + cut, x : x + w] = region[:cut]
        else:
            mask[y + cut : y + h, x : x + w] = region[cut:]
    else:
        cut = gap_index(region.sum(axis=0).astype(np.int32))
        if which == "left":
            mask[y : y + h, x : x + cut] = region[:, :cut]
        else:
            mask[y : y + h, x + cut : x + w] = region[:, cut:]
    return mask


def merge_mask(detect: np.ndarray, boxes: list[dict], pad: int = 10) -> np.ndarray:
    xs = [b["x"] for b in boxes]
    ys = [b["y"] for b in boxes]
    x1s = [b["x"] + b["w"] for b in boxes]
    y1s = [b["y"] + b["h"] for b in boxes]
    x0 = max(0, min(xs) - pad)
    y0 = max(0, min(ys) - pad)
    x1 = min(detect.shape[1], max(x1s) + pad)
    y1 = min(detect.shape[0], max(y1s) + pad)
    mask = np.zeros_like(detect, dtype=bool)
    mask[y0:y1, x0:x1] = detect[y0:y1, x0:x1]
    return mask


def pack_meta(slug: str, old: dict, extra: dict | None = None) -> dict:
    extra = extra or {}
    pack = {
        "uuid": extra.get("uuid", old.get("source_uuid", "")),
        "slug": slug,
        "title": extra.get("title", old.get("title", slug)),
        "fps": extra.get("fps", old.get("fps", 16)),
        "blend": extra.get("blend", old.get("blend", "add")),
        "pivot": extra.get("pivot", old.get("pivot", "center")),
        "kind": extra.get("kind", old.get("kind", "sequence")),
        "speed_curve": extra.get("speed_curve", old.get("speed_curve", "linear")),
    }
    if extra.get("frame_phases"):
        pack["frame_phases"] = extra["frame_phases"]
    if extra.get("frame_scales") is not None:
        pack["frame_scales"] = extra["frame_scales"]
    return pack


def apply_one(
    dest: Path,
    slug: str,
    ops: list,
    deps,
    source_slug: str | None = None,
    extra: dict | None = None,
) -> None:
    write_spine_fn, ALPHA_THRESHOLD, PAD_PX, crop_island, ensure_alpha = deps
    src_slug = source_slug or slug
    src_dir = dest / src_slug
    dest_dir = dest / slug
    src_parts = src_dir / "parts"
    old = json.loads((src_parts / "manifest.json").read_text(encoding="utf-8"))
    by_idx = {int(p["index"]): p for p in old["parts"]}
    src_sheet = src_dir / f"{src_slug}-sheet.png"
    dest_dir.mkdir(parents=True, exist_ok=True)
    sheet_path = dest_dir / f"{slug}-sheet.png"
    if src_sheet.is_file() and src_sheet.resolve() != sheet_path.resolve():
        shutil.copy2(src_sheet, sheet_path)
    parts = dest_dir / "parts"
    parts.mkdir(parents=True, exist_ok=True)
    raw = np.asarray(Image.open(sheet_path).convert("RGBA"))
    keyed, alpha_source = ensure_alpha(raw)
    keyed = erase_separator_grid(keyed, mode="auto")
    detect = keyed[:, :, 3] > ALPHA_THRESHOLD
    sheet_h, sheet_w = keyed.shape[:2]
    pack = pack_meta(slug, old, extra)

    tmp = dest_dir / "_parts_new"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    records = []
    for i, op in enumerate(ops, start=1):
        name = f"frame_{i:02d}.png"
        kind = op[0]
        if kind == "keep":
            src_idx = int(op[1])
            image = Image.open(src_parts / f"frame_{src_idx:02d}.png").convert("RGBA")
            image.save(tmp / name)
            rec = dict(by_idx[src_idx])
            rec["index"] = i
            rec["filename"] = name
            rec["width"] = image.size[0]
            rec["height"] = image.size[1]
        elif kind == "split_v":
            mask = split_region(detect, by_idx[int(op[1])]["bbox"], "v", op[2])
            image, meta = crop_island(keyed, mask, PAD_PX)
            image.save(tmp / name)
            rec = rec_from_crop(i, name, image, meta)
        elif kind == "split_h":
            mask = split_region(detect, by_idx[int(op[1])]["bbox"], "h", op[2])
            image, meta = crop_island(keyed, mask, PAD_PX)
            image.save(tmp / name)
            rec = rec_from_crop(i, name, image, meta)
        elif kind == "merge":
            boxes = [by_idx[int(n)]["bbox"] for n in op[1]]
            image, meta = crop_island(keyed, merge_mask(detect, boxes), PAD_PX)
            image.save(tmp / name)
            rec = rec_from_crop(i, name, image, meta)
        else:
            raise ValueError(f"unknown op {op}")
        records.append(rec)
        print(f"  {slug}/{name}  {rec['width']}x{rec['height']}  via={kind}")

    for old_png in parts.glob("frame_*.png"):
        old_png.unlink()
    for new_png in tmp.glob("frame_*.png"):
        new_png.replace(parts / new_png.name)
    tmp.rmdir()

    write_spine_fn(pack, dest_dir, records, sheet_w, sheet_h)
    peak = max(records, key=lambda r: r["area"])["filename"]
    manifest = {
        "id": slug,
        "title": pack["title"],
        "source_uuid": pack.get("uuid", old.get("source_uuid", "")),
        "source": str(sheet_path),
        "source_size": {"w": sheet_w, "h": sheet_h},
        "alpha_source": old.get("alpha_source", alpha_source),
        "fps": pack["fps"],
        "blend": pack["blend"],
        "pivot": pack.get("pivot", "center"),
        "island_threshold": ALPHA_THRESHOLD,
        "saved_count": len(records),
        "kind": pack.get("kind", "sequence"),
        "source_sheet": (extra or {}).get("source_sheet", old.get("source_sheet", "")),
        "peak_frame": peak,
        "parts": records,
        "audit": "manual keep/split/merge, crumbs removed, LTR TTB sequence",
    }
    if pack.get("speed_curve") and pack["speed_curve"] != "linear":
        manifest["speed_curve"] = pack["speed_curve"]
    if pack.get("frame_phases"):
        manifest["frame_phases"] = pack["frame_phases"]
    if pack.get("frame_scales") is not None:
        manifest["frame_scales"] = pack["frame_scales"]
    (parts / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"{slug}: {old['saved_count']} -> {len(records)}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", type=Path, default=None)
    p.add_argument("--ops", type=Path, required=True)
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    ops_map = json.loads(args.ops.read_text(encoding="utf-8"))
    deps = load_deps(dest)
    if isinstance(ops_map, dict) and "groups" in ops_map:
        source = ops_map["source"]
        for group in ops_map["groups"]:
            apply_one(
                dest,
                group["slug"],
                group["ops"],
                deps,
                source_slug=source,
                extra=group,
            )
        stage = dest / source
        delete_source = ops_map.get("delete_source")
        if delete_source is None:
            delete_source = source.startswith("_stage")
        if delete_source and stage.is_dir():
            shutil.rmtree(stage)
            print(f"removed {source}")
    else:
        for slug, ops in ops_map.items():
            apply_one(dest, slug, ops, deps)
    rebuild(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
