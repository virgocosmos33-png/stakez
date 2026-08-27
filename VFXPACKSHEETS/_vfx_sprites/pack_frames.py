"""First-pass VFX frame pack: cluster islands, crop, write Spine 3.8."""
from __future__ import annotations

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
    clean_separator_frame,
    crop_island,
    ensure_alpha,
    erase_separator_grid,
    label_islands,
)
from rebuild_catalog import normalize_loop, pack_entry  # noqa: E402
from speed_curve import resolve_timing  # noqa: E402

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None

BODY_SEED_AREA = 1400
INTRO_SEED_AREA = 90
INTRO_Y_FRAC = 0.30
SEED_MERGE_IOU = 0.18
LEFTOVER_DILATE = 22
MIN_FRAME_AREA = 400
MAX_FRAME_W_FRAC = 0.55
MAX_FRAME_H_FRAC = 0.62


def bbox_iou(a: dict, b: dict) -> float:
    x0 = max(a["x"], b["x"])
    y0 = max(a["y"], b["y"])
    x1 = min(a["x1"], b["x1"])
    y1 = min(a["y1"], b["y1"])
    if x1 <= x0 or y1 <= y0:
        return 0.0
    inter = (x1 - x0) * (y1 - y0)
    union = a["w"] * a["h"] + b["w"] * b["h"] - inter
    return inter / union if union else 0.0


def collect_islands(detect: np.ndarray):
    if cv2 is not None:
        nlab, labels, stats, cents = cv2.connectedComponentsWithStats(
            detect.astype(np.uint8), connectivity=8
        )
        islands = []
        for i in range(1, nlab):
            x, y, w, h, area = (int(v) for v in stats[i])
            if area < 8:
                continue
            islands.append(
                {
                    "id": i,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                    "x1": x + w,
                    "y1": y + h,
                    "area": int(area),
                    "cx": float(cents[i][0]),
                    "cy": float(cents[i][1]),
                }
            )
        return islands, labels
    labels, areas, nlab = label_islands(detect)
    islands = []
    for i in range(1, nlab + 1):
        if int(areas[i]) < 8:
            continue
        ys, xs = np.where(labels == i)
        x0, y0 = int(xs.min()), int(ys.min())
        x1, y1 = int(xs.max()) + 1, int(ys.max()) + 1
        islands.append(
            {
                "id": i,
                "x": x0,
                "y": y0,
                "w": x1 - x0,
                "h": y1 - y0,
                "x1": x1,
                "y1": y1,
                "area": int(areas[i]),
                "cx": (x0 + x1) / 2,
                "cy": (y0 + y1) / 2,
            }
        )
    return islands, labels


def merge_seed_group(islands: list[dict], idxs: list[int]) -> dict:
    xs0 = min(islands[i]["x"] for i in idxs)
    ys0 = min(islands[i]["y"] for i in idxs)
    xs1 = max(islands[i]["x1"] for i in idxs)
    ys1 = max(islands[i]["y1"] for i in idxs)
    area = sum(islands[i]["area"] for i in idxs)
    return {
        "members": list(idxs),
        "x": xs0,
        "y": ys0,
        "w": xs1 - xs0,
        "h": ys1 - ys0,
        "x1": xs1,
        "y1": ys1,
        "area": area,
        "cx": (xs0 + xs1) / 2,
        "cy": (ys0 + ys1) / 2,
    }


def merge_overlapping_seeds(islands: list[dict], seed_ids: list[int]) -> list[dict]:
    parent = {i: i for i in seed_ids}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(seed_ids):
        for b in seed_ids[i + 1 :]:
            ia, ib = islands[a], islands[b]
            contained = (
                ia["x"] >= ib["x"]
                and ia["y"] >= ib["y"]
                and ia["x1"] <= ib["x1"]
                and ia["y1"] <= ib["y1"]
            ) or (
                ib["x"] >= ia["x"]
                and ib["y"] >= ia["y"]
                and ib["x1"] <= ia["x1"]
                and ib["y1"] <= ia["y1"]
            )
            if contained or bbox_iou(ia, ib) >= SEED_MERGE_IOU:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[rb] = ra
    groups: dict[int, list[int]] = {}
    for sid in seed_ids:
        groups.setdefault(find(sid), []).append(sid)
    return [merge_seed_group(islands, g) for g in groups.values()]


def pick_seeds(islands: list[dict], sheet_h: int) -> list[dict]:
    if not islands:
        return []
    seed_ids: list[int] = []
    for i, isl in enumerate(islands):
        if isl["area"] >= BODY_SEED_AREA:
            seed_ids.append(i)
            continue
        if isl["area"] >= INTRO_SEED_AREA and isl["cy"] <= INTRO_Y_FRAC * sheet_h:
            seed_ids.append(i)
    if not seed_ids:
        seed_ids = [int(np.argmax([isl["area"] for isl in islands]))]
    return merge_overlapping_seeds(islands, seed_ids)


