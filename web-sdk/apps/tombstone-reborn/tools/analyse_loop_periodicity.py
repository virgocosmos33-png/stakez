"""Find repeating layers hiding inside a looping cue.

A music bed is supposed to repeat only at its own loop length. If a sustained
layer was built by tiling a short one-shot, the cue contains a SECOND, faster
repeat at the tile period. When that period is not a whole number of beats it
fights the music grid and is heard as a separate track droning underneath.

The envelope autocorrelation finds those periods; the beat check says whether a
period is musical or foreign.

Run: python tools/analyse_loop_periodicity.py [cue ...]
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
GEN = APP / "assets-raw" / "audio_gen"

ENVELOPE_RATE = 200          # envelope samples per second (5ms frames)
ANALYSIS_RATE = 8000         # plenty for an amplitude envelope
BEAT_MS = 500                # the grid the beds were sequenced on
MIN_PERIOD_S = 0.30          # ignore anything faster than a semiquaver-ish
BEAT_TOLERANCE_MS = 25       # how close to a beat multiple still counts as musical


def envelope(path: Path) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1",
         "-ar", str(ANALYSIS_RATE), "-f", "s16le", "-"],
        capture_output=True,
    ).stdout
    samples = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    if samples.size == 0:
        return samples
    frame = ANALYSIS_RATE // ENVELOPE_RATE
    usable = (samples.size // frame) * frame
    frames = samples[:usable].reshape(-1, frame)
    return np.sqrt((frames**2).mean(axis=1))


def top_periods(env: np.ndarray, count: int = 4) -> list[tuple[float, float]]:
    """Strongest self-similarity periods of the envelope, as (seconds, score)."""
    signal = env - env.mean()
    if not np.any(signal):
        return []
    corr = np.correlate(signal, signal, mode="full")[signal.size - 1:]
    corr /= corr[0]
    lo = int(MIN_PERIOD_S * ENVELOPE_RATE)
    hi = signal.size // 2
    if hi <= lo:
        return []
    window = corr[lo:hi]
    peaks = [
        (i + lo, window[i])
        for i in range(1, window.size - 1)
        if window[i] > window[i - 1] and window[i] >= window[i + 1]
    ]
    peaks.sort(key=lambda p: p[1], reverse=True)
    # keep peaks apart, otherwise one broad hump is reported as four "periods"
    min_gap = int(0.15 * ENVELOPE_RATE)
    chosen: list[tuple[int, float]] = []
    for lag, score in peaks:
        if all(abs(lag - kept) >= min_gap for kept, _ in chosen):
            chosen.append((lag, score))
        if len(chosen) == count:
            break
    return [(lag / ENVELOPE_RATE, score) for lag, score in chosen]


def beat_verdict(period_s: float) -> str:
    beats = period_s * 1000 / BEAT_MS
    nearest = round(beats)
    if nearest < 1:
        return "sub-beat"
    off_ms = abs(period_s * 1000 - nearest * BEAT_MS)
    if off_ms <= BEAT_TOLERANCE_MS:
        return f"on grid ({nearest} beat{'s' if nearest != 1 else ''})"
    return f"OFF GRID ({beats:.2f} beats, {off_ms:.0f}ms out)"


def main() -> int:
    cues = sys.argv[1:] or ["bgm_main", "sfx_anticipation", "sfx_fire_loop"]
    worst = 0
    for cue in cues:
        path = GEN / f"{cue}.mp3"
        if not path.exists():
            print(f"{cue}: missing {path}")
            continue
        env = envelope(path)
        print(f"\n{cue}  ({env.size / ENVELOPE_RATE:.2f}s)")
        found = top_periods(env)
        if not found:
            print("   no repeating structure")
            continue
        for period, score in found:
            verdict = beat_verdict(period)
            flag = ""
            if "OFF GRID" in verdict and score >= 0.30:
                flag = "   <-- foreign repeat, this is a second track"
                worst += 1
            print(f"   period {period:5.2f}s  strength {score:5.2f}  {verdict}{flag}")
    print(f"\n{worst} foreign repeat(s) found")
    return 1 if worst else 0


if __name__ == "__main__":
    raise SystemExit(main())
