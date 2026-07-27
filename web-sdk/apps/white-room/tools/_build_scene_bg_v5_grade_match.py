"""Grade-match scene_bg still to the same cold clinical look as lady idle v5.

Reuses the shared pipeline from _build_lady_idle_v5_grade_match.py:
  1) Desaturate RGB to Rec.709 luma (sat 0)
  2) Histogram-match luma CDF to the cold clinical reference still
  3) Recolor with identical cool tint (R*0.969 G*1.002 B*1.069)

Source: assets-raw/scene/scene_bg.png (fallback: shipped scene_bg.png)
Ship:   scene_bg_v5.webp (+ .png) into assets/ + static/ sprites/scene/
Cache-bust filename so Vite/browser pick up the new grade.

Run: python tools/_build_scene_bg_v5_grade_match.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# Allow importing sibling tool modules.
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from _build_lady_idle_v5_grade_match import (  # noqa: E402
    TINT_B,
    TINT_G,
    TINT_R,
    build_ref_target,
    cdf_from_luma,
    hist_match_lut,
    luma709,
)

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
QA = RAW / "_qa_v5"

SRC_CANDIDATES = (
    RAW / "scene_bg.png",
    VITE / "scene_bg.png",
    STATIC / "scene_bg.png",
    VITE / "scene_bg.webp",
    STATIC / "scene_bg.webp",
)

OUT_NAME_WEBP = "scene_bg_v5.webp"
OUT_NAME_PNG = "scene_bg_v5.png"


def apply_grade_rgb(rgb: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """Desaturate -> hist-match via lut -> cool tint. Full-frame RGB."""
    L = luma709(rgb.astype(np.float64))
    L_u8 = np.clip(np.rint(L), 0, 255).astype(np.uint8)
    L_matched = lut[L_u8].astype(np.float64)
    out = np.zeros_like(rgb, dtype=np.float64)
    out[..., 0] = L_matched * TINT_R
    out[..., 1] = L_matched * TINT_G
    out[..., 2] = L_matched * TINT_B
    return np.clip(np.rint(out), 0, 255).astype(np.uint8)


def mean_rgbl(rgb: np.ndarray) -> list[float]:
    L = luma709(rgb.astype(np.float64))
    return [
        float(rgb[..., 0].mean()),
        float(rgb[..., 1].mean()),
        float(rgb[..., 2].mean()),
        float(L.mean()),
    ]


def main() -> None:
    src = next((p for p in SRC_CANDIDATES if p.is_file()), None)
    if src is None:
        raise SystemExit("missing scene_bg source (assets-raw/scene/scene_bg.png)")

    tgt_cdf, ref_meta = build_ref_target()
    print("REF", json.dumps(ref_meta, indent=2), flush=True)
    print(f"SRC {src}", flush=True)

    im = Image.open(src).convert("RGB")
    rgb = np.array(im)
    before = mean_rgbl(rgb)
    src_cdf = cdf_from_luma(luma709(rgb.astype(np.float64)))
    lut = hist_match_lut(src_cdf, tgt_cdf)
    graded = apply_grade_rgb(rgb, lut)
    after = mean_rgbl(graded)
    print(f"grade before mean RGBL={before}", flush=True)
    print(f"grade after  mean RGBL={after}", flush=True)

    QA.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    VITE.mkdir(parents=True, exist_ok=True)
    STATIC.mkdir(parents=True, exist_ok=True)

    out_img = Image.fromarray(graded)
    # Keep an ungraded master copy if we are grading the raw master in place later.
    master_bak = RAW / "scene_bg_pre_v5.png"
    if src.resolve() == (RAW / "scene_bg.png").resolve() and not master_bak.exists():
        shutil.copy2(src, master_bak)
        print(f"backed up pre-grade master -> {master_bak}", flush=True)

    qa_png = QA / "scene_bg_v5_graded.png"
    out_img.save(qa_png, optimize=True)

    # Ship cache-bust names into vite + static.
    for dest_dir in (VITE, STATIC):
        png_path = dest_dir / OUT_NAME_PNG
        webp_path = dest_dir / OUT_NAME_WEBP
        out_img.save(png_path, optimize=True)
        out_img.save(webp_path, quality=90, method=6)
        print(f"wrote {png_path} ({png_path.stat().st_size} bytes)", flush=True)
        print(f"wrote {webp_path} ({webp_path.stat().st_size} bytes)", flush=True)

    # Also keep a graded master under assets-raw for prepare_scene_assets / redo.
    raw_graded = RAW / OUT_NAME_PNG
    out_img.save(raw_graded, optimize=True)

    summary = {
        "src": str(src),
        "ref": ref_meta,
        "mean_rgbl_before": before,
        "mean_rgbl_after": after,
        "tint_rgb": [TINT_R, TINT_G, TINT_B],
        "vite_webp": str(VITE / OUT_NAME_WEBP),
        "static_webp": str(STATIC / OUT_NAME_WEBP),
        "qa": str(qa_png),
        "wire": "assets.ts sceneBg + asset.manifest.json backgrounds.scene.still -> scene_bg_v5.webp",
    }
    (QA / "build_summary_scene_bg_v5.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("DONE", json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
