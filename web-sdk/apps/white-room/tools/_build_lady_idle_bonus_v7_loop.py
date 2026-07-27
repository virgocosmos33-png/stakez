"""Build bonus side-character TAIL loop via seamless ping-pong (v7).

Same merge as base idle breath/move (_build_lady_idle_v4_pingpong.py):
  frames[0..N-1] + frames[N-2..0]  → length 2N-1
  Drop only the mid join duplicate; KEEP final frame == first frame
  so loop=true wrap is seamless.

Source: last TAIL_S (4.3s) of lady_idle_bonus_v6.webm
  (Scenario asset_mmvxxR2qWvKd3CxSawDxw27q master).

Audio: best-effort ping-pong of the same 4.3s extract —
  forward audio + reverse audio with join-dup frame trimmed
  so duration matches (2N-1)/fps.

Ship: lady_idle_bonus_v7_loop.webm (cache-bust).

Run: python tools/_build_lady_idle_bonus_v7_loop.py
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
RAW = APP / "assets-raw" / "lady_video"
SRC_DIR = RAW / "_bonus_v6_src"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
QA = SRC_DIR / "qa_v7_loop"
FPS = 24
TAIL_S = 4.3
OUT_NAME = "lady_idle_bonus_v7_loop.webm"
# Prefer shipped scrubbed master; fall back to raw Scenario source.
SRC_CANDIDATES = (
    VITE / "lady_idle_bonus_v6.webm",
    SRC_DIR / "bonus_src.webm",
)


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:12])}...\n{result.stderr[-2500:]}")


def frame_mse(a: Path, b: Path) -> float:
    aa = np.array(Image.open(a).convert("RGBA"), dtype=np.float64)
    bb = np.array(Image.open(b).convert("RGBA"), dtype=np.float64)
    return float(np.mean((aa - bb) ** 2))


def extract_tail_rgba(src: Path, frames_dir: Path, start: float, dur: float) -> int:
    frames_dir.mkdir(parents=True, exist_ok=True)
    for p in frames_dir.glob("*.png"):
        p.unlink()
    # Decode then cut (accurate); VP9 needs libvpx-vp9 decode.
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-i", str(src),
            "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
            "-pix_fmt", "rgba",
            str(frames_dir / "f_%04d.png"),
        ]
    )
    paths = sorted(frames_dir.glob("f_*.png"))
    if not paths:
        raise RuntimeError(f"no frames extracted from {src}")
    return len(paths)


def write_pingpong_sequence(frames_dir: Path, out_dir: Path, n: int) -> int:
    """Build seamless ping-pong: fwd all + rev without join-dup; ends on frame 0."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in out_dir.glob("*.png"):
        p.unlink()
    # indices: 0..N-1 then N-2..0  (drop only mid join dup N-1)
    order = list(range(n)) + list(range(n - 2, -1, -1))
    for i, src_i in enumerate(order, start=1):
        src = frames_dir / f"f_{src_i + 1:04d}.png"  # ffmpeg 1-based
        dst = out_dir / f"p_{i:04d}.png"
        shutil.copy2(src, dst)
    return len(order)


def scrub_png_dir(frames_dir: Path) -> int:
    total = 0
    for p in sorted(frames_dir.glob("p_*.png")):
        arr = np.array(Image.open(p).convert("RGBA"))
        cleaned, dropped = strip_detached_islands(arr)
        total += dropped
        if dropped:
            Image.fromarray(cleaned).save(p)
    return total


def extract_tail_audio_wav(src: Path, out_wav: Path, start: float, dur: float) -> None:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src),
            "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
            "-vn", "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
            str(out_wav),
        ]
    )


def build_pingpong_audio(fwd_wav: Path, out_wav: Path, n_frames: int, fps: int = FPS) -> None:
    """Forward audio + reverse half with join-dup frame trimmed → (2N-1)/fps."""
    # Drop first 1/fps of reversed audio so reverse starts at frame N-2
    # (matches dropping video frame N-1 at the mid join).
    frame_dur = 1.0 / fps
    rev_start = frame_dur
    # filter: asplit → fwd kept; reverse+atrim join dup; concat
    fc = (
        f"[0:a]asplit=2[fwd][tmp];"
        f"[tmp]areverse,atrim=start={rev_start:.6f},asetpts=PTS-STARTPTS[rev];"
        f"[fwd][rev]concat=n=2:v=0:a=1[a]"
    )
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(fwd_wav),
            "-filter_complex", fc,
            "-map", "[a]",
            "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
            str(out_wav),
        ]
    )
    expected = (2 * n_frames - 1) / fps
    # Soft-check duration via ffprobe
    meta = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json", str(out_wav),
            ],
            capture_output=True, text=True, check=True,
        ).stdout
    )
    got = float(meta["format"]["duration"])
    print(f"[audio] pingpong dur={got:.4f}s expected~{expected:.4f}s", flush=True)
    if abs(got - expected) > 0.08:
        raise RuntimeError(f"pingpong audio duration mismatch: {got} vs {expected}")


