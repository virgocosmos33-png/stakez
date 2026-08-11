"""Download and install the two Layer AI bonus-entry stings.

Same shape as fetch_celeb_beds.py and it borrows that module's measuring
helpers: the forge surface ignores duration_seconds for this model and sizes
the take from the prompt wording, so each cue is drawn several times and the
take with the most audible content wins. Reported duration has been wrong
before, so every candidate is measured locally before anything is installed.

Owns sfx_bonus_entry_small and sfx_bonus_entry_super only. The third banner cue,
sfx_bonus_handoff, is a stem composition in build_tombstone_audio.py — the model
would only return a bare click for it, so it is layered from hammer_cock and
grit_fall_light instead. One producer per cue.

Run: python tools/fetch_bonus_entry_sfx.py
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_celeb_beds import levels, probe  # noqa: E402

APP = Path(__file__).resolve().parents[1]
RAW = APP / "assets-raw" / "bonus_entry_candidates"
MANIFEST = APP / "tools" / "bonus_entry_candidates.json"
GEN = APP / "assets-raw" / "audio_gen"

# Judged on AUDIBLE seconds, not file length. The model pads a take out to the
# requested duration with digital silence, and the sprite trims that off, so
# total length says nothing about whether the cue is complete - a two second
# file holding one 150ms click passes any length or peak test and still sounds
# like a cue with its tail cut off.
#
# Both stings play under a full-screen takeover and carry a sequence of events,
# so they need close to two seconds of actual sound in them.
MIN_AUDIBLE_SECONDS = {
    "sfx_bonus_entry_small": 1.8,
    "sfx_bonus_entry_super": 1.6,
}
MIN_PEAK_DBFS = -40.0
SILENCE_FLOOR_DB = -40

# Loudness is set here, deterministically, and the sprite leaves these two cues
# alone. A single loudnorm pass in the sprite delivered the small sting 7 dB
# under its target because the take ends in a long quiet decay that drags the
# integrated reading down - it came out quieter than the hand-off accent, which
# inverts the whole point. Measuring the take and applying a fixed gain is the
# same fix the celebration beds needed (tools/fetch_celeb_beds.py).
#
# OPEN GRAVE sits a step above DEAD MAN'S HAND: it is the 1000x buy and has to
# land bigger. Both are above the hand-off, which is punctuation, not an
# announcement.
TARGET_LUFS = {"sfx_bonus_entry_small": -11.0, "sfx_bonus_entry_super": -10.0}
PEAK_CEILING = 0.89  # about -1 dBFS as a linear limiter threshold


def integrated_lufs(path: Path) -> float:
    proc = subprocess.run(
        ["ffmpeg", "-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    found = re.findall(r"I:\s+(-?[\d.]+) LUFS", proc.stderr)
    return float(found[-1]) if found else -70.0


def set_level(cue: str) -> float:
    """Place a finished cue on its loudness target. Returns the gain applied."""
    path = GEN / f"{cue}.mp3"
    gain = TARGET_LUFS[cue] - integrated_lufs(path)
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp) / "level.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-af",
             f"volume={gain:.2f}dB,alimiter=limit={PEAK_CEILING}:level=false",
             "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2", str(staged)],
            check=True,
        )
        shutil.copy2(staged, path)
    return gain


def content_seconds(path: Path) -> float:
    """Seconds of the take that are above the silence floor."""
    proc = subprocess.run(
        ["ffmpeg", "-i", str(path), "-af",
         f"silencedetect=noise={SILENCE_FLOOR_DB}dB:d=0.1", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    silent = sum(float(m) for m in re.findall(r"silence_duration: ([\d.]+)", proc.stderr))
    return max(0.0, float(probe(path, "format=duration")[0]) - silent)


# Cues that no single take can cover, layered from several instead.
#
# OPEN GRAVE has to read as bigger than DEAD MAN'S HAND, and it needs a sequence
# in it: wood splintering, then earth tearing, then the brass under both. The
# model would not hold that for more than about a second no matter how the
# prompt was worded - twelve draws never beat 1.2s of audible content - so the
# takes are layered the same way the rest of this game's cues are built from
# stems, rather than shipping the longest lottery ticket. Offsets in ms.
COMPOSE: dict[str, list[tuple[str, int]]] = {
    "sfx_bonus_entry_super": [("super_f", 0), ("super_g", 520), ("super_c", 1450)],
}

_TRIM_ONE_END = ("silenceremove=start_periods=1:start_threshold=-45dB"
                 ":start_silence=0:detection=peak")
TRIM = f"{_TRIM_ONE_END},areverse,{_TRIM_ONE_END},areverse"


def install(record: dict, cue: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", record["path"], "-af", TRIM,
         "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
         str(GEN / f"{cue}.mp3")],
        check=True,
    )


def compose(cue: str, takes: dict[str, dict]) -> None:
    """Layer several takes into one cue, each trimmed then placed on its offset."""
    parts = COMPOSE[cue]
    args: list[str] = ["ffmpeg", "-y", "-v", "error"]
    for name, _ in parts:
        args += ["-i", takes[name]["path"]]
    chains = [
        f"[{i}:a]{TRIM},adelay={offset}|{offset}[p{i}]"
        for i, (_, offset) in enumerate(parts)
    ]
    mix = "".join(f"[p{i}]" for i in range(len(parts)))
    # normalize=0 keeps each layer at full weight - amix's default divides by the
    # input count, which would make a three-layer cue quieter than one take. The
    # limiter is what catches the peaks that creates.
    graph = (";".join(chains) + f";{mix}amix=inputs={len(parts)}:normalize=0,"
             "alimiter=limit=0.89:level=false[out]")
    args += ["-filter_complex", graph, "-map", "[out]",
             "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
             str(GEN / f"{cue}.mp3")]
    subprocess.run(args, check=True)


def main() -> int:
    candidates = json.loads(MANIFEST.read_text(encoding="utf-8"))["candidates"]
    RAW.mkdir(parents=True, exist_ok=True)
    by_cue: dict[str, list[dict]] = {}

    for item in candidates:
        dest = RAW / f"{item['name']}.mp3"
        if not dest.exists():
            urllib.request.urlretrieve(item["url"], dest)
        duration = float(probe(dest, "format=duration")[0])
        peak, rms = levels(dest)
        content = content_seconds(dest)
        record = {
            "name": item["name"], "cue": item["cue"], "path": str(dest),
            "seconds": duration, "peak_dbfs": peak, "rms_dbfs": rms,
            "content": content,
            "md5": hashlib.md5(dest.read_bytes()).hexdigest()[:12],
        }
        record["usable"] = (
            content >= MIN_AUDIBLE_SECONDS[item["cue"]] and peak >= MIN_PEAK_DBFS
        )
        by_cue.setdefault(item["cue"], []).append(record)
        print(f"{'OK ' if record['usable'] else 'REJECT'} {item['name']:26} "
              f"{duration:5.2f}s  audible {content:5.2f}s ({content / duration:4.0%})  "
              f"peak {peak:7.2f} dB  rms {rms:7.2f} dB  md5 {record['md5']}")

    print("\ninstalled cue:")
    missing = []
    by_name = {r["name"]: r for records in by_cue.values() for r in records}
    for cue in sorted(by_cue):
        if cue in COMPOSE:
            compose(cue, by_name)
            layers = ", ".join(f"{n}@{ms}ms" for n, ms in COMPOSE[cue])
            built = GEN / f"{cue}.mp3"
            audible = content_seconds(built)
            gain = set_level(cue)
            print(f"  {cue:24} <- layered {layers}  ({audible:.2f}s audible, "
                  f"{gain:+.1f} dB to {TARGET_LUFS[cue]:.0f} LUFS)")
            continue
        usable = [r for r in by_cue[cue] if r["usable"]]
        if usable:
            # Most audible content first, then level: two takes holding the same
            # amount of sound are not equal, and the louder one is the one with
            # all the events in it rather than one thin hit and air.
            best = max(usable, key=lambda r: (round(r["content"], 1), r["rms_dbfs"]))
            install(best, cue)
            gain = set_level(cue)
            print(f"  {cue:24} <- {best['name']}  {best['content']:.2f}s audible  "
                  f"md5 {best['md5']}  ({gain:+.1f} dB to {TARGET_LUFS[cue]:.0f} LUFS)")
        else:
            print(f"  {cue:24} NOTHING USABLE - needs regeneration")
            missing.append(cue)

    distinct = {r["md5"] for records in by_cue.values() for r in records}
    total = sum(len(v) for v in by_cue.values())
    print(f"\n{len(distinct)}/{total} candidates are unique content")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
