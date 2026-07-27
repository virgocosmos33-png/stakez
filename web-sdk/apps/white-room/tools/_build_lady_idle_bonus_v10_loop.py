"""Extract last 1.23s of lady_idle_bonus_v6 into a plain forward loop clip (v10).

NO reverse / ping-pong merge — just the tail, forward only, HTML loop=true.

Why: SceneCharacter plays full v6 once (audio ON), then SWAPs to this short
clip with loop=true so we never seek the long file (async seek = hitch).

Run: python tools/_build_lady_idle_bonus_v10_loop.py
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from _post_lady_idle_alpha import robust_copy

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "lady_video"
SRC_DIR = RAW / "_bonus_v6_src"
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
OUT_NAME = "lady_idle_bonus_v10_loop.webm"
TAIL_S = 1.23
SRC_CANDIDATES = (
    VITE / "lady_idle_bonus_v6.webm",
    SRC_DIR / "bonus_src.webm",
)


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:12])}...\n{result.stderr[-2500:]}")


def main() -> None:
    src = next((p for p in SRC_CANDIDATES if p.exists()), None)
    if src is None:
        raise SystemExit(f"missing source; tried {SRC_CANDIDATES}")

    probe = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                str(src),
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    duration = float(probe["format"]["duration"])
    if duration <= TAIL_S + 0.05:
        raise SystemExit(f"source too short for tail extract: {duration}s")
    start = duration - TAIL_S
    print(
        f"[bonus_v10_loop] src={src.name} dur={duration:.3f}s ss={start:.3f} "
        f"tail={TAIL_S} (plain forward, NO reverse)",
        flush=True,
    )

    out_tmp = SRC_DIR / OUT_NAME
    SRC_DIR.mkdir(parents=True, exist_ok=True)

    # Accurate cut after decode; short GOP + force KF at n=0; keep alpha + Opus.
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-i", str(src),
            "-ss", f"{start:.3f}", "-t", f"{TAIL_S:.3f}",
            "-map", "0:v:0", "-map", "0:a:0?",
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
            str(out_tmp),
        ]
    )

    streams_meta = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "stream=codec_type,codec_name,pix_fmt,r_frame_rate",
                "-show_entries", "format=duration",
                "-of", "json",
                str(out_tmp),
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    streams = streams_meta.get("streams", [])
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    if not has_audio:
        raise SystemExit("loop clip missing audio stream")
    loop_dur = float(streams_meta["format"]["duration"])
    if abs(loop_dur - TAIL_S) > 0.2:
        raise SystemExit(f"unexpected loop duration {loop_dur} (want ~{TAIL_S})")

    vstream = next(s for s in streams if s.get("codec_type") == "video")
    rate = vstream.get("r_frame_rate") or "24/1"
    num, den = rate.split("/")
    fps = float(num) / float(den) if float(den) else 24.0

    frames_meta = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-count_frames",
                "-select_streams", "v:0",
                "-show_entries", "stream=nb_read_frames",
                "-of", "json",
                str(out_tmp),
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    n_frames = int(frames_meta["streams"][0].get("nb_read_frames") or 0)

    for dest_dir in (VITE, STATIC):
        dest_dir.mkdir(parents=True, exist_ok=True)
        robust_copy(out_tmp, dest_dir / OUT_NAME)
        print(f"[bonus_v10_loop] installed {dest_dir / OUT_NAME}", flush=True)

    summary = {
        "source": str(src),
        "source_duration_s": duration,
        "tail_start_s": start,
        "tail_s": TAIL_S,
        "mode": "plain_forward",
        "pingpong": False,
        "frames": n_frames,
        "fps": fps,
        "duration_s": round(loop_dur, 4),
        "pix_fmt": vstream.get("pix_fmt"),
        "codec": vstream.get("codec_name"),
        "has_audio": has_audio,
        "bytes": out_tmp.stat().st_size,
        "vite": str(VITE / OUT_NAME),
        "static": str(STATIC / OUT_NAME),
    }
    (SRC_DIR / "build_v10_loop_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (SRC_DIR / "SOURCE_SCENARIO_V10_LOOP.txt").write_text(
        "BONUS LOOP v10: plain forward last 1.23s of lady_idle_bonus_v6\n"
        "  Scenario master: asset_mmvxxR2qWvKd3CxSawDxw27q\n"
        "  NO reverse / ping-pong merge\n"
        f"  Duration: ~{loop_dur:.3f}s ({n_frames}f @ {fps:.0f}fps)\n"
        "  Audio: same 1.23s extract (Opus)\n"
        f"  Shipped: {OUT_NAME}\n"
        "  FE: SceneCharacter play full v6 once → SWAP to v10_loop loop=true\n",
        encoding="utf-8",
    )
    print(f"[bonus_v10_loop] DONE duration={loop_dur}s from ss={start:.3f}", flush=True)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
