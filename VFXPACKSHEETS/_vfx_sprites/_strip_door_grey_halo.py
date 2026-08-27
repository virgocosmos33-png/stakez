"""Strip Recraft grey/white silhouette fringe from riveted-plank-door-swing.

Wood and dark iron stay. Grey/white rim pixels and leftover grey islands
are zeroed, then each part is recropped with a 1px pad.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from edit_pack import load_manifest, rewrite_spine, write_manifest
from rebuild_catalog import normalize_loop, rebuild

DEST = Path(r"C:\Users\Emex33\Documents\tombstone reborn\VFXPACKSHEETS")
PACK_DIR = DEST / "riveted-plank-door-swing"
PARTS = PACK_DIR / "parts"
PAD = 1
SAT_MAX = 32
LUMA_MIN = 68
ALPHA_HOLE = 16
ALPHA_KEEP = 8


def grey_mask(arr: np.ndarray) -> np.ndarray:
    rgb = arr[:, :, :3].astype(np.int16)
    a = arr[:, :, 3]
    mx = rgb.max(axis=2)
    sat = mx - rgb.min(axis=2)
    return (sat < SAT_MAX) & (mx > LUMA_MIN) & (a > 0)


def strip_edge_halo(arr: np.ndarray) -> tuple[np.ndarray, int]:
    a = arr[:, :, 3].astype(np.int16)
    grey = grey_mask(arr)
    low = a < ALPHA_HOLE
    neigh = np.zeros(a.shape, dtype=bool)
    neigh[1:] |= low[:-1]
    neigh[:-1] |= low[1:]
    neigh[:, 1:] |= low[:, :-1]
    neigh[:, :-1] |= low[:, 1:]
    neigh[1:, 1:] |= low[:-1, :-1]
    neigh[1:, :-1] |= low[:-1, 1:]
    neigh[:-1, 1:] |= low[1:, :-1]
    neigh[:-1, :-1] |= low[1:, 1:]
    drop = grey & neigh
    out = arr.copy()
    out[drop] = 0
    out[out[:, :, 3] == 0, :3] = 0
    return out, int(drop.sum())


def drop_grey_islands_numpy(arr: np.ndarray) -> tuple[np.ndarray, int]:
    """Flood-fill grey components without scipy."""
    grey = grey_mask(arr)
    if not grey.any():
        return arr, 0
    h, w = grey.shape
    seen = np.zeros((h, w), dtype=bool)
    out = arr.copy()
    dropped = 0
    a = arr[:, :, 3]
    for y, x in zip(*np.where(grey)):
        if seen[y, x]:
            continue
        stack = [(int(y), int(x))]
        cells: list[tuple[int, int]] = []
        ring_empty = 0
        ring_n = 0
        seen[y, x] = True
        while stack:
            cy, cx = stack.pop()
            cells.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = cy + dy, cx + dx
                    if ny < 0 or nx < 0 or ny >= h or nx >= w:
                        ring_n += 1
                        ring_empty += 1
                        continue
                    if grey[ny, nx]:
                        if not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
                        continue
                    ring_n += 1
                    if a[ny, nx] < ALPHA_HOLE:
                        ring_empty += 1
        isolated = ring_n > 0 and (ring_empty / ring_n) > 0.55
        tiny = len(cells) < 8
        if isolated or tiny:
            for cy, cx in cells:
                out[cy, cx] = 0
            dropped += len(cells)
    out[out[:, :, 3] == 0, :3] = 0
    return out, dropped


def trim_right_grey_columns(arr: np.ndarray) -> tuple[np.ndarray, int]:
    """Walk in from the hinge side and drop grey/empty columns."""
    out = arr.copy()
    dropped = 0
    h, w = arr.shape[:2]
    for x in range(w - 1, -1, -1):
        col = out[:, x]
        live = col[:, 3] > 0
        if not live.any():
            continue
        rgb = col[live, :3].astype(np.int16)
        mx = rgb.max(axis=1)
        sat = mx - rgb.min(axis=1)
        grey_frac = float(((sat < SAT_MAX) & (mx > LUMA_MIN)).mean())
        if grey_frac >= 0.7:
            dropped += int(live.sum())
            out[:, x] = 0
            continue
        break
    out[out[:, :, 3] == 0, :3] = 0
    return out, dropped


def recrop(arr: np.ndarray) -> np.ndarray:
    a = arr[:, :, 3]
    ys, xs = np.where(a > ALPHA_KEEP)
    if xs.size == 0:
        return arr
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    crop = arr[y0:y1, x0:x1]
    ch, cw = crop.shape[:2]
    canvas = np.zeros((ch + PAD * 2, cw + PAD * 2, 4), dtype=np.uint8)
    canvas[PAD : PAD + ch, PAD : PAD + cw] = crop
    return canvas


def clean(arr: np.ndarray) -> tuple[np.ndarray, int]:
    total = 0
    for _ in range(6):
        arr, n = strip_edge_halo(arr)
        total += n
        if n == 0:
            break
    arr, n = drop_grey_islands_numpy(arr)
    total += n
    arr, n = trim_right_grey_columns(arr)
    total += n
    for _ in range(3):
        arr, n = strip_edge_halo(arr)
        total += n
        if n == 0:
            break
    return recrop(arr), total


def right_summary(arr: np.ndarray, name: str) -> None:
    rgb = arr[:, :, :3].astype(np.int16)
    a = arr[:, :, 3]
    h, w = a.shape
    print(f"{name} {w}x{h}")
    for x in range(max(0, w - 6), w):
        live = a[:, x] > 0
        if not live.any():
            print(f"  x={x}: empty")
            continue
        col = rgb[live, x]
        mx = col.max(axis=1)
        sat = mx - col.min(axis=1)
        mean_rgb = col.mean(axis=0)
        print(
            f"  x={x}: live={int(live.sum())} "
            f"rgb~({int(mean_rgb[0])},{int(mean_rgb[1])},{int(mean_rgb[2])}) "
            f"sat~{float(sat.mean()):.1f} luma~{float(mx.mean()):.1f} "
            f"a~{float(a[live, x].mean()):.1f}"
        )


def main() -> None:
    man = load_manifest(PACK_DIR)
    records = []
    for rec in man["parts"]:
        path = PARTS / rec["filename"]
        arr = np.asarray(Image.open(path).convert("RGBA"))
        cleaned, n = clean(arr)
        Image.fromarray(cleaned, "RGBA").save(path)
        rec = dict(rec)
        rec["width"] = int(cleaned.shape[1])
        rec["height"] = int(cleaned.shape[0])
        rec["area"] = rec["width"] * rec["height"]
        records.append(rec)
        print(f"{path.name} dropped={n} -> {rec['width']}x{rec['height']}")
        right_summary(cleaned, "  after")

    loop = normalize_loop(man, len(records))
    write_manifest(PACK_DIR, man, records, loop)
    rewrite_spine(PACK_DIR, man, records, loop)
    rebuild(DEST)
    print("\npack rewritten")


if __name__ == "__main__":
    main()