def pad_audio_to_duration(src_wav: Path, out_wav: Path, dur_s: float) -> None:
    """Pad/trim PCM so mux never truncates the last video frame."""
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src_wav),
            "-af", f"apad=whole_dur={dur_s:.6f}",
            "-t", f"{dur_s:.6f}",
            "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
            str(out_wav),
        ]
    )


def encode_alpha_webm_with_audio(
    frames_glob: str, audio_wav: Path, out_webm: Path, n_out_frames: int
) -> None:
    """Mux ping-pong frames + pre-padded PCM audio (exact video duration)."""
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


def probe(webm: Path) -> dict:
    out = subprocess.run(
        [
            "ffprobe", "-v", "error", "-count_frames",
            "-select_streams", "v:0",
            "-show_entries", "stream=nb_read_frames,r_frame_rate,duration,pix_fmt,codec_name",
            "-show_entries", "format=duration",
            "-of", "json", str(webm),
        ],
        capture_output=True, text=True, check=True,
    ).stdout
    data = json.loads(out)
    st = data["streams"][0]
    num, den = st["r_frame_rate"].split("/")
    fps = float(num) / float(den)
    n = int(st.get("nb_read_frames") or 0)
    dur = n / fps if fps else float(data["format"]["duration"])
    has_audio = any(
        s.get("codec_type") == "audio"
        for s in json.loads(
            subprocess.run(
                [
                    "ffprobe", "-v", "error",
                    "-show_entries", "stream=codec_type,codec_name",
                    "-of", "json", str(webm),
                ],
                capture_output=True, text=True, check=True,
            ).stdout
        ).get("streams", [])
    )
    return {
        "frames": n,
        "fps": fps,
        "duration_s": round(dur, 4),
        "format_duration_s": round(float(data["format"]["duration"]), 4),
        "pix_fmt": st.get("pix_fmt"),
        "codec": st.get("codec_name"),
        "has_audio": has_audio,
        "bytes": webm.stat().st_size,
    }


