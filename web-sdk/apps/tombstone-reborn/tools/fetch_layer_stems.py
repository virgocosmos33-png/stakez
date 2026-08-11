"""Download the Layer AI stem library described by tools/layer_stems.json.

Stems land in assets-raw/audio_stems/{name}.mp3 and are reported with duration,
peak and RMS so silent or clipped material is caught before it reaches a cue.

Run: python tools/fetch_layer_stems.py
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).parent / "layer_stems.json"
OUT_DIR = APP / "assets-raw" / "audio_stems"

CLIP_PEAK_DB = -0.1
SILENCE_RMS_DB = -50.0


def measure(path: Path) -> tuple[float, float, float]:
    duration_raw = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    ).stdout.strip()
    stats = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "astats", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    peak = re.search(r"Peak level dB: (\S+)", stats)
    rms = re.search(r"RMS level dB: (\S+)", stats)

    def as_float(value: str | None) -> float:
        try:
            return float(value) if value is not None else 0.0
        except ValueError:
            return 0.0

    return (
        as_float(duration_raw),
        as_float(peak.group(1) if peak else None),
        as_float(rms.group(1) if rms else None),
    )


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    workspace_id = manifest["workspace_id"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{'stem':24} {'dur':>6} {'peak':>7} {'rms':>8} {'md5':>10}  status")
    seen: dict[str, str] = {}
    problems: list[str] = []
    for name, entry in manifest["stems"].items():
        dest = OUT_DIR / f"{name}.mp3"
        url = (
            f"https://media.app.layer.ai/workspaces/{workspace_id}"
            f"/files/{entry['file_id']}/{entry['filename']}"
        )
        if not dest.exists():
            request = urllib.request.Request(url, headers={"User-Agent": "tombstone-audio"})
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    dest.write_bytes(response.read())
            except (urllib.error.URLError, TimeoutError) as err:
                problems.append(f"{name}: download failed ({err})")
                print(f"{name:24} {'-':>6} {'-':>7} {'-':>8} {'-':>10}  DOWNLOAD FAILED")
                continue

        digest = hashlib.md5(dest.read_bytes()).hexdigest()
        duration, peak, rms = measure(dest)
        notes = []
        if duration <= 0:
            notes.append("UNREADABLE")
        if rms <= SILENCE_RMS_DB:
            notes.append("NEAR SILENT")
        if peak >= CLIP_PEAK_DB:
            notes.append("CLIPPING")
        if digest in seen:
            notes.append(f"DUPLICATE OF {seen[digest]}")
        else:
            seen[digest] = name
        status = ", ".join(notes) if notes else "ok"
        if notes:
            problems.append(f"{name}: {status}")
        print(f"{name:24} {duration:6.2f} {peak:7.2f} {rms:8.2f} {digest[:10]:>10}  {status}")

    print()
    print(f"{len(manifest['stems'])} stems, {len(problems)} problem(s)")
    for problem in problems:
        print(f"  ! {problem}")


if __name__ == "__main__":
    main()
