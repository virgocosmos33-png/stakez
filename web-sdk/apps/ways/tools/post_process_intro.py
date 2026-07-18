"""Finish the Scenario 'enter the mirror' clips into game-ready intro videos.

- gentle fade-in at the very start (seamless continuation from the loading art)
- fade the last 0.5s down to the game's dark violet-black so the hand-off to
  the game board is invisible
- re-encode web-friendly: H.264 yuv420p high, faststart, muted, compact

In:  qa-shots/intro/intro_mirror_land.mp4 / intro_mirror_port.mp4
Out: static/assets/sprites/mirror/intro_mirror.mp4 / intro_mirror_portrait.mp4
Run: python tools/post_process_intro.py
"""

from __future__ import annotations

import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
INTRO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "qa-shots", "intro"))
MIRROR = os.path.normpath(os.path.join(HERE, "..", "static", "assets", "sprites", "mirror"))

# game background dark violet-black (matches Background.svelte / board)
END_COLOR = "0x0A0714"
FADE_IN = 0.22
FADE_OUT = 0.55

JOBS = [
    ("intro_mirror_land.mp4", "intro_mirror.mp4"),
    ("intro_mirror_port.mp4", "intro_mirror_portrait.mp4"),
]


def duration(path: str) -> float:
    p = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", path],
        capture_output=True, text=True,
    )
    info = json.loads(p.stdout)
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    return float(v.get("duration") or 5.0)


def process(src_name: str, out_name: str) -> None:
    src = os.path.join(INTRO, src_name)
    if not os.path.exists(src):
        print("skip (missing):", src)
        return
    out = os.path.join(MIRROR, out_name)
    dur = duration(src)
    st_out = max(0.0, dur - FADE_OUT)
    vf = (
        f"fade=t=in:st=0:d={FADE_IN},"
        f"fade=t=out:st={st_out:.3f}:d={FADE_OUT}:color={END_COLOR}"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", src,
            "-vf", vf,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-crf", "23", "-preset", "slow", "-movflags", "+faststart", "-an",
            out,
        ],
        check=True, capture_output=True,
    )
    mb = os.path.getsize(out) / 1e6
    print(f"wrote {out} ({mb:.1f} MB, {dur:.2f}s)")


if __name__ == "__main__":
    for src_name, out_name in JOBS:
        process(src_name, out_name)
    print("done")
