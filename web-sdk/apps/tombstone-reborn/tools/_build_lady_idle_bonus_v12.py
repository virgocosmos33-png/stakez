"""Build SceneCharacter BONUS idle v12: graded A↔Arev intro + C ping-pong loop.

Scenario sources (Pixelcut alpha VP9 + Opus) — reuse _bonus_v11_src downloads:
  A: asset_mmvxxR2qWvKd3CxSawDxw27q
  C: asset_tS51AF1KczZ2EVyB1ft1WW6K
  (B dropped — no asset_9ApXR9xunajaKPLpEPxnTZHc)

Sequence:
  intro = A fwd + A rev (drop peak dup at join)  → length 2*Na-1, start==end==A[0]
  loop  = C ping-pong [0..N-1]+[N-2..0]         → length 2*Nc-1, start==end

Grade (SHARED pipeline with base idle v5 / scene_bg_v5):
  1) Desaturate opaque RGB to Rec.709 luma (sat 0)
  2) Histogram-match luma CDF to cold clinical reference still
  3) Recolor with cool tint R*0.969 G*1.002 B*1.069
Applied to A and C frames BEFORE concat so bonus doesn't shade-shift vs base.

FE: SceneCharacter plays intro once (audio ON), then SWAPs to loop clip
(audio ON). Dual-clip handoff — no seek on the intro. Base breath/mid/move
unchanged.

Run: python tools/_build_lady_idle_bonus_v12.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from _build_lady_idle_v5_grade_match import (  # noqa: E402
    TINT_B,
    TINT_G,
    TINT_R,
    apply_grade_dir,
    build_ref_target,
    hist_match_lut,
    sample_clip_cdf,
)
from _post_lady_idle_alpha import MIN_ISLAND, robust_copy, strip_detached_islands

APP = Path(__file__).resolve().parents[1]
SRC_DIR = APP / "assets-raw" / "lady_video" / "_bonus_v12_src"
V11_SRC = APP / "assets-raw" / "lady_video" / "_bonus_v11_src"
RAW = APP / "assets-raw" / "lady_video"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
QA = SRC_DIR / "qa"
FPS = 24
INTRO_NAME = "lady_idle_bonus_v12_intro.webm"
LOOP_NAME = "lady_idle_bonus_v12_loop.webm"

SCENARIO = {
    "A": "asset_mmvxxR2qWvKd3CxSawDxw27q",
    "C": "asset_tS51AF1KczZ2EVyB1ft1WW6K",
}
SRC_FILES = {
    "A": SRC_DIR / "A_src.webm",
    "C": SRC_DIR / "C_src.webm",
}


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:12])}...\n{result.stderr[-2500:]}")


def ensure_sources() -> None:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    for key in ("A", "C"):
        dest = SRC_FILES[key]
        if dest.exists():
            continue
        legacy = V11_SRC / f"{key}_src.webm"
        if legacy.exists():
            shutil.copy2(legacy, dest)
            print(f"[v12] reused {legacy.name} -> {dest}", flush=True)
        else:
            raise SystemExit(f"missing source {key}: {dest} (and no v11 fallback {legacy})")


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


def scrub_frames(frames_dir: Path, pattern: str = "f_*.png") -> int:
    total = 0
    for p in sorted(frames_dir.glob(pattern)):
        arr = np.array(Image.open(p).convert("RGBA"))
        cleaned, dropped = strip_detached_islands(arr)
        total += dropped
        if dropped:
            Image.fromarray(cleaned).save(p)
    return total


def extract_audio_wav(src: Path, out_wav: Path) -> None:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src),
            "-vn", "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
            str(out_wav),
        ]
    )


def reverse_audio_drop_peak(fwd_wav: Path, out_wav: Path, n_frames: int) -> None:
    """Reverse clip audio and drop first 1/fps so reverse starts at frame N-2."""
    frame_dur = 1.0 / FPS
    expected = (n_frames - 1) / FPS
    fc = (
        f"[0:a]areverse,atrim=start={frame_dur:.6f},asetpts=PTS-STARTPTS,"
        f"apad=whole_dur={expected:.6f}[a]"
    )
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(fwd_wav),
            "-filter_complex", fc,
            "-map", "[a]",
            "-t", f"{expected:.6f}",
            "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
            str(out_wav),
        ]
    )


def trim_audio_to_frames(fwd_wav: Path, out_wav: Path, n_frames: int) -> None:
    dur = n_frames / FPS
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(fwd_wav),
            "-af", f"apad=whole_dur={dur:.6f}",
            "-t", f"{dur:.6f}",
            "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
            str(out_wav),
        ]
    )


def concat_wavs(parts: list[Path], out_wav: Path) -> None:
    lst = out_wav.with_suffix(".txt")
    lst.write_text(
        "".join(f"file '{p.resolve().as_posix()}'\n" for p in parts),
        encoding="utf-8",
    )
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(lst),
            "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
            str(out_wav),
        ]
    )


def build_pingpong_audio(fwd_wav: Path, out_wav: Path, n_frames: int) -> None:
    """Forward + reverse half with join-dup frame trimmed → (2N-1)/fps."""
    frame_dur = 1.0 / FPS
    expected = (2 * n_frames - 1) / FPS
    fc = (
        f"[0:a]asplit=2[fwd][tmp];"
        f"[tmp]areverse,atrim=start={frame_dur:.6f},asetpts=PTS-STARTPTS[rev];"
        f"[fwd][rev]concat=n=2:v=0:a=1,apad=whole_dur={expected:.6f}[a]"
    )
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(fwd_wav),
            "-filter_complex", fc,
            "-map", "[a]",
            "-t", f"{expected:.6f}",
            "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
            str(out_wav),
        ]
    )


def copy_frame_order(
    src_dirs: dict[str, Path],
    counts: dict[str, int],
    order: list[tuple[str, int]],
    out_dir: Path,
) -> int:
    """Copy (clip_key, 0-based index) frames into out_dir as p_XXXX.png."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in out_dir.glob("*.png"):
        p.unlink()
    for i, (key, src_i) in enumerate(order, start=1):
        n = counts[key]
        if src_i < 0 or src_i >= n:
            raise RuntimeError(f"bad index {key}[{src_i}] n={n}")
        src = src_dirs[key] / f"f_{src_i + 1:04d}.png"
        dst = out_dir / f"p_{i:04d}.png"
        shutil.copy2(src, dst)
    return len(order)


