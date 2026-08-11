"""Prove the audio family is consistent: sprite <-> types <-> call sites.

Catches every way this can break at runtime:
  - a component plays a key that is not in the sprite (silent + console warning)
  - the sprite has a key the TypeScript union rejects (or vice versa)
  - a sprite segment runs past the end of the master, or overlaps its neighbour
  - a retired legacy key still appears anywhere in the app source

Run: python tools/validate_audio_wiring.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
SRC = APP / "src"
AUDIO = APP / "static" / "assets" / "audio"

SOURCE_SUFFIXES = {".ts", ".svelte", ".js"}
RETIRED = (
    "sfx_madams_eye",
    "sfx_mirror_break",
    "sfx_xways_split",
    "sfx_claw_split",
    "sfx_cell_seal_h3_loop",
    "bgm_winlevel_big",
    "bgm_winlevel_superwin",
    "bgm_winlevel_mega",
    "bgm_winlevel_epic",
    "bgm_winlevel_max",
)
# keys the app builds at runtime from a template rather than writing literally
DYNAMIC_KEY_PREFIXES = ("bgm_celeb_",)


def union_keys() -> set[str]:
    text = (SRC / "game" / "sound.ts").read_text(encoding="utf-8")
    return set(re.findall(r"^\s*\|\s*'([a-z0-9_]+)'", text, re.MULTILINE))


def source_files() -> list[Path]:
    found: list[Path] = []
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            if Path(name).suffix in SOURCE_SUFFIXES:
                found.append(Path(root) / name)
    return found


def referenced_keys(files: list[Path]) -> dict[str, list[str]]:
    """Sound keys quoted anywhere in app source, with the files that use them."""
    hits: dict[str, list[str]] = {}
    pattern = re.compile(r"'((?:sfx|bgm|jng|tumble)_[a-z0-9_]+)'")
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for key in set(pattern.findall(text)):
            hits.setdefault(key, []).append(str(path.relative_to(APP)))
    return hits


def master_duration_ms() -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(AUDIO / "sounds.mp3")],
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out) * 1000 if out else 0.0


def main() -> None:
    sounds = json.loads((AUDIO / "sounds.json").read_text(encoding="utf-8"))
    sprite: dict[str, list] = sounds["sprite"]
    union = union_keys()
    files = source_files()
    refs = referenced_keys(files)
    failures: list[str] = []

    missing_in_sprite = sorted(key for key in refs if key not in sprite)
    for key in missing_in_sprite:
        failures.append(f"played but NOT in sprite: {key}  ({', '.join(refs[key])})")

    for key in sorted(union - set(sprite)):
        failures.append(f"in sound.ts union but NOT in sprite: {key}")
    for key in sorted(set(sprite) - union):
        if not key.startswith(DYNAMIC_KEY_PREFIXES):
            failures.append(f"in sprite but NOT in sound.ts union: {key}")

    for key in RETIRED:
        if key in sprite:
            failures.append(f"retired key still in sprite: {key}")
        if key in refs:
            failures.append(f"retired key still referenced: {key} ({', '.join(refs[key])})")

    total_ms = master_duration_ms()
    ordered = sorted(sprite.items(), key=lambda item: item[1][0])
    previous_end = 0.0
    previous_key = None
    for key, entry in ordered:
        start, duration = float(entry[0]), float(entry[1])
        if duration <= 0:
            failures.append(f"zero-length sprite entry: {key}")
        if start + duration > total_ms + 1:
            failures.append(
                f"{key} runs past end of master: {start + duration:.0f}ms > {total_ms:.0f}ms"
            )
        if start < previous_end:
            failures.append(f"{key} overlaps {previous_key} ({start:.0f} < {previous_end:.0f})")
        previous_end, previous_key = start + duration, key

    unreferenced = sorted(
        key for key in sprite
        if key not in refs and not key.startswith(DYNAMIC_KEY_PREFIXES)
    )

    print(f"sprite cues        : {len(sprite)}")
    print(f"sound.ts union     : {len(union)}")
    print(f"keys used in src   : {len(refs)}")
    print(f"master length      : {total_ms:.0f} ms")
    print(f"last cue ends at   : {previous_end:.0f} ms")
    if unreferenced:
        print(f"\nin sprite, no literal call site ({len(unreferenced)}):")
        for key in unreferenced:
            print(f"  - {key}")

    print(f"\n{len(failures)} failure(s)")
    for failure in failures:
        print(f"  ! {failure}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