def cluster_rows(seeds: list[dict]) -> list[list[int]]:
    if not seeds:
        return []
    med_h = float(np.median([s["h"] for s in seeds]))
    gap = max(48.0, med_h * 0.42)
    order = sorted(range(len(seeds)), key=lambda i: seeds[i]["cy"])
    rows: list[list[int]] = [[order[0]]]
    for i in order[1:]:
        if seeds[i]["cy"] - seeds[rows[-1][-1]]["cy"] > gap:
            rows.append([i])
        else:
            rows[-1].append(i)
    return rows


def assign_islands_to_seeds(
    islands: list[dict], seeds: list[dict]
) -> tuple[list[list[int]], list[int]]:
    assigned = [list(seed["members"]) for seed in seeds]
    leftover: list[int] = []
    seed_ids = {mid for seed in seeds for mid in seed["members"]}
    rows = cluster_rows(seeds)
    row_of = {}
    for r, members in enumerate(rows):
        for si in members:
            row_of[si] = r
    for i, isl in enumerate(islands):
        if i in seed_ids:
            continue
        if not seeds:
            leftover.append(i)
            continue
        row_idx = int(
            np.argmin([abs(isl["cy"] - seeds[si]["cy"]) for si in range(len(seeds))])
        )
        row_idx = row_of.get(row_idx, 0)
        row_seeds = rows[row_idx] if rows else list(range(len(seeds)))
        if not row_seeds:
            leftover.append(i)
            continue
        row_sorted = sorted(row_seeds, key=lambda si: seeds[si]["cx"])
        nearest = int(np.argmin([abs(isl["cx"] - seeds[si]["cx"]) for si in row_sorted]))
        si = row_sorted[nearest]
        same_row = abs(isl["cy"] - seeds[si]["cy"]) <= max(48.0, 0.70 * seeds[si]["h"])
        if same_row:
            assigned[si].append(i)
        else:
            leftover.append(i)
    return assigned, leftover


def leftover_frames(
    leftover: list[int],
    islands: list[dict],
    labels: np.ndarray,
    detect: np.ndarray,
) -> list[np.ndarray]:
    if not leftover:
        return []
    mask = np.zeros(detect.shape, dtype=np.uint8)
    for i in leftover:
        mask[labels == islands[i]["id"]] = 1
    if LEFTOVER_DILATE and cv2 is not None:
        k = 2 * LEFTOVER_DILATE + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
        mask = cv2.dilate(mask, kernel)
    frames: list[np.ndarray] = []
    if cv2 is None:
        lab, areas, nlab = label_islands(mask.astype(bool))
        for i in range(1, nlab + 1):
            if int(areas[i]) < MIN_FRAME_AREA:
                continue
            piece = (lab == i) & detect
            if int(piece.sum()) >= MIN_FRAME_AREA:
                frames.append(piece)
        return frames
    nlab, lab, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    for i in range(1, nlab):
        if int(stats[i][4]) < MIN_FRAME_AREA:
            continue
        piece = (lab == i) & detect
        if int(piece.sum()) >= MIN_FRAME_AREA:
            frames.append(piece)
    return frames


def frame_mask(members: list[int], islands: list[dict], labels: np.ndarray) -> np.ndarray:
    mask = np.zeros(labels.shape, dtype=bool)
    for i in members:
        mask |= labels == islands[i]["id"]
    return mask


def split_wide_mask(mask: np.ndarray) -> list[np.ndarray]:
    if cv2 is not None:
        nlab, labels, stats, _ = cv2.connectedComponentsWithStats(
            mask.astype(np.uint8), connectivity=8
        )
        pieces = []
        for i in range(1, nlab):
            if int(stats[i][4]) < MIN_FRAME_AREA:
                continue
            piece = labels == i
            ys, xs = np.where(piece)
            if ys.size == 0:
                continue
            if int(xs.max()) - int(xs.min()) + 1 > mask.shape[1] * 0.42:
                continue
            pieces.append(piece)
        return pieces if pieces else [mask]
    labels, areas, nlab = label_islands(mask)
    pieces = []
    for i in range(1, nlab + 1):
        if int(areas[i]) < MIN_FRAME_AREA:
            continue
        piece = labels == i
        ys, xs = np.where(piece)
        if ys.size == 0:
            continue
        if int(xs.max()) - int(xs.min()) + 1 > mask.shape[1] * 0.42:
            continue
        pieces.append(piece)
    return pieces if pieces else [mask]