def main() -> None:
    src = next((p for p in SRC_CANDIDATES if p.exists()), None)
    if src is None:
        raise SystemExit(f"missing source; tried {SRC_CANDIDATES}")

    probe_fmt = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json", str(src),
            ],
            capture_output=True, text=True, check=True,
        ).stdout
    )
    duration = float(probe_fmt["format"]["duration"])
    if duration <= TAIL_S + 0.05:
        raise SystemExit(f"source too short for tail extract: {duration}s")
    start = duration - TAIL_S
    print(f"[bonus_v7_loop] src={src.name} dur={duration:.3f}s ss={start:.3f} tail={TAIL_S}", flush=True)

    work = Path(tempfile.mkdtemp(prefix="lady_bonus_v7_loop_"))
    raw_frames = work / "raw"
    pp_frames = work / "pp"
    fwd_wav = work / "tail_fwd.wav"
    pp_wav = work / "tail_pp.wav"
    tmp_webm = work / OUT_NAME

    try:
        n = extract_tail_rgba(src, raw_frames, start, TAIL_S)
        print(f"[bonus_v7_loop] tail frames={n}", flush=True)
        if n < 3:
            raise RuntimeError(f"need >=3 frames, got {n}")

        src_mse = frame_mse(raw_frames / "f_0001.png", raw_frames / f"f_{n:04d}.png")
        print(f"[bonus_v7_loop] tail first-vs-last MSE={src_mse:.4f}", flush=True)

        total = write_pingpong_sequence(raw_frames, pp_frames, n)
        expected = 2 * n - 1
        if total != expected:
            raise RuntimeError(f"pingpong len {total} != {expected}")
        print(f"[bonus_v7_loop] pingpong frames={total} (= 2*{n}-1)", flush=True)

        first_png = pp_frames / "p_0001.png"
        last_png = pp_frames / f"p_{total:04d}.png"
        wrap_mse = frame_mse(first_png, last_png)
        mid_join_a = pp_frames / f"p_{n:04d}.png"
        mid_join_b = pp_frames / f"p_{n + 1:04d}.png"
        join_mse = frame_mse(mid_join_a, mid_join_b)
        print(f"[bonus_v7_loop] png start==end MSE={wrap_mse:.6f} (want ~0)", flush=True)
        print(f"[bonus_v7_loop] png join adjacent MSE={join_mse:.4f} (want >0)", flush=True)
        if wrap_mse > 0.5:
            raise RuntimeError(f"start/end frames do not match (MSE={wrap_mse})")

        dropped = scrub_png_dir(pp_frames)
        print(f"[bonus_v7_loop] island scrub dropped_px~{dropped}", flush=True)
        wrap_mse2 = frame_mse(first_png, last_png)
        if wrap_mse2 > 1.0:
            raise RuntimeError(f"scrub broke start/end match (MSE={wrap_mse2})")

        # Audio: same 4.3s window, then fwd + rev (join-dup frame trimmed).
        extract_tail_audio_wav(src, fwd_wav, start, TAIL_S)
        # Align fwd audio length to exact N frames before reverse-merge.
        aligned = work / "tail_fwd_aligned.wav"
        run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(fwd_wav),
                "-t", f"{n / FPS:.6f}",
                "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
                str(aligned),
            ]
        )
        build_pingpong_audio(aligned, pp_wav, n)
        video_dur = total / FPS
        pp_wav_exact = work / "tail_pp_exact.wav"
        pad_audio_to_duration(pp_wav, pp_wav_exact, video_dur)

        encode_alpha_webm_with_audio(
            str(pp_frames / "p_%04d.png"), pp_wav_exact, tmp_webm, total
        )
        meta = probe(tmp_webm)
        print(f"[bonus_v7_loop] encoded {meta}", flush=True)
        if not meta["has_audio"]:
            raise RuntimeError("loop clip missing audio stream")
        # Allow ±1 frame probe jitter; refuse larger drops (would break start==end).
        if abs(meta["frames"] - total) > 1:
            raise RuntimeError(f"encoded frames {meta['frames']} != pingpong {total}")
        if meta["frames"] < total:
            print(
                f"[bonus_v7_loop] WARN probe frames={meta['frames']} < {total}; "
                "relying on start==end MSE gate",
                flush=True,
            )

        first, last, webm_mse = extract_edge_frames(tmp_webm, QA, "bonus_v7_loop")
        print(f"[bonus_v7_loop] webm first==last MSE={webm_mse:.6f}", flush=True)
        if webm_mse > 5.0:
            raise RuntimeError(f"encoded webm start/end mismatch MSE={webm_mse}")

        for dest_dir in (VITE, STATIC):
            dest_dir.mkdir(parents=True, exist_ok=True)
            robust_copy(tmp_webm, dest_dir / OUT_NAME)
            print(f"[bonus_v7_loop] installed {dest_dir / OUT_NAME}", flush=True)

        ref = RAW / OUT_NAME
        robust_copy(tmp_webm, ref)

        summary = {
            "source": str(src),
            "source_duration_s": duration,
            "tail_start_s": start,
            "tail_s": TAIL_S,
            "source_frames": n,
            "pingpong_frames": total,
            "png_mse_first_last": wrap_mse,
            "webm_mse_first_last": webm_mse,
            "qa_first": str(first),
            "qa_last": str(last),
            "vite": str(VITE / OUT_NAME),
            "static": str(STATIC / OUT_NAME),
            **meta,
        }
        (SRC_DIR / "build_v7_loop_summary.json").write_text(
            json.dumps(summary, indent=2), encoding="utf-8"
        )
        note = SRC_DIR / "SOURCE_SCENARIO_V7_LOOP.txt"
        note.write_text(
            "BONUS LOOP v7: ping-pong of last 4.3s of lady_idle_bonus_v6\n"
            "  Scenario master: asset_mmvxxR2qWvKd3CxSawDxw27q\n"
            f"  Merge: frames[0..N-1]+[N-2..0] = 2N-1  (N={n} → {total}f)\n"
            f"  Duration: ~{meta['duration_s']}s @ {FPS}fps\n"
            "  Audio: fwd + rev of same 4.3s extract (join-dup frame trimmed)\n"
            f"  Shipped: {OUT_NAME}\n"
            "  FE: SceneCharacter play full v6 once → SWAP to v7_loop loop=true\n",
            encoding="utf-8",
        )
        print("\nDONE", json.dumps(summary, indent=2), flush=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
