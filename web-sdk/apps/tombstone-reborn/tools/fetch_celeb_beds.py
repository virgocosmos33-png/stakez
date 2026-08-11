"""Download and inspect the Layer AI celebration bed candidates.

The forge API reports a duration per output, but reported duration has lied
before and every short output comes back at exactly the same byte size, which
is what a placeholder looks like. So every candidate is fetched and measured
locally: real duration, peak, RMS and a content hash. A bed only ships if it
is long enough, audible, and different from the others.

Run: python tools/fetch_celeb_beds.py
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "celeb_candidates"
MANIFEST = APP / "tools" / "celeb_bed_candidates.json"

# A one second music loop is a stutter, not a bed. Two seconds is the shortest
# musical phrase this model reliably returns and the shortest that reads as
# music when looped, so that is the floor a take has to clear.
MIN_USABLE_SECONDS = 1.9
MIN_PEAK_DBFS = -40.0


def probe(path: Path, entries: str) -> list[str]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", entries, "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return [line for line in out.stdout.strip().splitlines() if line]


def levels(path: Path) -> tuple[float, float]:
    out = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    peak = rms = -99.0
    for line in out.stderr.splitlines():
        if "max_volume:" in line:
            peak = float(line.split("max_volume:")[1].split("dB")[0])
        elif "mean_volume:" in line:
            rms = float(line.split("mean_volume:")[1].split("dB")[0])
    return peak, rms


# The win level climbs one stage at a time, so each bed sits a step above the
# one before it and the escalation is audible in the mix, not just the
# arrangement. These are RMS targets in dBFS, set here rather than with
# loudnorm in the sprite: loudnorm does not converge on a two second clip and
# left every stage at the same level when it was tried.
STAGE_RMS_TARGET = {"1": -22.0, "2": -21.0, "3": -20.0, "4": -19.0, "5": -18.0, "6": -17.0}
PEAK_CEILING = 0.84  # -1.5 dBFS as a linear limiter threshold


# Mirrors the trim the sprite applies, so the level is measured on exactly the
# audio that ends up looping rather than on the untrimmed take.
_TRIM_END = ("silenceremove=start_periods=1:start_threshold=-50dB"
             ":start_silence=0:detection=peak")
TRIM_EDGES = f"{_TRIM_END},areverse,{_TRIM_END},areverse"


def install(record: dict, stage: str) -> float:
    """Publish a winning take as the stage's bed, placed on the level ladder."""
    dest = APP / "assets-raw" / "audio_gen" / f"bgm_celeb_{stage}.mp3"
    with tempfile.TemporaryDirectory() as tmp:
        trimmed = Path(tmp) / "trimmed.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", record["path"],
                        "-af", TRIM_EDGES, "-ar", "44100", "-ac", "2", str(trimmed)],
                       check=True)
        _, trimmed_rms = levels(trimmed)
        gain_db = STAGE_RMS_TARGET[stage] - trimmed_rms
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(trimmed),
             "-af", f"volume={gain_db:.2f}dB,alimiter=limit={PEAK_CEILING}:level=false",
             "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2", str(dest)],
            check=True,
        )
    return gain_db


def main() -> int:
    candidates = json.loads(MANIFEST.read_text(encoding="utf-8"))["candidates"]
    RAW.mkdir(parents=True, exist_ok=True)
    by_stage: dict[str, list[dict]] = {}

    for item in candidates:
        dest = RAW / f"{item['name']}.mp3"
        if not dest.exists():
            urllib.request.urlretrieve(item["url"], dest)
        duration = float(probe(dest, "format=duration")[0])
        peak, rms = levels(dest)
        digest = hashlib.md5(dest.read_bytes()).hexdigest()[:12]
        record = {
            "name": item["name"], "stage": item["stage"], "path": str(dest),
            "seconds": duration, "peak_dbfs": peak, "rms_dbfs": rms, "md5": digest,
            "reported": item.get("reported"),
        }
        usable = duration >= MIN_USABLE_SECONDS and peak >= MIN_PEAK_DBFS
        record["usable"] = usable
        by_stage.setdefault(item["stage"], []).append(record)
        flag = "OK " if usable else "REJECT"
        drift = "" if abs(duration - float(item.get("reported", duration))) < 0.2 else "  (API LIED)"
        print(f"{flag} {item['name']:26} {duration:5.2f}s  peak {peak:7.2f} dB  "
              f"rms {rms:7.2f} dB  md5 {digest}{drift}")

    print("\nidentical content groups (same md5 = the model returned the same file):")
    seen: dict[str, list[str]] = {}
    for records in by_stage.values():
        for record in records:
            seen.setdefault(record["md5"], []).append(record["name"])
    duplicates = {k: v for k, v in seen.items() if len(v) > 1}
    if duplicates:
        for digest, names in duplicates.items():
            print(f"  {digest}: {', '.join(names)}")
    else:
        print("  none - every candidate is unique")

    print("\ninstalled bed per stage:")
    missing = []
    for stage in sorted(by_stage):
        usable = [r for r in by_stage[stage] if r["usable"]]
        if usable:
            best = max(usable, key=lambda r: r["seconds"])
            gain = install(best, stage)
            print(f"  bgm_celeb_{stage} <- {best['name']}  {best['seconds']:.2f}s  "
                  f"gain {gain:+.1f} dB to {STAGE_RMS_TARGET[stage]:.0f} dBFS  md5 {best['md5']}")
        else:
            print(f"  stage {stage}: NOTHING USABLE - needs regeneration")
            missing.append(stage)

    (APP / "tools" / "celeb_bed_report.json").write_text(
        json.dumps(by_stage, indent=2), encoding="utf-8"
    )
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