def split_tall_mask(mask: np.ndarray) -> list[np.ndarray]:
    ys, xs = np.where(mask)
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    sub = mask[y0:y1, x0:x1]
    row = sub.sum(axis=1).astype(np.float64)
    if row.size < 48:
        return [mask]
    smooth = np.convolve(row, np.ones(9) / 9.0, mode="same")
    lo = int(0.22 * len(smooth))
    hi = int(0.78 * len(smooth))
    band = smooth[lo:hi]
    cut = lo + int(np.argmin(band))
    peak = float(smooth.max()) or 1.0
    if smooth[cut] > 0.16 * peak:
        return [mask]
    top = np.zeros_like(mask)
    bot = np.zeros_like(mask)
    top[y0 : y0 + cut, x0:x1] = sub[:cut]
    bot[y0 + cut : y1, x0:x1] = sub[cut:]
    pieces = [p for p in (top, bot) if int(p.sum()) >= MIN_FRAME_AREA]
    return pieces if pieces else [mask]


def order_masks_row_major(masks: list[np.ndarray]) -> list[np.ndarray]:
    items = []
    heights = []
    for mask in masks:
        ys, xs = np.where(mask)
        if ys.size == 0:
            continue
        h = int(ys.max()) - int(ys.min()) + 1
        heights.append(h)
        items.append(
            {
                "mask": mask,
                "cx": float((int(xs.min()) + int(xs.max()) + 1) / 2),
                "cy": float((int(ys.min()) + int(ys.max()) + 1) / 2),
            }
        )
    if not items:
        return []
    gap = max(48.0, float(np.median(heights)) * 0.42)
    items.sort(key=lambda it: it["cy"])
    rows = [[items[0]]]
    for it in items[1:]:
        if it["cy"] - rows[-1][-1]["cy"] > gap:
            rows.append([it])
        else:
            rows[-1].append(it)
    ordered = []
    for row in rows:
        row.sort(key=lambda it: it["cx"])
        ordered.extend(it["mask"] for it in row)
    return ordered


def cluster_frames(detect: np.ndarray) -> list[np.ndarray]:
    islands, labels = collect_islands(detect)
    seeds = pick_seeds(islands, detect.shape[0])
    assigned, leftover = assign_islands_to_seeds(islands, seeds)
    masks = []
    for members in assigned:
        if not members:
            continue
        mask = frame_mask(members, islands, labels)
        if int(mask.sum()) >= MIN_FRAME_AREA:
            masks.append(mask)
    masks.extend(leftover_frames(leftover, islands, labels, detect))
    scored = []
    sheet_w = detect.shape[1]
    max_w = int(sheet_w * 0.42)
    for mask in masks:
        ys, xs = np.where(mask)
        if ys.size == 0:
            continue
        bw = int(xs.max()) - int(xs.min()) + 1
        bh = int(ys.max()) - int(ys.min()) + 1
        pieces = [mask]
        if bw > max_w:
            pieces = split_wide_mask(mask)
        elif bh > int(detect.shape[0] * 0.40):
            pieces = split_tall_mask(mask)
        for piece in pieces:
            if np.where(piece)[0].size:
                scored.append(piece)
    return order_masks_row_major(scored)


def _attach_track(records: list[dict], durations: list[float]) -> list[dict]:
    keys = []
    t = 0.0
    last_name = records[0]["filename"][:-4]
    for rec, dur in zip(records, durations):
        last_name = rec["filename"][:-4]
        keys.append({"time": round(t, 4), "name": last_name})
        t += float(dur)
    keys.append({"time": round(t, 4), "name": last_name})
    return keys


def write_spine(pack: dict, dest_dir: Path, records: list[dict], sheet_w: int, sheet_h: int) -> None:
    if not records:
        return
    images = str(dest_dir / "parts").replace("\\", "/") + "/"
    skins = {"default": {"fx": {}}}
    loop = normalize_loop(pack, len(records))
    timing = resolve_timing(pack, len(records), loop)
    durations = timing["frame_durations"]
    pivot = pack.get("pivot", "center")
    for rec in records:
        name = rec["filename"][:-4]
        attach_y = rec["height"] / 2.0 if pivot == "bottom" else 0.0
        skins["default"]["fx"][name] = {
            "x": 0.0,
            "y": round(attach_y, 3),
            "width": rec["width"],
            "height": rec["height"],
        }
    slot = {"name": "fx", "bone": "fx", "attachment": records[0]["filename"][:-4]}
    if pack["blend"] == "add":
        slot["blend"] = "additive"
    animations = {
        "play": {"slots": {"fx": {"attachment": _attach_track(records, durations)}}}
    }
    if loop:
        hold_recs = records[loop[0] : loop[1] + 1]
        hold_durs = durations[loop[0] : loop[1] + 1]
        animations["hold"] = {
            "slots": {"fx": {"attachment": _attach_track(hold_recs, hold_durs)}}
        }
    skeleton = {
        "skeleton": {
            "hash": pack["slug"],
            "spine": "3.8.75",
            "x": 0,
            "y": 0,
            "width": sheet_w,
            "height": sheet_h,
            "images": images,
            "audio": "",
        },
        "bones": [{"name": "root"}, {"name": "fx", "parent": "root", "x": 0, "y": 0}],
        "slots": [slot],
        "skins": skins,
        "animations": animations,
    }
    spine_dir = dest_dir / "spine"
    spine_dir.mkdir(parents=True, exist_ok=True)
    (spine_dir / "skeleton.json").write_text(
        json.dumps(skeleton, indent=2), encoding="utf-8"
    )