def encode_alpha_webm_with_audio(
    frames_glob: str, audio_wav: Path, out_webm: Path, n_out_frames: int
) -> None:
    out_webm.parent.mkdir(parents=True, exist_ok=True)
    video_dur = n_out_frames / FPS
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS),
            "-i", frames_glob,
            "-i", str(audio_wav),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuva420p",
            "-b:v", "0",
            "-crf", "28",
            "-auto-alt-ref", "0",
            "-g", "12",
            "-keyint_min", "12",
            "-force_key_frames", "expr:eq(n,0)",
            "-c:a", "libopus",
            "-b:a", "128k",
            "-t", f"{video_dur:.6f}",
            str(out_webm),
        ]
    )


def probe_webm(webm: Path) -> dict:
    meta = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-count_frames",
                "-show_entries", "stream=codec_type,codec_name,pix_fmt,r_frame_rate,nb_read_frames",
                "-show_entries", "format=duration",
                "-of", "json",
                str(webm),
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    streams = meta.get("streams", [])
    v = next(s for s in streams if s.get("codec_type") == "video")
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    rate = v.get("r_frame_rate") or "24/1"
    num, den = rate.split("/")
    fps = float(num) / float(den) if float(den) else float(FPS)
    n = int(v.get("nb_read_frames") or 0)
    return {
        "frames": n,
        "fps": fps,
        "duration_s": round(float(meta["format"]["duration"]), 4),
        "pix_fmt": v.get("pix_fmt"),
        "codec": v.get("codec_name"),
        "has_audio": has_audio,
        "bytes": webm.stat().st_size,
    }


