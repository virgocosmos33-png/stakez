"""Build SceneCharacter idle v5: grade-matched seamless ping-pong breath + move.

Same ping-pong contract as v4:
  frames[0..N-1] + frames[N-2..0]  -> length 2N-1, start==end (seamless).

Grade (SHARED on both clips so sequencer shades match):
  1) Desaturate opaque RGB to Rec.709 luma (sat 0).
  2) Histogram-match luma to the cold clinical reference still
     (washed asylum near-B&W, pale skin, dark hair).
  3) Recolor with the SAME cool tint ratios derived from that reference
     (B lifted vs R/G) so both clips share one LUT/tint.

Alpha: preserve Pixelcut alpha + island scrub. Encode muted VP9 yuva420p.
Cache-bust filenames: lady_idle_breath_v5.webm / lady_idle_move_v5.webm

Run: python tools/_build_lady_idle_v5_grade_match.py
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

APP = Path(__file__).resolve().parents[1]
SRC_DIR = APP / "assets-raw" / "lady_video" / "_v4_src"
RAW = APP / "assets-raw" / "lady_video"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
QA = SRC_DIR / "_qa_v5"
FPS = 24

# Cold clinical reference (user-provided still).
REF_PNG = Path(
    r"C:\Users\xheih\.cursor\projects\c-Users-xheih-OneDrive-Documents-lady-mirror-drama-studios"
    r"\assets\c__Users_xheih_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_"
    r"image-7f61c49d-ef20-407a-991b-45a0d9613bfa.png"
)

CLIPS = (
    ("breath", SRC_DIR / "breath_src.mp4", "lady_idle_breath_v5.webm"),
    ("move", SRC_DIR / "move_src.mp4", "lady_idle_move_v5.webm"),
)

# Cool tint ratios from reference mean RGB / mean luma (~141.7/146.6/156.3 over 146.3).
TINT_R = 0.969
TINT_G = 1.002
TINT_B = 1.069


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:10])}...\n{result.stderr[-2500:]}")


def luma709(rgb: np.ndarray) -> np.ndarray:
    r = rgb[..., 0].astype(np.float64)
    g = rgb[..., 1].astype(np.float64)
    b = rgb[..., 2].astype(np.float64)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cdf_from_luma(luma: np.ndarray) -> np.ndarray:
    """256-bin CDF over float/uint luma samples in [0,255]."""
    hist, _ = np.histogram(luma.clip(0, 255), bins=256, range=(0, 256))
    cdf = hist.cumsum().astype(np.float64)
    if cdf[-1] <= 0:
        return np.linspace(0.0, 1.0, 256)
    cdf /= cdf[-1]
    # Avoid flat zero leading to divide issues — enforce strict increase via eps.
    return np.maximum.accumulate(np.maximum(cdf, np.linspace(0, 1e-12, 256)))


def hist_match_lut(src_cdf: np.ndarray, tgt_cdf: np.ndarray) -> np.ndarray:
    """Map source grey level -> target grey level via CDF matching."""
    lut = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        # smallest j where tgt_cdf[j] >= src_cdf[i]
        j = int(np.searchsorted(tgt_cdf, src_cdf[i], side="left"))
        lut[i] = np.uint8(min(255, j))
    return lut


def build_ref_target() -> tuple[np.ndarray, dict]:
    if not REF_PNG.exists():
        raise SystemExit(f"missing grade reference: {REF_PNG}")
    arr = np.array(Image.open(REF_PNG).convert("RGB"), dtype=np.float64)
    h, w = arr.shape[:2]
    # Subject-ish crop (center) for pale-skin / dark-hair histogram.
    crop = arr[h // 6 : 5 * h // 6, w // 4 : 3 * w // 4]
    L = luma709(crop)
    meta = {
        "ref": str(REF_PNG),
        "mean_rgb": [float(x) for x in crop.reshape(-1, 3).mean(axis=0)],
        "mean_luma": float(L.mean()),
        "luma_p10_50_90": [float(x) for x in np.percentile(L, [10, 50, 90])],
        "tint_rgb": [TINT_R, TINT_G, TINT_B],
    }
    return cdf_from_luma(L), meta


def sample_clip_cdf(frames_dir: Path, n: int, step: int = 4) -> np.ndarray:
    samples: list[np.ndarray] = []
    for i in range(1, n + 1, step):
        p = frames_dir / f"f_{i:04d}.png"
        a = np.array(Image.open(p).convert("RGBA"))
        m = a[..., 3] > 16
        if not np.any(m):
            continue
        samples.append(luma709(a[..., :3])[m])
    if not samples:
        raise RuntimeError(f"no opaque samples in {frames_dir}")
    return cdf_from_luma(np.concatenate(samples))


def apply_grade_dir(frames_dir: Path, lut: np.ndarray) -> dict:
    """Desaturate -> hist-match via lut -> cool tint. Preserve alpha. In-place."""
    stats_before = []
    stats_after = []
    for p in sorted(frames_dir.glob("f_*.png")):
        a = np.array(Image.open(p).convert("RGBA"))
        rgb = a[..., :3].astype(np.float64)
        alpha = a[..., 3]
        m = alpha > 16
        L = luma709(rgb)
        if np.any(m):
            stats_before.append(
                (
                    float(rgb[m, 0].mean()),
                    float(rgb[m, 1].mean()),
                    float(rgb[m, 2].mean()),
                    float(L[m].mean()),
                )
            )
        L_u8 = np.clip(np.rint(L), 0, 255).astype(np.uint8)
        L_matched = lut[L_u8].astype(np.float64)
        out = np.zeros_like(rgb)
        out[..., 0] = L_matched * TINT_R
        out[..., 1] = L_matched * TINT_G
        out[..., 2] = L_matched * TINT_B
        out = np.clip(np.rint(out), 0, 255).astype(np.uint8)
        # Keep fully transparent pixels black (cleaner VP9 alpha edges).
        out[alpha == 0] = 0
        graded = np.dstack([out, alpha])
        Image.fromarray(graded).save(p)
        if np.any(m):
            Lg = luma709(out)
            stats_after.append(
                (
                    float(out[m, 0].mean()),
                    float(out[m, 1].mean()),
                    float(out[m, 2].mean()),
                    float(Lg[m].mean()),
                )
            )
    def avg(rows: list[tuple]) -> list[float]:
        if not rows:
            return [0.0, 0.0, 0.0, 0.0]
        arr = np.array(rows, dtype=np.float64)
        return [float(x) for x in arr.mean(axis=0)]

    return {"mean_rgba_luma_before": avg(stats_before), "mean_rgba_luma_after": avg(stats_after)}


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


def write_pingpong_sequence(frames_dir: Path, out_dir: Path, n: int) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in out_dir.glob("*.png"):
        p.unlink()
    order = list(range(n)) + list(range(n - 2, -1, -1))
    for i, src_i in enumerate(order, start=1):
        src = frames_dir / f"f_{src_i + 1:04d}.png"
        dst = out_dir / f"p_{i:04d}.png"
        shutil.copy2(src, dst)
    return len(order)


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


def frame_mse(a: Path, b: Path) -> float:
    aa = np.array(Image.open(a).convert("RGBA"), dtype=np.float64)
    bb = np.array(Image.open(b).convert("RGBA"), dtype=np.float64)
    return float(np.mean((aa - bb) ** 2))


def extract_edge_frames(webm: Path, qa_dir: Path, tag: str) -> tuple[Path, Path, float]:
    qa_dir.mkdir(parents=True, exist_ok=True)
    first = qa_dir / f"{tag}_first.png"
    last = qa_dir / f"{tag}_last.png"
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-i", str(webm),
            "-vf", "select=eq(n\\,0)", "-frames:v", "1", "-pix_fmt", "rgba",
            str(first),
        ]
    )
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-i", str(webm),
            "-vf", "reverse,select=eq(n\\,0)", "-frames:v", "1", "-pix_fmt", "rgba",
            str(last),
        ]
    )
    return first, last, frame_mse(first, last)


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


def build_one(name: str, src: Path, out_name: str, tgt_cdf: np.ndarray) -> dict:
    print(f"\n=== {name}: {src.name} -> {out_name} ===", flush=True)
    work = Path(tempfile.mkdtemp(prefix=f"lady_v5_{name}_"))
    raw_frames = work / "raw"
    pp_frames = work / "pp"
    n = extract_rgba_frames(src, raw_frames)
    print(f"[{name}] source frames={n}", flush=True)
    if n < 3:
        raise RuntimeError(f"{name}: need >=3 frames, got {n}")

    src_cdf = sample_clip_cdf(raw_frames, n, step=3)
    lut = hist_match_lut(src_cdf, tgt_cdf)
    grade_stats = apply_grade_dir(raw_frames, lut)
    print(f"[{name}] grade before mean RGBL={grade_stats['mean_rgba_luma_before']}", flush=True)
    print(f"[{name}] grade after  mean RGBL={grade_stats['mean_rgba_luma_after']}", flush=True)

    # Save mid-frame QA after grade (pre-pingpong)
    mid = raw_frames / f"f_{max(1, n // 2):04d}.png"
    qa_mid = QA / f"{name}_graded_mid.png"
    QA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mid, qa_mid)

    total = write_pingpong_sequence(raw_frames, pp_frames, n)
    expected = 2 * n - 1
    if total != expected:
        raise RuntimeError(f"{name}: pingpong len {total} != {expected}")
    print(f"[{name}] pingpong frames={total} (= 2*{n}-1)", flush=True)

    first_png = pp_frames / "p_0001.png"
    last_png = pp_frames / f"p_{total:04d}.png"
    wrap_mse = frame_mse(first_png, last_png)
    print(f"[{name}] png start==end MSE={wrap_mse:.6f} (want ~0)", flush=True)
    if wrap_mse > 0.5:
        raise RuntimeError(f"{name}: start/end frames do not match (MSE={wrap_mse})")

    dropped = scrub_png_dir(pp_frames)
    print(f"[{name}] island scrub dropped_px~{dropped}", flush=True)
    wrap_mse2 = frame_mse(first_png, last_png)
    if wrap_mse2 > 1.0:
        raise RuntimeError(f"{name}: scrub broke start/end match (MSE={wrap_mse2})")

    tmp_webm = work / out_name
    encode_alpha_webm(pp_frames / "p_%04d.png", tmp_webm)
    meta = probe_duration(tmp_webm)
    print(f"[{name}] encoded {meta}", flush=True)

    first, last, webm_mse = extract_edge_frames(tmp_webm, QA, name)
    print(f"[{name}] webm first==last MSE={webm_mse:.6f}", flush=True)
    if webm_mse > 5.0:
        raise RuntimeError(f"{name}: encoded webm start/end mismatch MSE={webm_mse}")

    dest_vite = VITE / out_name
    dest_static = STATIC / out_name
    robust_copy(tmp_webm, dest_vite)
    robust_copy(tmp_webm, dest_static)
    pp_ref = RAW / f"lady_idle_{name}_v5_pingpong.webm"
    robust_copy(tmp_webm, pp_ref)

    shutil.rmtree(work, ignore_errors=True)

    return {
        "name": name,
        "source_frames": n,
        "pingpong_frames": total,
        "webm_mse_first_last": webm_mse,
        "png_mse_first_last": wrap_mse,
        "grade": grade_stats,
        "qa_mid": str(qa_mid),
        **meta,
        "vite": str(dest_vite),
        "static": str(dest_static),
        "qa_first": str(first),
        "qa_last": str(last),
    }


def main() -> None:
    STATIC.mkdir(parents=True, exist_ok=True)
    VITE.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    tgt_cdf, ref_meta = build_ref_target()
    print("REF", json.dumps(ref_meta, indent=2), flush=True)

    results = []
    for name, src, out_name in CLIPS:
        if not src.exists():
            raise SystemExit(f"missing source: {src}")
        results.append(build_one(name, src, out_name, tgt_cdf))

    # Cross-clip shade check on graded mid QA frames
    b_mid = np.array(Image.open(QA / "breath_graded_mid.png").convert("RGBA"))
    m_mid = np.array(Image.open(QA / "move_graded_mid.png").convert("RGBA"))
    bm = b_mid[..., 3] > 16
    mm = m_mid[..., 3] > 16
    b_mean = luma709(b_mid[..., :3])[bm].mean() if np.any(bm) else 0.0
    m_mean = luma709(m_mid[..., :3])[mm].mean() if np.any(mm) else 0.0
    cross = {
        "breath_mid_opaque_luma": float(b_mean),
        "move_mid_opaque_luma": float(m_mean),
        "abs_luma_delta": float(abs(b_mean - m_mean)),
        "ref": ref_meta,
    }
    print("CROSS_CLIP", json.dumps(cross, indent=2), flush=True)

    note = RAW / "SOURCE_SCENARIO_V5_BREATH_MOVE.txt"
    note.write_text(
        "BREATH: Scenario asset_jDxAn1p25Vx1MfNXqZmpXHMf (Pixelcut alpha, 720x1280, 24fps)\n"
        "MOVE:   Scenario asset_7ryyhvZcpJjEh7zAmmSJ6qSo (Pixelcut alpha, 720x1280, 24fps)\n"
        "PINGPONG: frames[0..N-1] + frames[N-2..0] (drop join dup only; start==end)\n"
        "GRADE (shared): desaturate Rec.709 -> hist-match luma to cold clinical ref still\n"
        "  -> recolor with identical cool tint (R*0.969 G*1.002 B*1.069). Alpha preserved.\n"
        "  Script: tools/_build_lady_idle_v5_grade_match.py\n"
        "SHIPPED: lady_idle_breath_v5.webm + lady_idle_move_v5.webm\n"
        "PLAYBACK: SceneCharacter breath x5 then move x1, forever. Muted (-an + runtime mute).\n"
        "NOT H3 Cell Seal (that is play-full-once + loop last 3s with audio once).\n",
        encoding="utf-8",
    )
    summary = SRC_DIR / "build_summary_v5.json"
    summary.write_text(
        json.dumps({"ref": ref_meta, "cross": cross, "clips": results}, indent=2),
        encoding="utf-8",
    )
    print("\nDONE", json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