def pack_one(library: Path, pack: dict) -> dict:
    library = Path(library)
    dest_dir = library / pack["slug"]
    parts_dir = dest_dir / "parts"
    dest_dir.mkdir(parents=True, exist_ok=True)
    sheet_dest = dest_dir / f"{pack['slug']}-sheet.png"
    src = Path(pack.get("sheet") or sheet_dest)
    if src.resolve() != sheet_dest.resolve():
        shutil.copy2(src, sheet_dest)
    raw = np.asarray(Image.open(sheet_dest).convert("RGBA"))
    keyed, alpha_source = ensure_alpha(raw)
    keyed = erase_separator_grid(keyed, mode="auto")
    detect = keyed[:, :, 3] > ALPHA_THRESHOLD
    masks = cluster_frames(detect)
    sheet_h, sheet_w = keyed.shape[:2]
    if parts_dir.exists():
        for old in parts_dir.glob("frame_*.png"):
            old.unlink()
    parts_dir.mkdir(parents=True, exist_ok=True)
    records = []
    saved_idx = 0
    for mask in masks:
        image, meta = crop_island(keyed, mask, PAD_PX)
        if (
            image.size[0] >= sheet_w * MAX_FRAME_W_FRAC
            and image.size[1] >= sheet_h * MAX_FRAME_H_FRAC
        ):
            continue
        cleaned, n_erased = clean_separator_frame(np.asarray(image), mode="frame")
        if cleaned is None:
            print(f"  {pack['slug']}/drop separator-only island area={meta['area']}")
            continue
        image = Image.fromarray(cleaned, "RGBA")
        saved_idx += 1
        name = f"frame_{saved_idx:02d}.png"
        image.save(parts_dir / name)
        rec = {
            "index": saved_idx,
            "filename": name,
            "bbox": meta["bbox"],
            "area": int((cleaned[:, :, 3] > 0).sum()),
            "width": image.size[0],
            "height": image.size[1],
        }
        records.append(rec)
        extra = f"  stripped={n_erased}" if n_erased else ""
        print(
            f"  {pack['slug']}/{name}  {image.size[0]}x{image.size[1]}  "
            f"area={rec['area']}{extra}"
        )
    for i, rec in enumerate(records, start=1):
        new_name = f"frame_{i:02d}.png"
        if rec["filename"] != new_name:
            (parts_dir / rec["filename"]).rename(parts_dir / new_name)
            rec["filename"] = new_name
            rec["index"] = i
    write_spine(pack, dest_dir, records, sheet_w, sheet_h)
    peak = max(records, key=lambda r: r["area"])["filename"] if records else ""
    timing = resolve_timing(pack, len(records), normalize_loop(pack, len(records)))
    manifest = {
        "id": pack["slug"],
        "title": pack["title"],
        "source_uuid": pack.get("uuid", ""),
        "source": str(sheet_dest),
        "source_size": {"w": sheet_w, "h": sheet_h},
        "alpha_source": alpha_source,
        "fps": pack["fps"],
        "blend": pack["blend"],
        "pivot": pack.get("pivot", "center"),
        "kind": pack.get("kind", "sequence"),
        "island_threshold": ALPHA_THRESHOLD,
        "saved_count": len(records),
        "peak_frame": peak,
        "parts": records,
    }
    if pack.get("speed_curve") or pack.get("speedCurve"):
        manifest["speed_curve"] = timing["speed_curve"]
    if pack.get("frame_phases") or pack.get("framePhases"):
        manifest["frame_phases"] = timing["frame_phases"]
    raw_scales = pack.get("frame_scales", pack.get("frameScales"))
    if raw_scales is not None:
        manifest["frame_scales"] = raw_scales
    (parts_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"{pack['slug']}: {len(records)} frames  alpha={alpha_source}")
    entry = pack_entry(library, pack["slug"])
    if not entry:
        raise RuntimeError("catalog entry missing after pack")
    return entry
