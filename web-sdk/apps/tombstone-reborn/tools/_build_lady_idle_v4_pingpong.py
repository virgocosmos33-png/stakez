"""Build SceneCharacter idle v4: seamless baked ping-pong breath + move.

Definition of 1 loop = one forward+reverse cycle baked into a single file.

Ping-pong merge (CRITICAL):
  frames[0..N-1] + frames[N-2..0]
  - Drop only the join duplicate (forward last == reverse first)
  - KEEP final frame == first frame so loop=true / ended→replay wrap is seamless
  Length = 2N - 1

Sources already have Pixelcut alpha (ALPHA_MODE=1). Preserve alpha; scrub islands;
encode VP9 yuva420p. Install cache-busted v4 filenames.

Run: python tools/_build_lady_idle_v4_pingpong.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

# Reuse island scrub from existing lady idle post
from _post_lady_idle_alpha import MIN_ISLAND, robust_copy, strip_detached_islands

APP = Path(__file__).resolve().parents[1]
SRC_DIR = APP / "assets-raw" / "lady_video" / "_v4_src"
RAW = APP / "assets-raw" / "lady_video"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
QA = SRC_DIR / "_qa"
FPS = 24

CLIPS = (
    ("breath", SRC_DIR / "breath_src.mp4", "lady_idle_breath_v4.webm"),
    ("move", SRC_DIR / "move_src.mp4", "lady_idle_move_v4.webm"),
)


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
    # last frame via reverse select
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


def build_one(name: str, src: Path, out_name: str) -> dict:
    print(f"\n=== {name}: {src.name} -> {out_name} ===", flush=True)
    work = Path(tempfile.mkdtemp(prefix=f"lady_v4_{name}_"))
    raw_frames = work / "raw"
    pp_frames = work / "pp"
    n = extract_rgba_frames(src, raw_frames)
    print(f"[{name}] source frames={n}", flush=True)
    if n < 3:
        raise RuntimeError(f"{name}: need >=3 frames, got {n}")

    # Verify source first != last (ping-pong needed) — informational
    src_mse = frame_mse(raw_frames / "f_0001.png", raw_frames / f"f_{n:04d}.png")
    print(f"[{name}] source first-vs-last MSE={src_mse:.4f}", flush=True)

    total = write_pingpong_sequence(raw_frames, pp_frames, n)
    expected = 2 * n - 1
    if total != expected:
        raise RuntimeError(f"{name}: pingpong len {total} != {expected}")
    print(f"[{name}] pingpong frames={total} (= 2*{n}-1)", flush=True)

    # Continuity on PNG sequence before encode
    first_png = pp_frames / "p_0001.png"
    last_png = pp_frames / f"p_{total:04d}.png"
    mid_join_a = pp_frames / f"p_{n:04d}.png"          # last of forward = src N
    mid_join_b = pp_frames / f"p_{n + 1:04d}.png"      # first of reverse = src N-1
    wrap_mse = frame_mse(first_png, last_png)
    # join should NOT be identical (we dropped the dup); adjacent should be N and N-1
    join_mse = frame_mse(mid_join_a, mid_join_b)
    print(f"[{name}] png start==end MSE={wrap_mse:.6f} (want ~0)", flush=True)
    print(f"[{name}] png join adjacent MSE={join_mse:.4f} (want >0 — no doubled end)", flush=True)
    if wrap_mse > 0.5:
        raise RuntimeError(f"{name}: start/end frames do not match (MSE={wrap_mse})")

    dropped = scrub_png_dir(pp_frames)
    print(f"[{name}] island scrub dropped_px~{dropped}", flush=True)

    # re-check wrap after scrub (scrub should be symmetric enough; verify)
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
    # keep intermediate pingpong reference
    pp_ref = RAW / f"lady_idle_{name}_v4_pingpong.webm"
    robust_copy(tmp_webm, pp_ref)

    # cleanup work
    shutil.rmtree(work, ignore_errors=True)

    return {
        "name": name,
        "source_frames": n,
        "pingpong_frames": total,
        "webm_mse_first_last": webm_mse,
        "png_mse_first_last": wrap_mse,
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
    results = []
    for name, src, out_name in CLIPS:
        if not src.exists():
            raise SystemExit(f"missing source: {src}")
        results.append(build_one(name, src, out_name))

    note = RAW / "SOURCE_SCENARIO_V4_BREATH_MOVE.txt"
    note.write_text(
        "BREATH: Scenario asset_jDxAn1p25Vx1MfNXqZmpXHMf (Pixelcut alpha webm, 720x1280, 24fps, 120f, ~5s)\n"
        "MOVE:   Scenario asset_7ryyhvZcpJjEh7zAmmSJ6qSo (Pixelcut alpha webm, 720x1280, 24fps, 168f, ~7s)\n"
        "PINGPONG: frames[0..N-1] + frames[N-2..0]  (drop join dup only; start==end for wrap)\n"
        "  breath: 120 -> 239 frames (~9.958s)  |  move: 168 -> 335 frames (~13.958s)\n"
        "ALPHA: preserve Pixelcut alpha + island scrub (_post_lady_idle_alpha.strip_detached_islands)\n"
        "SHIPPED: lady_idle_breath_v4.webm + lady_idle_move_v4.webm\n"
        "PLAYBACK: SceneCharacter plays breath x5 (each ended = 1 ping-pong loop), then move x1, repeat.\n"
        "MUTE: SceneCharacter forces muted; encodes are -an.\n",
        encoding="utf-8",
    )
    summary = RAW / "_v4_src" / "build_summary.json"
    summary.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("\nDONE", json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
