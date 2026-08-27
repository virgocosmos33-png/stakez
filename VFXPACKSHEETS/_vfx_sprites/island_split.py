"""
Bundled VFX island + alpha crop (no project dependency).

Detection is ALPHA-FIRST:
  1. If the sheet has no useful alpha, key near-black to alpha 0
     (soft ramp so glow / AA fringe survives). Existing alpha is kept.
  2. Erase separator-grid remnants (green thin lines and yellow/black
     hazard tape). Those gutters are never frames and never stay on a
     packed frame. Interior yellow-red art (handle wrap, fire, gas) stays.
  3. Islands = 8-connected components of pixels with alpha > threshold.
  4. Drop crumbs and tape-only bars. Crop each island to non-zero alpha
     and pad 1px of empty alpha on every side.

Standalone:
  python island_split.py path/to/sheet.png -o path/to/parts
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = Path("parts")

# Alpha above this counts as "non-empty" for island detection.
# 8 keeps glow bridges between close props; 12 splits them without
# eating lantern fringe on the saved pixels (crop still uses full alpha).
ALPHA_THRESHOLD = 12
# Soft black-key ramp used only when the source is fully opaque.
BLACK_LO = 6
BLACK_HI = 22
# Ignore dust specks (27x18 leftover at 271px is below this).
MIN_AREA = 400
# Optional binary close on the detect mask (px). 0 = off.
CLOSE_RADIUS = 0
# Transparent border around every saved prop.
PAD_PX = 1
USEFUL_ALPHA_FRACTION = 0.02
# Second pass: split oversized islands that share a thin alpha bridge
# (beam+lantern, sign+skull, side-by-side buildings).
GUTTER_SPLIT_MIN_AREA = 8000
GUTTER_SPLIT_MIN_EDGE = 80
BEAM_WIDE_FRAC = 0.50
BEAM_NARROW_FRAC = 0.10
NECK_WIDE_FRAC = 0.50
NECK_RATIO_MAX = 0.32
NECK_MIN_RUN = 16
NECK_SECOND_PEAK_MAX_FRAC = 0.80
SPARSE_FILL_FRAC = 0.15
# Separator LINE GRID remnants. The generator draws gutters so frames
# do not touch (basic green thin lines, or yellow/black hazard tape).
# Those pixels are NEVER a frame and NEVER part of a packed frame.
# Knife-handle wrap / fire / toxic glow can be yellow-red: only strip
# edge-aligned striped bars and obvious grid lines, never interior art.
SEP_YELLOW_R = 150
SEP_YELLOW_G = 100
SEP_YELLOW_B = 110
SEP_GREEN_G = 80
SEP_GREEN_DOMINANCE = 25
SEP_DARK_LUMA = 60
SEP_STRIPE_YEL = 0.18
SEP_STRIPE_DARK = 0.18
SEP_STRIPE_COMBO = 0.55
SEP_SOLID_YEL = 0.80
SEP_SOLID_DARK = 0.80
SEP_GREEN_LINE = 0.50
SEP_GREEN_MAX_THICK = 8
SEP_BAR_MAX_PX = 56
SEP_LOOKAHEAD = 28
SEP_STRIPE_MAX_INSET = 20
SEP_ONLY_ASPECT = 8.0
SEP_ONLY_THIN = 28
SEP_ONLY_TAPE_FRAC = 0.50
SEP_GOLD_ART_FRAC = 0.22
SHEET_MIN_W = 900
SHEET_MIN_H = 700


def soft_alpha_from_black(rgb: np.ndarray) -> np.ndarray:
    """Map near-black RGB to a soft alpha. Used only on opaque sheets."""
    luma = rgb.max(axis=2).astype(np.int16)
    alpha = np.zeros(luma.shape, dtype=np.uint8)
    span = max(1, BLACK_HI - BLACK_LO)
    mid = (luma > BLACK_LO) & (luma <= BLACK_HI)
    alpha[luma > BLACK_HI] = 255
    alpha[mid] = np.clip(
        ((luma[mid] - BLACK_LO) * 255 + span - 1) // span, 0, 255
    ).astype(np.uint8)
    return alpha


def ensure_alpha(rgba: np.ndarray) -> tuple[np.ndarray, str]:
    """Return RGBA whose empty background is alpha 0. Prefer existing alpha."""
    rgb = rgba[:, :, :3]
    src_a = rgba[:, :, 3]
    empty = int((src_a == 0).sum())
    if empty >= int(src_a.size * USEFUL_ALPHA_FRACTION):
        out = rgba.copy()
        out[:, :, 0][src_a == 0] = 0
        out[:, :, 1][src_a == 0] = 0
        out[:, :, 2][src_a == 0] = 0
        return out, "existing_alpha"
    keyed = rgba.copy()
    keyed[:, :, 3] = soft_alpha_from_black(rgb)
    keyed[:, :, 0][keyed[:, :, 3] == 0] = 0
    keyed[:, :, 1][keyed[:, :, 3] == 0] = 0
    keyed[:, :, 2][keyed[:, :, 3] == 0] = 0
    return keyed, "black_keyed"


def binary_close(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask
    return _erode(_dilate(mask, radius), radius)


def _dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    out = mask.copy()
    h, w = mask.shape
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            ys = slice(max(0, dy), h + min(0, dy))
            xs = slice(max(0, dx), w + min(0, dx))
            yd = slice(max(0, -dy), h + min(0, -dy))
            xd = slice(max(0, -dx), w + min(0, -dx))
            out[yd, xd] |= mask[ys, xs]
    return out


def _erode(mask: np.ndarray, radius: int) -> np.ndarray:
    out = mask.copy()
    h, w = mask.shape
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            ys = slice(max(0, dy), h + min(0, dy))
            xs = slice(max(0, dx), w + min(0, dx))
            yd = slice(max(0, -dy), h + min(0, -dy))
            xd = slice(max(0, -dx), w + min(0, -dx))
            out[yd, xd] &= mask[ys, xs]
    return out


def label_islands(mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    """8-connected labels. Returns (labels, areas, nlab). Label 0 is background."""
    h, w = mask.shape
    labels = np.zeros((h, w), dtype=np.int32)
    parent = [0]

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    nid = 0
    for y in range(h):
        row = mask[y]
        labrow = labels[y]
        prow = mask[y - 1] if y else None
        plab = labels[y - 1] if y else None
        for x in range(w):
            if not row[x]:
                continue
            neigh: list[int] = []
            if x and row[x - 1] and labrow[x - 1]:
                neigh.append(int(labrow[x - 1]))
            if y:
                if x and prow[x - 1] and plab[x - 1]:
                    neigh.append(int(plab[x - 1]))
                if prow[x] and plab[x]:
                    neigh.append(int(plab[x]))
                if x + 1 < w and prow[x + 1] and plab[x + 1]:
                    neigh.append(int(plab[x + 1]))
            if not neigh:
                nid += 1
                parent.append(nid)
                labrow[x] = nid
            else:
                m = min(neigh)
                labrow[x] = m
                for n in neigh:
                    if n != m:
                        union(m, n)

    roots = np.zeros(len(parent), dtype=np.int32)
    for i in range(1, len(parent)):
        roots[i] = find(i)
    uniq: dict[int, int] = {}
    next_id = 1
    for i in range(1, len(parent)):
        r = int(roots[i])
        if r not in uniq:
            uniq[r] = next_id
            next_id += 1
    remap = np.zeros(len(parent), dtype=np.int32)
    for i in range(1, len(parent)):
        remap[i] = uniq[int(roots[i])]
    out = remap[labels]
    nlab = next_id - 1
    areas = np.bincount(out.ravel(), minlength=nlab + 1)
    return out, areas, nlab


def alpha_bbox(alpha: np.ndarray) -> tuple[int, int, int, int] | None:
    ys, xs = np.where(alpha > 0)
    if ys.size == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def separator_color_masks(
    rgba: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Bright yellow, darker gold, green grid, dark stripe, opaque."""
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3]
    red = rgb[:, :, 0].astype(np.int16)
    grn = rgb[:, :, 1].astype(np.int16)
    blu = rgb[:, :, 2].astype(np.int16)
    opaque = alpha > 12
    bright = opaque & (
        (red >= SEP_YELLOW_R)
        & (grn >= SEP_YELLOW_G)
        & (blu <= SEP_YELLOW_B)
        & ((red + grn) > (blu * 3 + 40))
    )
    gold = opaque & (
        (red >= 90)
        & (grn >= 50)
        & (blu <= 45)
        & ((red + grn) > (blu * 3 + 20))
        & (red >= grn - 15)
    )
    green = (
        opaque
        & (grn >= SEP_GREEN_G)
        & (grn > red + SEP_GREEN_DOMINANCE)
        & (grn > blu + 15)
        & (red < 140)
        & (blu < 140)
    )
    dark = opaque & (rgb.max(axis=2) <= SEP_DARK_LUMA)
    return bright, gold, green, dark, opaque


