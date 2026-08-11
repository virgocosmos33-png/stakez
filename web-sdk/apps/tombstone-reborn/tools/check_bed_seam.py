"""Check that a looping bed in the shipped sprite actually loops seamlessly.

A loop is only clean if the sprite window holds the whole take: silence at the
window edges reads as a gap every time it wraps, and a loud discontinuity
between the last and first millisecond reads as a click. This measures the
shipped sprite, not the source file, so it catches damage done by the sprite's
own re-encode.

Run: python tools/check_bed_seam.py bgm_main sfx_fire_loop
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
import wave
from array import array
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
AUDIO = APP / "static" / "assets" / "audio"
EDGE_MS = 40  # window either side of the wrap point
SILENT_DBFS = -60.0  # below this an edge counts as a gap
CLICK_DB = 12.0  # a jump this much louder than the take is a click


def rms_dbfs(samples: array) -> float:
    if not samples:
        return -math.inf
    mean_square = sum(float(s) * s for s in samples) / len(samples)
    if mean_square <= 0:
        return -math.inf
    return 20 * math.log10(math.sqrt(mean_square) / 32768.0)


def read_window(cue: str, offset_ms: float, length_ms: float) -> array:
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / f"{cue}.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error",
             "-ss", f"{offset_ms / 1000:.6f}", "-t", f"{length_ms / 1000:.6f}",
             "-i", str(AUDIO / "sounds.mp3"), "-ar", "44100", "-ac", "1", str(wav)],
            check=True,
        )
        with wave.open(str(wav), "rb") as handle:
            data = array("h")
            data.frombytes(handle.readframes(handle.getnframes()))
            return data


def main() -> int:
    sprite = json.loads((AUDIO / "sounds.json").read_text())["sprite"]
    cues = sys.argv[1:] or [k for k, v in sprite.items() if len(v) > 2 and v[2]]
    failures = 0

    for cue in cues:
        entry = sprite.get(cue)
        if entry is None:
            print(f"{cue:20} MISSING from sprite")
            failures += 1
            continue

        offset, length = entry[0], entry[1]
        samples = read_window(cue, offset, length)
        edge = int(44100 * EDGE_MS / 1000)
        head, tail = samples[:edge], samples[-edge:]
        whole = rms_dbfs(samples)
        head_db, tail_db = rms_dbfs(head), rms_dbfs(tail)
        step = abs(samples[0] - samples[-1]) / 32768.0
        step_db = 20 * math.log10(step) if step > 0 else -math.inf

        problems = []
        if head_db < SILENT_DBFS:
            problems.append(f"silent head ({head_db:.1f} dBFS) = gap on wrap")
        if tail_db < SILENT_DBFS:
            problems.append(f"silent tail ({tail_db:.1f} dBFS) = gap on wrap")
        if step_db > whole + CLICK_DB:
            problems.append(f"discontinuity {step_db:.1f} dB vs bed {whole:.1f} dB = click")

        state = "SEAMLESS" if not problems else "PROBLEM"
        print(f"{cue:20} {length / 1000:6.2f}s  bed {whole:6.1f} dBFS  "
              f"head {head_db:6.1f}  tail {tail_db:6.1f}  wrap step {step_db:6.1f} dB  {state}")
        for problem in problems:
            print(f"{'':20}   - {problem}")
        failures += len(problems)

    print(f"\n{failures} seam problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
