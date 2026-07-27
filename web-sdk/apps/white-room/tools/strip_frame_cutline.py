"""Strip the baked white dashed cut-line on the reel-frame opening rim.

Root cause: Scenario-generated mirror_frame_wide.png has a bright 1px dashed
'cut path' / highlight lip on the innermost opaque edge of the opening.
Not drawn by Pixi / CSS.

Strategy: restore-safe. Paint a dark metal seal band on the opaque side of the
opening (sampled from the existing dark bevel), covering the cutline without
moving the transparent well (bak-locked opening bbox).

Writes static + assets mirror_frame_wide.png and legacy mirror_frame.png alias.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
STATIC_DIR = HERE.parent / "static" / "assets" / "sprites" / "mirror"
APP_ASSETS_DIR = HERE.parent / "assets" / "sprites" / "mirror"
OUT_NAME = "mirror_frame_wide.png"
PRE_BAK = "mirror_frame_wide_PRE_CUTLINE_STRIP.png"
QA_DIR = HERE.parent

# Seal band depth into the opaque frame (px). Covers cutline + bright lip.
SEAL_DEPTH = 6.0
# Soft falloff so the seal blends into existing bevel (0 = hard, 1 = full depth fade)
SEAL_FEATHER = 0.55


def _distance_transform_edt_binary(mask: np.ndarray) -> np.ndarray:
    """Distance from each True cell to nearest False cell."""
    try:
        from scipy import ndimage  # type: ignore

        return ndimage.distance_transform_edt(mask).astype(np.float32)
    except Exception:
        pass
    try:
        import cv2  # type: ignore

        src = mask.astype(np.uint8) * 255
        return cv2.distanceTransform(src, cv2.DIST_L2, 5).astype(np.float32)
    except Exception:
        pass

    h, w = mask.shape
    dist = np.full((h, w), 1e6, dtype=np.float32)
    dist[~mask] = 0.0
    changed = True
    while changed:
        changed = False
        n = dist.copy()
        n[1:, :] = np.minimum(n[1:, :], dist[:-1, :] + 1)
        n[:-1, :] = np.minimum(n[:-1, :], dist[1:, :] + 1)
        n[:, 1:] = np.minimum(n[:, 1:], dist[:, :-1] + 1)
        n[:, :-1] = np.minimum(n[:, :-1], dist[:, 1:] + 1)
        n = np.where(mask, n, 0.0)
        if not np.allclose(n, dist):
            changed = True
        dist = n
    return dist


def find_opening(a: np.ndarray) -> tuple[int, int, int, int]:
    alpha = a[..., 3]
    h, w = alpha.shape

    def max_run(row: np.ndarray) -> tuple[int, int]:
        padded = np.concatenate(([0], row.astype(np.int8), [0]))
        d = np.diff(padded)
        starts = np.where(d == 1)[0]
        ends = np.where(d == -1)[0]
        lengths = ends - starts
        k = int(lengths.argmax())
        return int(starts[k]), int(lengths[k])

    ox, ow = max_run((alpha[h // 2] < 20))
    oy, oh = max_run((alpha[:, w // 2] < 20))
    return ox, oy, ow, oh


def strip_cutline(im: Image.Image) -> Image.Image:
    arr = np.asarray(im.convert("RGBA")).copy()
    rgb = arr[..., :3].astype(np.float32)
    alpha = arr[..., 3].astype(np.float32)

    opaque = alpha > 20
    dist = _distance_transform_edt_binary(opaque)
    dist_to_opaque = _distance_transform_edt_binary(~opaque)
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]

    # Sample dark metal bevel: opaque pixels 2–5px from opening with low luminance
    sample_zone = opaque & (dist >= 2.0) & (dist <= 5.0) & (lum < 90)
    if int(sample_zone.sum()) < 50:
        sample_zone = opaque & (dist >= 1.5) & (dist <= 6.0) & (lum < 120)
    if int(sample_zone.sum()) < 20:
        raise SystemExit("could not sample dark bevel for seal color")

    seal_rgb = np.array(
        [
            float(np.median(rgb[..., 0][sample_zone])),
            float(np.median(rgb[..., 1][sample_zone])),
            float(np.median(rgb[..., 2][sample_zone])),
        ],
        dtype=np.float32,
    )
    print(
        f"seal_rgb={seal_rgb.tolist()} from {int(sample_zone.sum())} bevel px",
        flush=True,
    )

    # Band to seal: entire opaque rim within SEAL_DEPTH of opening
    band = opaque & (dist > 0) & (dist <= SEAL_DEPTH)
    # Blend weight: full cover near opening, feather out
    # t=0 at opening edge, t=1 at SEAL_DEPTH
    t = np.clip(dist / SEAL_DEPTH, 0.0, 1.0)
    # Strong cover on inner half; feather on outer half
    w = np.ones_like(t)
    feather_start = 1.0 - SEAL_FEATHER
    outer = t > feather_start
    w[outer] = 1.0 - (t[outer] - feather_start) / max(SEAL_FEATHER, 1e-6)
    w = np.where(band, w, 0.0).astype(np.float32)

    # Extra force on bright cutline pixels (kill residual white dashes)
    bright_lip = band & (lum > 140)
    w = np.where(bright_lip, np.maximum(w, 0.92), w)

    out = arr.copy()
    for c in range(3):
        ch = rgb[..., c]
        blended = ch * (1.0 - w) + seal_rgb[c] * w
        out[..., c] = np.clip(blended, 0, 255).astype(np.uint8)

    # Harden the opening lip: semi-transparent fringe composites as a dashed
    # speckled cutline against the reel matte. Dark semis -> full opaque seal;
    # light semis -> fully transparent. Clear RGB in fully-transparent cells
    # near the opening so filter/nine-slice bleed can't resurrect a bright edge.
    out_alpha = out[..., 3].astype(np.float32)
    out_lum = (
        0.2126 * out[..., 0].astype(np.float32)
        + 0.7152 * out[..., 1].astype(np.float32)
        + 0.0722 * out[..., 2].astype(np.float32)
    )
    semi = (out_alpha > 0) & (out_alpha < 255)
    near_open_semi = semi & (dist <= 2.5)
    make_opaque = near_open_semi & (out_lum < 80)
    make_zero = near_open_semi | ((out_alpha > 0) & (out_alpha < 200) & (dist_to_opaque <= 1.5) & (out_lum >= 70))
    # resolve overlap: opaque wins for dark, zero for light
    make_zero = make_zero & ~make_opaque
    out[make_opaque, 0] = int(seal_rgb[0])
    out[make_opaque, 1] = int(seal_rgb[1])
    out[make_opaque, 2] = int(seal_rgb[2])
    out[make_opaque, 3] = 255
    out[make_zero] = 0

    ox, oy, ow, oh = find_opening(arr)
    clear = np.zeros(out_alpha.shape, dtype=bool)
    clear[oy - 2 : oy + oh + 2, ox - 2 : ox + ow + 2] = True
    trans_near = (out[..., 3] == 0) & clear
    out[trans_near, 0:3] = 0

    print(
        f"band={int(band.sum())} bright_lip={int(bright_lip.sum())} "
        f"make_opaque={int(make_opaque.sum())} make_zero={int(make_zero.sum())} "
        f"mean_w={float(w[band].mean()):.3f}",
        flush=True,
    )
    return Image.fromarray(out, "RGBA")


def _atomic_save(im: Image.Image, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp.png")
    im.save(tmp, format="PNG")
    try:
        tmp.replace(dest)
    except OSError as e:
        alt = dest.with_name(dest.stem + "_wr.png")
        im.save(alt)
        print(f"[warn] locked {dest.name} ({e}); wrote {alt.name}", flush=True)
    else:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        print(f"wrote {dest} ({dest.stat().st_size} bytes)", flush=True)


def main() -> None:
    bak = STATIC_DIR / PRE_BAK
    src = STATIC_DIR / OUT_NAME
    if bak.is_file():
        before_im = Image.open(bak).convert("RGBA")
        print(f"src=PRE bak {bak.name}", flush=True)
    elif src.is_file():
        before_im = Image.open(src).convert("RGBA")
        before_im.save(bak)
        print(f"src={src}; wrote PRE bak", flush=True)
    else:
        raise SystemExit(f"missing {src}")

    before = find_opening(np.asarray(before_im))
    print(f"opening_before={before}", flush=True)

    out_im = strip_cutline(before_im)
    after = find_opening(np.asarray(out_im))
    print(f"opening_after={after}", flush=True)
    if after != before:
        raise SystemExit(f"OPENING GEOMETRY CHANGED {before} -> {after}; aborting write")

    ox, oy, ow, oh = after
    out_im.crop((ox - 40, oy + 200, ox + 20, oy + 500)).resize(
        (180, 900), Image.Resampling.NEAREST
    ).save(QA_DIR / ".tmp_qa_frame_edge_left_AFTER.png")
    out_im.crop((ox + 400, oy - 40, ox + 800, oy + 20)).resize(
        (1200, 180), Image.Resampling.NEAREST
    ).save(QA_DIR / ".tmp_qa_frame_edge_top_AFTER.png")
    out_im.crop((ox - 50, oy - 50, ox + 200, oy + 200)).resize(
        (750, 750), Image.Resampling.NEAREST
    ).save(QA_DIR / ".tmp_qa_frame_corner_AFTER.png")
    strip = np.asarray(out_im)[oy - 20 : oy + 5, ox + 200 : ox + 900]
    Image.fromarray(strip).resize(
        (strip.shape[1] * 2, strip.shape[0] * 8), Image.Resampling.NEAREST
    ).save(QA_DIR / ".tmp_qa_topstrip_AFTER.png")
    print("wrote QA after-crops", flush=True)

    _atomic_save(out_im, STATIC_DIR / OUT_NAME)
    _atomic_save(out_im, APP_ASSETS_DIR / OUT_NAME)
    _atomic_save(out_im, STATIC_DIR / "mirror_frame.png")
    print("OK: cutline sealed; opening bak-locked", flush=True)


if __name__ == "__main__":
    main()