def _scanline_fracs(mask: np.ndarray, axis: int) -> np.ndarray:
    length = mask.shape[1 - axis]
    return mask.sum(axis=1 - axis).astype(np.float64) / max(1, length)


def classify_separator_scanline(
    yel: float, dark: float, green: float, gold: float = 0.0
) -> str:
    if (
        yel >= SEP_STRIPE_YEL
        and dark >= SEP_STRIPE_DARK
        and (yel + dark) >= SEP_STRIPE_COMBO
    ):
        return "stripe"
    if green >= SEP_GREEN_LINE and yel < 0.12:
        return "green"
    if gold >= SEP_SOLID_YEL or yel >= SEP_SOLID_YEL:
        return "solid_yellow"
    if dark >= SEP_SOLID_DARK and yel < 0.10 and gold < 0.10:
        return "solid_dark"
    return "other"


def _collect_bar_indices(
    classes: list[str],
    max_thick: int,
    green_only_max: int,
    *,
    allow_green: bool = True,
) -> list[int]:
    """Keep a flush striped/green gutter plus a short solid outline. No gap resume."""
    core_at = [
        i
        for i, kind in enumerate(classes)
        if kind in ("stripe", "green") and i < SEP_LOOKAHEAD
    ]
    if not core_at:
        return []
    first_core = core_at[0]
    prefix = classes[: max(SEP_LOOKAHEAD, first_core + green_only_max + 4)]
    cores = [kind for kind in prefix if kind in ("stripe", "green")]
    green_only = bool(cores) and all(kind == "green" for kind in cores)
    if green_only:
        if not allow_green or first_core > 3:
            return []
    elif first_core > SEP_STRIPE_MAX_INSET:
        return []
        run = 0
        for kind in classes[first_core:]:
            if kind != "green":
                break
            run += 1
        if run > green_only_max:
            return []
        after = classes[first_core + run : first_core + run + 12]
        if not after or after.count("green") >= 3:
            return []
    start = first_core
    while start > 0 and classes[start - 1] in (
        "solid_yellow",
        "solid_dark",
        "stripe",
        "green",
    ):
        start -= 1
    end = first_core
    while end + 1 < len(classes) and classes[end + 1] in ("stripe", "green"):
        end += 1
    outline = 0
    while (
        end + 1 < len(classes)
        and classes[end + 1] in ("solid_yellow", "solid_dark")
        and outline < 4
    ):
        end += 1
        outline += 1
    # Same gutter can be stripe, then a yellow face, then more stripe.
    k = end + 1
    limit = min(len(classes), SEP_STRIPE_MAX_INSET + 8, start + max_thick)
    while k < limit:
        window = classes[k : k + 4]
        if not any(kind in ("stripe", "solid_yellow") for kind in window):
            break
        if classes[k] in ("stripe", "green", "solid_yellow", "solid_dark"):
            end = k
        k += 1
    if (end - start + 1) > max_thick:
        end = start + max_thick - 1
    return list(range(start, end + 1))