def qa_alpha(webm: Path, ss: str, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-ss", ss, "-i", str(webm),
            "-frames:v", "1", "-pix_fmt", "rgba", str(dest),
        ]
    )
    a = np.array(Image.open(dest).convert("RGBA"))[..., 3]
    n, _, stats, _ = cv2.connectedComponentsWithStats((a > 24).astype(np.uint8), 8)
    extras = []
    if n > 1:
        main_i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        extras = [
            int(stats[i, cv2.CC_STAT_AREA])
            for i in range(1, n)
            if i != main_i and int(stats[i, cv2.CC_STAT_AREA]) >= MIN_ISLAND
        ]
    return {
        "ss": ss,
        "frac0": float((a < 8).mean()),
        "opaque": float((a > 200).mean()),
        "extras": extras,
    }


def frame_mse(a: Path, b: Path) -> float:
    xa = np.array(Image.open(a).convert("RGBA"), dtype=np.float32)
    xb = np.array(Image.open(b).convert("RGBA"), dtype=np.float32)
    return float(np.mean((xa - xb) ** 2))


def main() -> None:
    ensure_sources()
    for key, path in SRC_FILES.items():
        if not path.exists():
            raise SystemExit(f"missing source {key}: {path}")

    work = Path(tempfile.mkdtemp(prefix="lady_bonus_v12_"))
    QA.mkdir(parents=True, exist_ok=True)
    STATIC.mkdir(parents=True, exist_ok=True)
    VITE.mkdir(parents=True, exist_ok=True)

    tgt_cdf, ref_meta = build_ref_target()
    print("[v12] REF", json.dumps(ref_meta, indent=2), flush=True)
    print(
        f"[v12] grade tint R*{TINT_R} G*{TINT_G} B*{TINT_B} (same as base idle v5)",
        flush=True,
    )

    frame_dirs: dict[str, Path] = {}
    counts: dict[str, int] = {}
    grade_stats: dict[str, dict] = {}
    for key in ("A", "C"):
        d = work / f"frames_{key}"
        print(f"[v12] extract {key} {SRC_FILES[key].name}", flush=True)
        n = extract_rgba_frames(SRC_FILES[key], d)
        if n < 3:
            raise RuntimeError(f"{key}: need >=3 frames, got {n}")
        sample = np.array(Image.open(d / f"f_{max(1, n // 2):04d}.png").convert("RGBA"))
        frac0 = float((sample[..., 3] < 8).mean())
        print(f"[v12] {key} frames={n} mid_frac0={frac0:.4f}", flush=True)
        if frac0 < 0.15:
            raise RuntimeError(f"{key}: alpha key failed (frac0={frac0})")
        dropped = scrub_frames(d)
        print(f"[v12] {key} scrub dropped_island_px~{dropped}", flush=True)

        src_cdf = sample_clip_cdf(d, n, step=3)
        lut = hist_match_lut(src_cdf, tgt_cdf)
        gstats = apply_grade_dir(d, lut)
        grade_stats[key] = gstats
        print(f"[v12] {key} grade before mean RGBL={gstats['mean_rgba_luma_before']}", flush=True)
        print(f"[v12] {key} grade after  mean RGBL={gstats['mean_rgba_luma_after']}", flush=True)
        mid = d / f"f_{max(1, n // 2):04d}.png"
        shutil.copy2(mid, QA / f"{key}_graded_mid.png")

        frame_dirs[key] = d
        counts[key] = n

    na, nc = counts["A"], counts["C"]

    # Intro: A fwd + A rev (N-2..0) — drop peak dup at join; start==end==A[0]
    intro_order: list[tuple[str, int]] = (
        [("A", i) for i in range(na)]
        + [("A", i) for i in range(na - 2, -1, -1)]
    )
    expected_intro = 2 * na - 1
    if len(intro_order) != expected_intro:
        raise RuntimeError(f"intro order len {len(intro_order)} != {expected_intro}")

    intro_frames = work / "intro_frames"
    n_intro = copy_frame_order(frame_dirs, counts, intro_order, intro_frames)
    first_intro = intro_frames / "p_0001.png"
    last_intro = intro_frames / f"p_{n_intro:04d}.png"
    intro_wrap = frame_mse(first_intro, last_intro)
    print(
        f"[v12] intro frames={n_intro} (~{n_intro / FPS:.3f}s) start==end MSE={intro_wrap:.6f}",
        flush=True,
    )
    if intro_wrap > 0.5:
        raise RuntimeError(f"intro start/end mismatch MSE={intro_wrap}")

    # C ping-pong
    loop_order: list[tuple[str, int]] = (
        [("C", i) for i in range(nc)]
        + [("C", i) for i in range(nc - 2, -1, -1)]
    )
    expected_loop = 2 * nc - 1
    loop_frames = work / "loop_frames"
    n_loop = copy_frame_order(frame_dirs, counts, loop_order, loop_frames)
    if n_loop != expected_loop:
        raise RuntimeError(f"loop frames {n_loop} != {expected_loop}")
    first_loop = loop_frames / "p_0001.png"
    last_loop = loop_frames / f"p_{n_loop:04d}.png"
    wrap_mse = frame_mse(first_loop, last_loop)
    print(f"[v12] C pingpong frames={n_loop} start==end MSE={wrap_mse:.6f}", flush=True)
    if wrap_mse > 0.5:
        raise RuntimeError(f"C pingpong start/end mismatch MSE={wrap_mse}")

    # Audio
    print("[v12] build audio beds", flush=True)
    wav_a = work / "A.wav"
    wav_c = work / "C.wav"
    extract_audio_wav(SRC_FILES["A"], wav_a)
    extract_audio_wav(SRC_FILES["C"], wav_c)

    a_fwd = work / "A_fwd.wav"
    a_rev = work / "A_rev.wav"
    trim_audio_to_frames(wav_a, a_fwd, na)
    reverse_audio_drop_peak(wav_a, a_rev, na)

    intro_wav = work / "intro.wav"
    concat_wavs([a_fwd, a_rev], intro_wav)
    intro_audio_meta = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json", str(intro_wav),
            ],
            capture_output=True, text=True, check=True,
        ).stdout
    )
    intro_audio_dur = float(intro_audio_meta["format"]["duration"])
    intro_video_dur = n_intro / FPS
    print(
        f"[v12] intro audio={intro_audio_dur:.4f}s video={intro_video_dur:.4f}s",
        flush=True,
    )
    if abs(intro_audio_dur - intro_video_dur) > 0.08:
        raise RuntimeError(
            f"intro A/V duration mismatch: audio={intro_audio_dur} video={intro_video_dur}"
        )

    loop_wav = work / "loop.wav"
    build_pingpong_audio(wav_c, loop_wav, nc)

    # Encode
    intro_tmp = work / INTRO_NAME
    loop_tmp = work / LOOP_NAME
    print("[v12] encode intro", flush=True)
    encode_alpha_webm_with_audio(
        str(intro_frames / "p_%04d.png"), intro_wav, intro_tmp, n_intro
    )
    print("[v12] encode loop", flush=True)
    encode_alpha_webm_with_audio(
        str(loop_frames / "p_%04d.png"), loop_wav, loop_tmp, n_loop
    )

    intro_meta = probe_webm(intro_tmp)
    loop_meta = probe_webm(loop_tmp)
    print(f"[v12] intro probe {intro_meta}", flush=True)
    print(f"[v12] loop probe {loop_meta}", flush=True)
    if not intro_meta["has_audio"] or not loop_meta["has_audio"]:
        raise SystemExit("v12 encode missing audio stream")
    if abs(intro_meta["frames"] - n_intro) > 2:
        raise SystemExit(f"intro frame count {intro_meta['frames']} != {n_intro}")
    if abs(loop_meta["frames"] - n_loop) > 2:
        raise SystemExit(f"loop frame count {loop_meta['frames']} != {n_loop}")

    for ss, tag in (
        ("0.25", "start"),
        (f"{intro_video_dur / 2:.2f}", "mid"),
        (f"{max(0.1, intro_video_dur - 0.3):.2f}", "tail"),
    ):
        info = qa_alpha(intro_tmp, ss, QA / f"intro_{tag}.png")
        print(f"[v12] intro qa @{ss}s {info}", flush=True)
        if info["extras"]:
            raise SystemExit(f"intro floating islands @{ss}s: {info['extras']}")
        if info["frac0"] < 0.2:
            raise SystemExit(f"intro alpha key failed @{ss}s")

    for ss, tag in (
        ("0.25", "start"),
        (f"{(n_loop / FPS) / 2:.2f}", "mid"),
        (f"{max(0.1, n_loop / FPS - 0.25):.2f}", "tail"),
    ):
        info = qa_alpha(loop_tmp, ss, QA / f"loop_{tag}.png")
        print(f"[v12] loop qa @{ss}s {info}", flush=True)
        if info["extras"]:
            raise SystemExit(f"loop floating islands @{ss}s: {info['extras']}")
        if info["frac0"] < 0.2:
            raise SystemExit(f"loop alpha key failed @{ss}s")

    for dest_dir in (VITE, STATIC):
        robust_copy(intro_tmp, dest_dir / INTRO_NAME)
        robust_copy(loop_tmp, dest_dir / LOOP_NAME)
        print(f"[v12] installed {dest_dir / INTRO_NAME}", flush=True)
        print(f"[v12] installed {dest_dir / LOOP_NAME}", flush=True)

    robust_copy(intro_tmp, RAW / INTRO_NAME.replace(".webm", "_ship.webm"))
    robust_copy(loop_tmp, RAW / LOOP_NAME.replace(".webm", "_ship.webm"))

    summary = {
        "scenario": SCENARIO,
        "dropped": "B asset_9ApXR9xunajaKPLpEPxnTZHc (not in v12)",
        "fps": FPS,
        "source_frames": counts,
        "grade": {
            "pipeline": "Rec.709 desat -> hist-match clinical ref -> tint R*0.969 G*1.002 B*1.069",
            "shared_with": "lady_idle_breath_v5 / lady_idle_move_v5 / scene_bg_v5",
            "ref": ref_meta,
            "clips": grade_stats,
        },
        "sequence": "A_fwd -> A_rev -> C_pingpong_loop",
        "intro": {
            "file": INTRO_NAME,
            "frames": n_intro,
            "duration_s": round(intro_video_dur, 4),
            "join_drops": "A peak (N-1) at A|Arev join only",
            "wrap_mse": intro_wrap,
            **intro_meta,
        },
        "loop": {
            "file": LOOP_NAME,
            "frames": n_loop,
            "duration_s": round(n_loop / FPS, 4),
            "pingpong": True,
            "wrap_mse": wrap_mse,
            **loop_meta,
        },
        "vite_intro": str(VITE / INTRO_NAME),
        "vite_loop": str(VITE / LOOP_NAME),
        "static_intro": str(STATIC / INTRO_NAME),
        "static_loop": str(STATIC / LOOP_NAME),
    }
    (SRC_DIR / "build_v12_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (SRC_DIR / "SOURCE_SCENARIO_BONUS_V12.txt").write_text(
        "BONUS SIDE CHARACTER v12 (freegame only)\n"
        f"  A: {SCENARIO['A']}\n"
        f"  C: {SCENARIO['C']}\n"
        "  B: DROPPED (not in this version)\n"
        "Sequence: A fwd -> A rev -> then C pingpong forever\n"
        "Grade: Rec.709 desat -> hist-match clinical ref -> tint R*0.969 G*1.002 B*1.069\n"
        "  (same as lady_idle_breath_v5 / move_v5 / scene_bg_v5)\n"
        f"Intro: {INTRO_NAME}  (~{intro_video_dur:.2f}s, {n_intro}f @ {FPS}fps)\n"
        f"Loop:  {LOOP_NAME}  (~{n_loop / FPS:.2f}s ping-pong, {n_loop}f)\n"
        "Audio ON (Opus). Dual-clip SWAP in SceneCharacter — no long-file seek.\n"
        "Base breath/mid/move sequencer unchanged.\n"
        "Sources reused from _bonus_v11_src/{A,C}_src.webm.\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2), flush=True)
    print("[v12] DONE", flush=True)
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
