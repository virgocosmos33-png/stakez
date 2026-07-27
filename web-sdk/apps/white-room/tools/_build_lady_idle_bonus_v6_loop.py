"""Extract last 4.3s of lady_idle_bonus_v6 into a short loop clip.

Why: SceneCharacter used to seek the long webm to duration-TAIL on ended —
async seek + keyframe snap = visible hitch. Short clip with keyframe at
frame 0 + HTML loop (or cheap seek-to-0) avoids that.

Run: python tools/_build_lady_idle_bonus_v6_loop.py
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from _post_lady_idle_alpha import robust_copy

APP = Path(__file__).resolve().parents[1]
STATIC = APP / "static" / "assets" / "sprites" / "scene"
VITE = APP / "assets" / "sprites" / "scene"
SRC = VITE / "lady_idle_bonus_v6.webm"
OUT_NAME = "lady_idle_bonus_v6_loop.webm"
TAIL_S = 4.3


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:12])}...\n{result.stderr[-2500:]}")


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing source: {SRC}")

    probe = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                str(SRC),
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

    out_tmp = APP / "assets-raw" / "lady_video" / OUT_NAME
    out_tmp.parent.mkdir(parents=True, exist_ok=True)

    # Accurate cut after decode; short GOP + force KF at n=0; keep alpha + Opus.
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9", "-i", str(SRC),
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

    meta = json.loads(
        subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "stream=codec_type,codec_name",
                "-show_entries", "format=duration",
                "-of", "json",
                str(out_tmp),
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    has_audio = any(s.get("codec_type") == "audio" for s in meta.get("streams", []))
    if not has_audio:
        raise SystemExit("loop clip missing audio stream")
    loop_dur = float(meta["format"]["duration"])
    if abs(loop_dur - TAIL_S) > 0.15:
        raise SystemExit(f"unexpected loop duration {loop_dur}")

    for dest_dir in (VITE, STATIC):
        robust_copy(out_tmp, dest_dir / OUT_NAME)
        print(f"[bonus_v6_loop] installed {dest_dir / OUT_NAME}", flush=True)
    print(f"[bonus_v6_loop] DONE duration={loop_dur}s from ss={start:.3f}", flush=True)


if __name__ == "__main__":
    main()
