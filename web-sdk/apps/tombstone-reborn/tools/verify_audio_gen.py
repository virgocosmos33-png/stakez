"""Quality gate for assets-raw/audio_gen before the sprite is rebuilt.

Flags the failure modes that an API response will happily hide: silent files,
clipped files, files that are mostly dead air, and accidental duplicates.

Run: python tools/verify_audio_gen.py
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
GEN = APP / "assets-raw" / "audio_gen"

CLIP_PEAK_DB = -0.05
SILENT_RMS_DB = -50.0
QUIET_RMS_DB = -40.0
MAX_SILENT_RATIO = 0.6


def analyse(path: Path) -> dict:
    duration_raw = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    ).stdout.strip()
    log = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-af", "astats=metadata=1:reset=0,silencedetect=n=-45dB:d=0.25", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr

    def grab(pattern: str) -> float:
        match = re.search(pattern, log)
        try:
            return float(match.group(1)) if match else 0.0
        except ValueError:
            return 0.0

    duration = float(duration_raw) if duration_raw else 0.0
    silent = sum(float(value) for value in re.findall(r"silence_duration: (\S+)", log))
    return {
        "duration": duration,
        "peak_db": grab(r"Peak level dB: (\S+)"),
        "rms_db": grab(r"RMS level dB: (\S+)"),
        "silent_ratio": (silent / duration) if duration else 1.0,
    }


def main() -> None:
    files = sorted(GEN.glob("*.mp3"))
    if not files:
        raise SystemExit(f"no mp3 files in {GEN}")

    seen: dict[str, str] = {}
    problems: list[str] = []
    print(f"{'cue':30} {'dur':>6} {'peak':>7} {'rms':>7} {'silent':>7}  status")
    for path in files:
        info = analyse(path)
        digest = hashlib.md5(path.read_bytes()).hexdigest()
        notes: list[str] = []
        if info["duration"] <= 0.05:
            notes.append("EMPTY")
        if info["rms_db"] <= SILENT_RMS_DB:
            notes.append("SILENT")
        elif info["rms_db"] <= QUIET_RMS_DB:
            notes.append("very quiet")
        if info["peak_db"] >= CLIP_PEAK_DB:
            notes.append("CLIPPING")
        if info["silent_ratio"] > MAX_SILENT_RATIO:
            notes.append(f"{info['silent_ratio']:.0%} dead air")
        if digest in seen:
            notes.append(f"DUPLICATE OF {seen[digest]}")
        else:
            seen[digest] = path.stem
        hard = [note for note in notes if note.isupper() or "dead air" in note]
        if hard:
            problems.append(f"{path.stem}: {', '.join(hard)}")
        print(
            f"{path.stem:30} {info['duration']:6.2f} {info['peak_db']:7.2f} "
            f"{info['rms_db']:7.2f} {info['silent_ratio']:6.0%}  {', '.join(notes) or 'ok'}"
        )

    print(f"\n{len(files)} files, {len(problems)} problem(s)")
    for problem in problems:
        print(f"  ! {problem}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