def _collect_leftover_outline(classes: list[str]) -> list[int]:
    """Thin gold/dark gutter line left after the striped face was erased."""
    first = next(
        (
            i
            for i, kind in enumerate(classes[:18])
            if kind in ("solid_dark", "solid_yellow")
        ),
        None,
    )
    if first is None:
        return []
    end = first
    while end + 1 < len(classes) and classes[end + 1] in ("solid_dark", "solid_yellow"):
        end += 1
    if (end - first + 1) > 8:
        return []
    after = classes[end + 1 : end + 9]
    if not after:
        return []
    if any(kind in ("stripe", "solid_dark", "solid_yellow") for kind in after[:3]):
        return []
    return list(range(first, end + 1))


def _thin_core_runs(classes: list[str], max_thick: int) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    i = 0
    n = len(classes)
    while i < n:
        if classes[i] not in ("stripe", "green"):
            i += 1
            continue
        j = i
        while j + 1 < n and classes[j + 1] in (
            "stripe",
            "green",
            "solid_yellow",
            "solid_dark",
        ):
            j += 1
        thick = j - i + 1
        if thick <= max_thick:
            start, end = i, j
            if start > 0 and classes[start - 1] in ("solid_yellow", "solid_dark"):
                start -= 1
            if end + 1 < n and classes[end + 1] in ("solid_yellow", "solid_dark"):
                end += 1
            if (end - start + 1) <= max_thick + 2:
                runs.append((start, end))
        i = j + 1
    return runs


