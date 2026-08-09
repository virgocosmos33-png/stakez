"""Build SceneCharacter BASE mid-idle v1: grade-matched seamless ping-pong.

Source: Scenario asset_YaH9ZZ6PMrcWmn9es1NyeDhr (Pixelcut ALPHA_MODE=1 VP9, 720x1280, 16fps).
Inserted in base sequencer BETWEEN breath and move:
  breath x5 → mid x1 → move x1 → repeat. Muted. Bonus untouched.

Same contract as breath/move v5:
  frames[0..N-1] + frames[N-2..0]  -> length 2N-1, start==end (seamless).
  Grade: desat Rec.709 → hist-match cold clinical ref → cool tint.
  Alpha: preserve Pixelcut + island scrub. Encode muted VP9 yuva420p.

Run: python tools/_build_lady_idle_mid_v1.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from _post_lady_idle_alpha import robust_copy, strip_detached_islands
from _build_lady_idle_v5_grade_match import (
    REF_PNG,
    TINT_B,
    TINT_G,
    TINT_R,
    apply_grade_dir,
    build_ref_target,
    extract_edge_frames,
    frame_mse,
    hist_match_lut,
    sample_clip_cdf,
    write_pingpong_sequence,
)

APP = Path(__file__).resolve().parents[1]
SRC_DIR = APP / "assets-raw" / "lady_video" / "_mid_v1_src"
RAW = APP / "assets-raw" / "lady_video"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
QA = SRC_DIR / "_qa"
SRC = SRC_DIR / "mid_src.webm"
OUT_NAME = "lady_idle_mid_v1.webm"
# Source is 16fps (Scenario Pixelcut); preserve rate so duration stays ~5s fwd.
FPS = 16
SCENARIO_ID = "asset_YaH9ZZ6PMrcWmn9es1NyeDhr"


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:10])}...\n{result.stderr[-2500:]}")


def extract_rgba_frames(src: Path, frames_dir: Path) -> int:
    frames_dir.mkdir(parents=True, exist_ok=True)
    for p in frames_dir.glob("*.png"):
        p.unlink()
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-i", str(src),
            "-pix_fmt", "rgba",
            str(frames_dir / "f_%04d.png"),
        ]
    )
    paths = sorted(frames_dir.glob("f_*.png"))
    if not paths:
        raise RuntimeError(f"no frames extracted from {src}")
    return len(paths)


def encode_alpha_webm(frames_glob: Path, out_webm: Path, fps: int = FPS) -> None:
    out_webm.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(fps),
            "-i", str(frames_glob),
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuva420p",
            "-b:v", "0",
            "-crf", "28",
            "-auto-alt-ref", "0",
            "-an",
            str(out_webm),
        ]
    )


def scrub_png_dir(frames_dir: Path) -> int:
    total = 0
    for p in sorted(frames_dir.glob("p_*.png")):
        arr = np.array(Image.open(p).convert("RGBA"))
        cleaned, dropped = strip_detached_islands(arr)
        total += dropped
        if dropped:
            Image.fromarray(cleaned).save(p)
    return total


def probe_duration(webm: Path) -> dict:
    out = subprocess.run(
        [
            "ffprobe", "-v", "error", "-count_frames",
            "-select_streams", "v:0",
            "-show_entries", "stream=nb_read_frames,r_frame_rate,duration,pix_fmt,codec_name",
            "-of", "json", str(webm),
        ],
        capture_output=True, text=True, check=True,
    ).stdout
    st = json.loads(out)["streams"][0]
    num, den = st["r_frame_rate"].split("/")
    fps = float(num) / float(den)
    n = int(st.get("nb_read_frames") or 0)
    dur = n / fps if fps else 0.0
    return {
        "frames": n,
        "fps": fps,
        "duration_s": round(dur, 4),
        "pix_fmt": st.get("pix_fmt"),
        "codec": st.get("codec_name"),
        "bytes": webm.stat().st_size,
    }


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing source: {SRC}")
    if not REF_PNG.exists():
        raise SystemExit(f"missing grade reference: {REF_PNG}")

    STATIC.mkdir(parents=True, exist_ok=True)
    VITE.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    tgt_cdf, ref_meta = build_ref_target()
    print("REF", json.dumps(ref_meta, indent=2), flush=True)

    work = Path(tempfile.mkdtemp(prefix="lady_mid_v1_"))
    raw_frames = work / "raw"
    pp_frames = work / "pp"

    n = extract_rgba_frames(SRC, raw_frames)
    print(f"[mid] source frames={n} @ {FPS}fps", flush=True)
    if n < 3:
        raise RuntimeError(f"mid: need >=3 frames, got {n}")

    # Alpha sanity: Pixelcut should have transparent corners.
    sample = np.array(Image.open(raw_frames / f"f_{max(1, n // 2):04d}.png").convert("RGBA"))
    frac0 = float((sample[..., 3] == 0).mean())
    print(f"[mid] mid-frame alpha frac0={frac0:.4f}", flush=True)
    if frac0 < 0.1:
        raise RuntimeError("mid: no transparent alpha — decode failed or wrong source")

    src_cdf = sample_clip_cdf(raw_frames, n, step=3)
    lut = hist_match_lut(src_cdf, tgt_cdf)
    grade_stats = apply_grade_dir(raw_frames, lut)
    print(f"[mid] grade before mean RGBL={grade_stats['mean_rgba_luma_before']}", flush=True)
    print(f"[mid] grade after  mean RGBL={grade_stats['mean_rgba_luma_after']}", flush=True)

    mid = raw_frames / f"f_{max(1, n // 2):04d}.png"
    qa_mid = QA / "mid_graded_mid.png"
    shutil.copy2(mid, qa_mid)

    total = write_pingpong_sequence(raw_frames, pp_frames, n)
    expected = 2 * n - 1
    if total != expected:
        raise RuntimeError(f"mid: pingpong len {total} != {expected}")
    print(f"[mid] pingpong frames={total} (= 2*{n}-1)", flush=True)

    first_png = pp_frames / "p_0001.png"
    last_png = pp_frames / f"p_{total:04d}.png"
    wrap_mse = frame_mse(first_png, last_png)
    print(f"[mid] png start==end MSE={wrap_mse:.6f}", flush=True)
    if wrap_mse > 0.5:
        raise RuntimeError(f"mid: start/end frames do not match (MSE={wrap_mse})")

    dropped = scrub_png_dir(pp_frames)
    print(f"[mid] island scrub dropped_px~{dropped}", flush=True)
    wrap_mse2 = frame_mse(first_png, last_png)
    if wrap_mse2 > 1.0:
        raise RuntimeError(f"mid: scrub broke start/end match (MSE={wrap_mse2})")

    tmp_webm = work / OUT_NAME
    encode_alpha_webm(pp_frames / "p_%04d.png", tmp_webm, fps=FPS)
    meta = probe_duration(tmp_webm)
    print(f"[mid] encoded {meta}", flush=True)

    first, last, webm_mse = extract_edge_frames(tmp_webm, QA, "mid")
    print(f"[mid] webm first==last MSE={webm_mse:.6f}", flush=True)
    if webm_mse > 5.0:
        raise RuntimeError(f"mid: encoded webm start/end mismatch MSE={webm_mse}")

    dest_vite = VITE / OUT_NAME
    dest_static = STATIC / OUT_NAME
    robust_copy(tmp_webm, dest_vite)
    robust_copy(tmp_webm, dest_static)
    pp_ref = RAW / "lady_idle_mid_v1_pingpong.webm"
    robust_copy(tmp_webm, pp_ref)

    shutil.rmtree(work, ignore_errors=True)

    result = {
        "name": "mid",
        "scenario": SCENARIO_ID,
        "source_frames": n,
        "pingpong_frames": total,
        "webm_mse_first_last": webm_mse,
        "png_mse_first_last": wrap_mse,
        "grade": grade_stats,
        "qa_mid": str(qa_mid),
        "tint": [TINT_R, TINT_G, TINT_B],
        "ref": ref_meta,
        **meta,
        "vite": str(dest_vite),
        "static": str(dest_static),
        "qa_first": str(first),
        "qa_last": str(last),
    }

    note = RAW / "SOURCE_SCENARIO_MID_V1.txt"
    note.write_text(
        f"MID: Scenario {SCENARIO_ID} (Pixelcut ALPHA_MODE=1 VP9, 720x1280, 16fps, 81f)\n"
        "PINGPONG: frames[0..N-1] + frames[N-2..0] (drop join dup only; start==end)\n"
        "GRADE: same as breath/move v5 (desat Rec.709 → hist-match cold clinical → cool tint).\n"
        f"  Script: tools/_build_lady_idle_mid_v1.py\n"
        f"SHIPPED: {OUT_NAME} (muted -an)\n"
        "PLAYBACK: SceneCharacter base ONLY — breath x5 → mid x1 → move x1 → repeat.\n"
        "NOT used on freegame/bonus (v6/v8 untouched).\n",
        encoding="utf-8",
    )
    summary = SRC_DIR / "build_summary_mid_v1.json"
    summary.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("\nDONE", json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
