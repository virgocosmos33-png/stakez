"""Measure every cue as it actually exists inside the shipped sprite.

The per-cue mp3 files in assets-raw are only the input; what the player hears is
the segment carved out of static/assets/audio/sounds.mp3 after the sprite's own
loudness pass. This reads that, so levels are verified on the real artifact.

Run: python tools/probe_sprite_segments.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
AUDIO = APP / "static" / "assets" / "audio"

CLIP_PEAK_DB = -0.05
INAUDIBLE_RMS_DB = -45.0
# a segment that is nearly all silence means the sprite window is misaligned
MAX_SILENT_RATIO = 0.75


def probe(start_ms: float, duration_ms: float, temp: Path) -> dict:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-ss", f"{start_ms / 1000:.6f}", "-i", str(AUDIO / "sounds.mp3"),
         "-t", f"{duration_ms / 1000:.6f}", "-ar", "44100", "-ac", "2", str(temp)],
        capture_output=True, text=True, check=True,
    )
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(temp),
         "-af", "astats,silencedetect=n=-45dB:d=0.2", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr

    def grab(pattern: str) -> float:
        match = re.search(pattern, log)
        try:
            return float(match.group(1)) if match else 0.0
        except ValueError:
            return 0.0

    silent = sum(float(value) for value in re.findall(r"silence_duration: (\S+)", log))
    return {
        "peak_db": grab(r"Peak level dB: (\S+)"),
        "rms_db": grab(r"RMS level dB: (\S+)"),
        "silent_ratio": silent / (duration_ms / 1000) if duration_ms else 1.0,
    }


def main() -> None:
    sprite = json.loads((AUDIO / "sounds.json").read_text(encoding="utf-8"))["sprite"]
    temp_dir = Path(tempfile.mkdtemp(prefix="sprite_probe_"))
    temp = temp_dir / "seg.wav"
    failures: list[str] = []

    print(f"{'cue':30} {'start':>8} {'dur':>7} {'peak':>7} {'rms':>7} {'silent':>7} loop  status")
    for cue, entry in sprite.items():
        start, duration = float(entry[0]), float(entry[1])
        info = probe(start, duration, temp)
        notes: list[str] = []
        if info["rms_db"] <= INAUDIBLE_RMS_DB:
            notes.append("INAUDIBLE")
        if info["peak_db"] >= CLIP_PEAK_DB:
            notes.append("CLIPPING")
        if info["silent_ratio"] > MAX_SILENT_RATIO:
            notes.append(f"{info['silent_ratio']:.0%} SILENT")
        if notes:
            failures.append(f"{cue}: {', '.join(notes)}")
        print(
            f"{cue:30} {start:8.0f} {duration:7.0f} {info['peak_db']:7.2f} "
            f"{info['rms_db']:7.2f} {info['silent_ratio']:6.0%} "
            f"{'yes ' if len(entry) > 2 and entry[2] else '  - '} {', '.join(notes) or 'ok'}"
        )

    print(f"\n{len(sprite)} cues probed in the shipped sprite, {len(failures)} failure(s)")
    for failure in failures:
        print(f"  ! {failure}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