def separator_pixel_mask(rgba: np.ndarray, mode: str = "auto") -> np.ndarray:
    """True on yellow/black hazard tape and thin green grid remnants."""
    height, width = rgba.shape[:2]
    bright, gold, green, dark, opaque = separator_color_masks(rgba)
    tape_color = bright | gold | green | dark
    out = np.zeros((height, width), dtype=bool)
    op_count = max(1, int(opaque.sum()))
    image_green_frac = float(green.sum()) / op_count
    yel_r = _scanline_fracs(bright, 0)
    gold_r = _scanline_fracs(bright | gold, 0)
    dark_r = _scanline_fracs(dark, 0)
    grn_r = _scanline_fracs(green, 0)
    yel_c = _scanline_fracs(bright, 1)
    gold_c = _scanline_fracs(bright | gold, 1)
    dark_c = _scanline_fracs(dark, 1)
    grn_c = _scanline_fracs(green, 1)
    sheet = mode == "sheet" or (
        mode == "auto" and width >= SHEET_MIN_W and height >= SHEET_MIN_H
    )
    allow_green = sheet or image_green_frac <= 0.12
    image_gold_frac = float((bright | gold).sum()) / op_count
    allow_gold_outline = sheet or image_gold_frac <= SEP_GOLD_ART_FRAC
    depth_h = min(SEP_BAR_MAX_PX, max(8, height // 4))
    depth_w = min(SEP_BAR_MAX_PX, max(8, width // 4))

    def row_classes(origin: str) -> list[str]:
        out_cls: list[str] = []
        for i in range(min(depth_h, height)):
            y = i if origin == "top" else height - 1 - i
            out_cls.append(
                classify_separator_scanline(
                    float(yel_r[y]),
                    float(dark_r[y]),
                    float(grn_r[y]),
                    float(gold_r[y]),
                )
            )
        return out_cls

    def col_classes(origin: str) -> list[str]:
        out_cls: list[str] = []
        for i in range(min(depth_w, width)):
            x = i if origin == "left" else width - 1 - i
            out_cls.append(
                classify_separator_scanline(
                    float(yel_c[x]),
                    float(dark_c[x]),
                    float(grn_c[x]),
                    float(gold_c[x]),
                )
            )
        return out_cls

    for origin, classes in (
        ("top", row_classes("top")),
        ("bottom", row_classes("bottom")),
    ):
        bar = _collect_bar_indices(
            classes, SEP_BAR_MAX_PX, SEP_GREEN_MAX_THICK, allow_green=allow_green
        )
        if not bar and allow_gold_outline:
            bar = _collect_leftover_outline(classes)
        for i in bar:
            y = i if origin == "top" else height - 1 - i
            out[y] |= tape_color[y]
    for origin, classes in (
        ("left", col_classes("left")),
        ("right", col_classes("right")),
    ):
        bar = _collect_bar_indices(
            classes, SEP_BAR_MAX_PX, SEP_GREEN_MAX_THICK, allow_green=allow_green
        )
        if not bar and allow_gold_outline:
            bar = _collect_leftover_outline(classes)
        for i in bar:
            x = i if origin == "left" else width - 1 - i
            out[:, x] |= tape_color[:, x]

    if sheet:
        row_cls = [
            classify_separator_scanline(
                float(yel_r[i]),
                float(dark_r[i]),
                float(grn_r[i]),
                float(gold_r[i]),
            )
            for i in range(height)
        ]
        col_cls = [
            classify_separator_scanline(
                float(yel_c[i]),
                float(dark_c[i]),
                float(grn_c[i]),
                float(gold_c[i]),
            )
            for i in range(width)
        ]
        for start, end in _thin_core_runs(row_cls, SEP_BAR_MAX_PX):
            for y in range(start, end + 1):
                out[y] |= tape_color[y]
        for start, end in _thin_core_runs(col_cls, SEP_BAR_MAX_PX):
            for x in range(start, end + 1):
                out[:, x] |= tape_color[:, x]

    if out.any():
        out = _dilate(out, 1) & tape_color
    return out


def erase_separator_grid(rgba: np.ndarray, mode: str = "auto") -> np.ndarray:
    """Make separator remnants transparent. Does not recrop."""
    out = rgba.copy()
    mask = separator_pixel_mask(out, mode=mode)
    if mask.any():
        out[mask] = 0
    return out


def is_separator_only(rgba: np.ndarray) -> bool:
    """True for a long thin striped bar with no real VFX."""
    bright, gold, green, dark, opaque = separator_color_masks(rgba)
    op_count = int(opaque.sum())
    if op_count == 0:
        return True
    height, width = opaque.shape
    min_d, max_d = min(height, width), max(height, width)
    tape = int((bright | gold | green | dark).sum())
    if max_d / max(1, min_d) >= SEP_ONLY_ASPECT and min_d <= SEP_ONLY_THIN:
        if tape / op_count >= SEP_ONLY_TAPE_FRAC:
            return True
    return False


def recrop_rgba(rgba: np.ndarray, pad: int = PAD_PX) -> np.ndarray | None:
    box = alpha_bbox(rgba[:, :, 3])
    if box is None:
        return None
    x0, y0, x1, y1 = box
    tile = rgba[y0:y1, x0:x1]
    canvas = np.zeros((y1 - y0 + pad * 2, x1 - x0 + pad * 2, 4), dtype=np.uint8)
    canvas[pad : pad + (y1 - y0), pad : pad + (x1 - x0)] = tile
    canvas[0, :, 3] = 0
    canvas[-1, :, 3] = 0
    canvas[:, 0, 3] = 0
    canvas[:, -1, 3] = 0
    canvas[canvas[:, :, 3] == 0, :3] = 0
    return canvas


def clean_separator_frame(
    rgba: np.ndarray, mode: str = "frame"
) -> tuple[np.ndarray | None, int]:
    """Erase grid remnants and re-alpha-crop. (None, n) means drop the island."""
    total = 0
    current = rgba
    for _ in range(3):
        erased = erase_separator_grid(current, mode=mode)
        n_erased = int(((current[:, :, 3] > 0) & (erased[:, :, 3] == 0)).sum())
        if is_separator_only(erased):
            return None, total + n_erased
        if n_erased == 0:
            return current, total
        cropped = recrop_rgba(erased)
        if cropped is None or is_separator_only(cropped):
            return None, total + n_erased
        total += n_erased
        current = cropped
    return current, total


def find_horizontal_cuts(mask: np.ndarray) -> list[int]:
    """Local-y cuts that separate glued props stacked vertically."""
    h, w = mask.shape
    if h < GUTTER_SPLIT_MIN_EDGE or int(mask.sum()) < GUTTER_SPLIT_MIN_AREA:
        return []
    row = mask.sum(axis=1).astype(np.int32)
    wide_thresh = max(16, int(BEAM_WIDE_FRAC * w))
    narrow_thresh = max(8, int(BEAM_NARROW_FRAC * w))
    collapse_window = 14
    for y in range(1, h):
        if row[y] > narrow_thresh:
            continue
        if not (0.08 * h < y < 0.85 * h):
            continue
        prior = row[max(0, y - collapse_window) : y]
        if prior.size and int(prior.max()) >= wide_thresh:
            return [int(y)]

    k = 7
    smooth = np.convolve(row.astype(np.float64), np.ones(k) / k, mode="same")
    mx = float(smooth.max()) if smooth.max() else 1.0
    wide = smooth > (NECK_WIDE_FRAC * mx)
    state = "start"
    run0 = 0
    best: tuple[float, int] | None = None
    for y in range(h):
        is_wide = bool(wide[y])
        if state == "start" and is_wide:
            state = "wide1"
        elif state == "wide1" and not is_wide:
            state = "neck"
            run0 = y
        elif state == "neck" and is_wide:
            run1 = y
            neck = smooth[run0:run1]
            if neck.size >= NECK_MIN_RUN and run1 < NECK_SECOND_PEAK_MAX_FRAC * h:
                ycut = int(run0 + int(np.argmin(neck)))
                ratio = float(neck.min()) / mx
                if 0.08 * h < ycut < 0.85 * h and ratio < NECK_RATIO_MAX:
                    if best is None or ratio < best[0]:
                        best = (ratio, ycut)
            state = "wide2"
        elif state == "wide2" and not is_wide:
            state = "neck"
            run0 = y
    return [best[1]] if best else []


def find_vertical_cuts(mask: np.ndarray) -> list[int]:
    """Local-x cuts that separate glued props sitting side by side."""
    h, w = mask.shape
    if w < GUTTER_SPLIT_MIN_EDGE or int(mask.sum()) < GUTTER_SPLIT_MIN_AREA:
        return []
    col = mask.sum(axis=0).astype(np.int32)
    wide_thresh = max(16, int(BEAM_WIDE_FRAC * h))
    narrow_thresh = max(8, int(BEAM_NARROW_FRAC * h))
    collapse_window = 14
    cuts: list[int] = []
    for x in range(1, w):
        if col[x] > narrow_thresh:
            continue
        if not (0.08 * w < x < 0.92 * w):
            continue
        prior = col[max(0, x - collapse_window) : x]
        if prior.size and int(prior.max()) >= wide_thresh:
            cuts.append(int(x))
    if cuts:
        return cuts

    k = 7
    smooth = np.convolve(col.astype(np.float64), np.ones(k) / k, mode="same")
    mx = float(smooth.max()) if smooth.max() else 1.0
    wide = smooth > (NECK_WIDE_FRAC * mx)
    state = "start"
    run0 = 0
    best: tuple[float, int] | None = None
    for x in range(w):
        is_wide = bool(wide[x])
        if state == "start" and is_wide:
            state = "wide1"
        elif state == "wide1" and not is_wide:
            state = "neck"
            run0 = x
        elif state == "neck" and is_wide:
            run1 = x
            neck = smooth[run0:run1]
            if neck.size >= NECK_MIN_RUN:
                xcut = int(run0 + int(np.argmin(neck)))
                ratio = float(neck.min()) / mx
                if 0.08 * w < xcut < 0.92 * w and ratio < NECK_RATIO_MAX:
                    if best is None or ratio < best[0]:
                        best = (ratio, xcut)
            state = "wide2"
        elif state == "wide2" and not is_wide:
            state = "neck"
            run0 = x
    return [best[1]] if best else []


def split_island_mask(full_mask: np.ndarray) -> list[np.ndarray]:
    """Second pass: cut one island on empty-alpha gutters / necks."""
    ys, xs = np.where(full_mask)
    if ys.size == 0:
        return []
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    sub = full_mask[y0:y1, x0:x1]
    hcuts = find_horizontal_cuts(sub)
    vcuts = find_vertical_cuts(sub)
    if not hcuts and not vcuts:
        return [full_mask]

    ys_cuts = [0] + sorted(hcuts) + [sub.shape[0]]
    xs_cuts = [0] + sorted(vcuts) + [sub.shape[1]]
    pieces: list[np.ndarray] = []
    for i in range(len(ys_cuts) - 1):
        for j in range(len(xs_cuts) - 1):
            piece = np.zeros_like(full_mask)
            y_a, y_b = ys_cuts[i], ys_cuts[i + 1]
            x_a, x_b = xs_cuts[j], xs_cuts[j + 1]
            tile = sub[y_a:y_b, x_a:x_b]
            if int(tile.sum()) < MIN_AREA:
                continue
            piece[y0 + y_a : y0 + y_b, x0 + x_a : x0 + x_b] = tile
            pieces.extend(tighten_sparse_mask(piece))
    return pieces if pieces else [full_mask]


def tighten_sparse_mask(full_mask: np.ndarray) -> list[np.ndarray]:
    """If a gutter piece is mostly empty, keep only real alpha islands."""
    ys, xs = np.where(full_mask)
    if ys.size == 0:
        return []
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    area = int(full_mask.sum())
    box = max(1, (x1 - x0) * (y1 - y0))
    if area / box >= SPARSE_FILL_FRAC:
        return [full_mask]
    sub = full_mask[y0:y1, x0:x1]
    labels, areas, nlab = label_islands(sub)
    out: list[np.ndarray] = []
    for i in range(1, nlab + 1):
        if int(areas[i]) < MIN_AREA:
            continue
        piece = np.zeros_like(full_mask)
        piece[y0:y1, x0:x1] = labels == i
        out.append(piece)
    return out if out else [full_mask]


def crop_island(
    rgba: np.ndarray,
    island: np.ndarray,
    pad: int,
) -> tuple[Image.Image, dict]:
    """Crop one island. Output is surrounded by empty alpha on all sides."""
    h, w = island.shape
    ys, xs = np.where(island)
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    area = int(island.sum())

    pw = (x1 - x0) + pad * 2
    ph = (y1 - y0) + pad * 2
    canvas = np.zeros((ph, pw, 4), dtype=np.uint8)
    tile = rgba[y0:y1, x0:x1].copy()
    tile_mask = island[y0:y1, x0:x1]
    tile[~tile_mask] = 0
    canvas[pad : pad + (y1 - y0), pad : pad + (x1 - x0)] = tile

    # Guarantee a transparent outer ring even if the island filled its bbox.
    canvas[0, :, 3] = 0
    canvas[-1, :, 3] = 0
    canvas[:, 0, 3] = 0
    canvas[:, -1, 3] = 0

    return Image.fromarray(canvas, "RGBA"), {
        "bbox": {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0},
        "area": area,
    }


def split_sheet(
    src: Path,
    out_dir: Path,
    alpha_threshold: int = ALPHA_THRESHOLD,
    min_area: int = MIN_AREA,
    close_radius: int = CLOSE_RADIUS,
    pad: int = PAD_PX,
    write_keyed: bool = False,
    gutter_split: bool = True,
) -> dict:
    if not src.is_file():
        raise FileNotFoundError(f"source sheet not found: {src}")

    raw = np.asarray(Image.open(src).convert("RGBA"))
    sheet_h, sheet_w = raw.shape[:2]
    keyed, alpha_source = ensure_alpha(raw)
    keyed = erase_separator_grid(keyed, mode="auto")
    alpha = keyed[:, :, 3]
    detect = alpha > alpha_threshold
    detect = binary_close(detect, close_radius)
    labels, areas, nlab = label_islands(detect)

    island_masks: list[np.ndarray] = []
    for i in range(1, nlab + 1):
        area = int(areas[i])
        if area < min_area:
            continue
        mask = labels == i
        if gutter_split:
            island_masks.extend(split_island_mask(mask))
        else:
            island_masks.append(mask)

    kept: list[tuple[int, int, np.ndarray, int, int, int]] = []
    for mask in island_masks:
        ys, xs = np.where(mask)
        if ys.size == 0:
            continue
        area = int(mask.sum())
        if area < min_area:
            continue
        x0, x1 = int(xs.min()), int(xs.max()) + 1
        y0, y1 = int(ys.min()), int(ys.max()) + 1
        kept.append((y0, x0, mask, area, x1 - x0, y1 - y0))
    kept.sort(key=lambda t: (t[0], t[1]))

    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("prop_*.png"):
        old.unlink()

    if write_keyed:
        Image.fromarray(keyed, "RGBA").save(out_dir / "keyed_sheet.png")

    records = []
    saved_idx = 0
    for y0, x0, mask, area, bw, bh in kept:
        image, meta = crop_island(keyed, mask, pad)
        cleaned, n_erased = clean_separator_frame(np.asarray(image), mode="frame")
        if cleaned is None:
            print(
                f"  drop separator-only island  area={area}  "
                f"src_bbox=({meta['bbox']['x']},{meta['bbox']['y']},"
                f"{meta['bbox']['w']}x{meta['bbox']['h']})"
            )
            continue
        image = Image.fromarray(cleaned, "RGBA")
        if image.size == (sheet_w, sheet_h):
            raise RuntimeError("saved island is still sheet-sized; split failed")
        saved_idx += 1
        name = f"prop_{saved_idx:02d}.png"
        dest = out_dir / name
        image.save(dest)
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
            f"  {name}  {image.size[0]}x{image.size[1]}  "
            f"area={rec['area']}  src_bbox=({meta['bbox']['x']},{meta['bbox']['y']},"
            f"{meta['bbox']['w']}x{meta['bbox']['h']}){extra}"
        )

    manifest = {
        "source": str(src),
        "source_size": {"w": sheet_w, "h": sheet_h},
        "alpha_source": alpha_source,
        "thresholds": {
            "alpha_threshold": alpha_threshold,
            "min_area": min_area,
            "close_radius": close_radius,
            "pad_px": pad,
            "black_lo": BLACK_LO,
            "black_hi": BLACK_HI,
            "gutter_split": gutter_split,
        },
        "island_count": int(nlab),
        "saved_count": len(records),
        "crumb_count": int(nlab) - len(records),
        "parts": records,
    }
    man_path = out_dir / "manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(
        f"islands={nlab} saved={len(records)} crumbs={nlab - len(records)} "
        f"alpha={alpha_source}"
    )
    return manifest


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Split a sheet by alpha islands")
    p.add_argument("src", nargs="?", type=Path, default=None)
    p.add_argument("-o", "--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--alpha-threshold", type=int, default=ALPHA_THRESHOLD)
    p.add_argument("--min-area", type=int, default=MIN_AREA)
    p.add_argument("--close", type=int, default=CLOSE_RADIUS)
    p.add_argument("--pad", type=int, default=PAD_PX)
    p.add_argument("--write-keyed", action="store_true")
    p.add_argument(
        "--no-gutter-split",
        action="store_true",
        help="Disable second-pass split of oversized glued islands",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.src is None:
        raise SystemExit("usage: python island_split.py path/to/sheet.png -o path/to/parts")
    split_sheet(
        src=args.src.resolve(),
        out_dir=args.out.resolve(),
        alpha_threshold=args.alpha_threshold,
        min_area=args.min_area,
        close_radius=args.close,
        pad=args.pad,
        write_keyed=args.write_keyed,
        gutter_split=not args.no_gutter_split,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
