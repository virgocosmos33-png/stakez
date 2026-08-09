"""Normalize generated wild-reel videos to the reference framing.

Veo insets the padded cell inside black bands on all four sides; the game
cover-fits the video to the reel column HEIGHT, so top/bottom black would show
in-game. This detects the content box (ffmpeg cropdetect), crops to the content
height, rescales to exactly 1080x1920 with the cell horizontally centered, and
copies the audio track through untouched.

Usage:
    python tools/normalize_wild_reel_videos.py h1 h2 h4 h5
"""

import re
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).parent / "scenario_out"
W, H = 1080, 1920


def content_box(src: Path) -> tuple[int, int, int, int]:
    """(x1, y1, w, h) of the non-black region, from cropdetect's last report."""
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(src), "-vf", "cropdetect=limit=24:round=2",
         "-frames:v", "90", "-f", "null", "NUL"],
        capture_output=True, text=True, check=False,
    )
    matches = re.findall(r"x1:(\d+) x2:(\d+) y1:(\d+) y2:(\d+)", result.stderr)
    if not matches:
        raise SystemExit(f"{src.name}: cropdetect found nothing")
    x1, x2, y1, y2 = map(int, matches[-1])
    return x1, y1, x2 - x1 + 1, y2 - y1 + 1


def normalize(key: str) -> Path:
    src = OUT / f"wr_reel_{key}.mp4"
    dest = OUT / f"wr_reel_{key}_norm.mp4"
    x1, y1, cw, ch = content_box(src)

    scale = H / ch
    scaled_w = round(W * scale / 2) * 2
    # after scaling, center the 1080 window on the CONTENT center (the cell can
    # sit slightly off-center in the generation)
    content_cx = (x1 + cw / 2) * scale
    crop_x = max(0, min(scaled_w - W, round(content_cx - W / 2)))

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-vf", f"crop={W}:{ch}:0:{y1},scale={scaled_w}:{H}:flags=lanczos,crop={W}:{H}:{crop_x}:0",
         "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "copy", "-movflags", "+faststart", str(dest)],
        check=True,
    )
    print(f"[{key}] content y={y1} h={ch} -> normalized {dest.name} ({dest.stat().st_size:,} B)")
    return dest


if __name__ == "__main__":
    keys = sys.argv[1:] or ["h1"]
    for key in keys:
        normalize(key)
