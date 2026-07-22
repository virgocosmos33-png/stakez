"""Turn the Kling blue-screen idle clips into SEAMLESS-looping ALPHA webms.

For each assets-raw/lady_video/lady_idle_*.mp4:
  1. chroma-key the blue background to alpha (+ blue despill), aggressive enough
     to also remove the bluish floor-shadow Kling bakes under the figure.
  2. zero the very bottom strip (below the feet) so any leftover shadow smear is
     gone.
  3. build a SEAMLESS loop by CROSSFADE-WRAP: motion always plays forward and the
     tail is cross-dissolved back into the head, so the last frame is continuous
     with the first (no boomerang "rewind", no jump-cut).
  4. encode VP9 with alpha (yuva420p) -> static/assets/sprites/scene/{stem}.webm

Chrome/Pixi decode VP9 alpha natively (ffprobe may mis-report pix_fmt as yuv420p
with alpha_mode=1 — that's fine, the alpha is present).

Run: python tools/post_lady_idle_video.py
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
SRC = APP / "assets-raw" / "lady_video"
DEST = APP / "static" / "assets" / "sprites" / "scene"

# aggressive blue key: the figure has NO true blue (her "blues" are purple = red+
# blue, a different chroma angle, so they survive), which lets us push similarity
# high enough to erase the flat field AND the bluish floor shadow.
KEY = "chromakey=0x0000FF:0.24:0.12,despill=type=blue:mix=0.5:expand=0.05"

# crossfade-wrap overlap (seconds). The loop length becomes L - XFADE.
XFADE = 1.2

# bottom strip (fraction of height) forced fully transparent to nuke any residual
# shadow smear below the feet.
BOTTOM_KEEP = 0.955


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(str(c) for c in cmd[:6])}...\n{result.stderr[-1500:]}")


def probe(mp4: Path) -> tuple[float, int, int]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "format=duration:stream=width,height",
         "-of", "json", str(mp4)],
        capture_output=True, text=True, check=True,
    ).stdout
    data = json.loads(out)
    dur = float(data["format"]["duration"])
    w = int(data["streams"][0]["width"])
    h = int(data["streams"][0]["height"])
    return dur, w, h


def build_filter(dur: float, h: int) -> str:
    d = XFADE
    keep_h = (round(h * BOTTOM_KEEP) // 2) * 2  # even
    # keyed + shadow-strip removed, then split into 3 for the wrap loop
    pre = (
        f"[0:v]{KEY},format=yuva420p,"
        f"crop={{W}}:{keep_h}:0:0,pad={{W}}:{h}:0:0:color=0x00000000,"
        f"setpts=PTS-STARTPTS,split=3[k0][k1][k2];"
    ).replace("{W}", "iw")
    tail = f"[k0]trim=start={dur - d:.3f}:end={dur:.3f},setpts=PTS-STARTPTS[tail];"
    head = f"[k1]trim=start=0:end={d:.3f},setpts=PTS-STARTPTS[head];"
    # cross-dissolve tail -> head over the overlap (linear, per-plane incl. alpha)
    cross = f"[tail][head]blend=all_expr='A*(1-(T/{d}))+B*(T/{d})'[cross];"
    mid = f"[k2]trim=start={d:.3f}:end={dur - d:.3f},setpts=PTS-STARTPTS[mid];"
    out = "[cross][mid]concat=n=2:v=1:a=0,format=yuva420p[v]"
    return pre + tail + head + cross + mid + out


def main() -> None:
    mp4s = sorted(SRC.glob("lady_idle_*.mp4"))
    if not mp4s:
        raise SystemExit(f"no source clips in {SRC} (run gen_lady_idle_video.py first)")
    for mp4 in mp4s:
        dur, _w, h = probe(mp4)
        out = DEST / f"{mp4.stem}.webm"
        print(f"[post] {mp4.name} (L={dur:.2f}s) -> {out.name}", flush=True)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(mp4),
            "-filter_complex", build_filter(dur, h), "-map", "[v]",
            "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p",
            "-b:v", "0", "-crf", "30", "-auto-alt-ref", "0",
            "-an", str(out),
        ])
        print(f"[post] wrote {out.name} ({out.stat().st_size // 1024} KB, loop={dur - XFADE:.2f}s)", flush=True)


if __name__ == "__main__":
    main()
