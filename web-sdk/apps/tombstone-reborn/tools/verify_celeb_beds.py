"""Prove the shipped celebration beds are the western Layer AI takes.

Two questions matter and neither is answered by reading a manifest:
  1. does the cue in the shipped sprite hold the new bed we installed?
  2. is any trace of the old cloned-game bed still in there?

So each shipped segment is correlated against both the new source and the
pre-overhaul sprite segment recovered from git. High against new and low
against old is the only passing result.

Run: python tools/verify_celeb_beds.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from analyse_loop_periodicity import envelope  # noqa: E402

APP = Path(__file__).resolve().parents[1]
AUDIO = APP / "static" / "assets" / "audio"
GEN = APP / "assets-raw" / "audio_gen"
OLD_REF = "HEAD:web-sdk/apps/tombstone-reborn/static/assets/audio"
MATCH = 0.90


def to_wav(source: Path, dest: Path, start_ms: float | None = None,
           length_ms: float | None = None) -> Path:
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if start_ms is not None:
        cmd += ["-ss", f"{start_ms / 1000:.4f}"]
    cmd += ["-i", str(source)]
    if length_ms is not None:
        cmd += ["-t", f"{length_ms / 1000:.4f}"]
    cmd += ["-ar", "44100", "-ac", "1", str(dest)]
    subprocess.run(cmd, check=True)
    return dest


def best_correlation(a: Path, b: Path) -> float:
    """Envelope correlation allowing a small lag, so encoder delay is ignored."""
    x, y = envelope(a), envelope(b)
    if x.size < 40 or y.size < 40:
        return 0.0
    best = 0.0
    for lag in range(0, 41):
        n = min(x.size, y.size - lag)
        if n < 40:
            break
        with np.errstate(invalid="ignore"):
            c = np.corrcoef(x[:n], y[lag:lag + n])[0, 1]
        if np.isfinite(c):
            best = max(best, abs(c))
    return best


def main() -> int:
    sprite = json.loads((AUDIO / "sounds.json").read_text())["sprite"]
    failures = 0

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        old_sprite = work / "old_sounds.mp3"
        old_json = work / "old_sounds.json"
        for ref, dest in ((f"{OLD_REF}/sounds.mp3", old_sprite),
                          (f"{OLD_REF}/sounds.json", old_json)):
            with dest.open("wb") as handle:
                subprocess.run(["git", "show", ref], stdout=handle,
                               cwd=APP.parents[2], check=True)
        old_map = json.loads(old_json.read_text(encoding="utf-8-sig"))["sprite"]

        print(f"{'cue':14}{'shipped':>9}{'vs new bed':>13}{'vs old bed':>13}   verdict")
        for stage in range(1, 7):
            cue = f"bgm_celeb_{stage}"
            offset, length = sprite[cue][0], sprite[cue][1]
            shipped = to_wav(AUDIO / "sounds.mp3", work / f"{cue}_ship.wav", offset, length)
            new_src = to_wav(GEN / f"{cue}.mp3", work / f"{cue}_new.wav")
            old_off, old_len = old_map[cue][0], old_map[cue][1]
            old_src = to_wav(old_sprite, work / f"{cue}_old.wav", old_off, old_len)

            to_new = best_correlation(shipped, new_src)
            to_old = best_correlation(shipped, old_src)
            ok = to_new >= MATCH and to_old < MATCH
            verdict = "western bed shipped" if ok else "PROBLEM"
            if not ok:
                failures += 1
            print(f"{cue:14}{length / 1000:8.2f}s{to_new:13.4f}{to_old:13.4f}   {verdict}")

    print(f"\n{failures} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
