"""Rebuild the Howler audio sprite with Madam Mirror themed cues.

Sources per cue:
  - assets-raw/audio_gen/{cue}.mp3  (newly generated) if present
  - otherwise the segment is extracted from the CURRENT sounds.mp3 so all
    existing custom cues (bgm_main, reel stops, celeb kit, ...) are preserved.

Every cue is laid out on whole-second boundaries with >=1s of silence between
cues (same convention as the template sprite), then encoded to mp3/ogg/m4a/ac3.
sounds.json keeps its src + config blocks and loop flags.
"""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import tempfile
import wave
from math import ceil
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
AUDIO = APP / "static" / "assets" / "audio"
GEN = APP / "assets-raw" / "audio_gen"
BACKUP = APP / "assets-backup" / "audio_pre_mirror"

SAMPLE_RATE = 44100
CHANNELS = 2
SAMPLE_WIDTH = 2  # 16-bit


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:6])}... failed:\n{result.stderr[-800:]}")


def to_wav(source: Path, dest: Path, start_ms: float | None = None, duration_ms: float | None = None,
           loudnorm: bool = False) -> None:
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if start_ms is not None:
        cmd += ["-ss", f"{start_ms / 1000:.6f}"]
    cmd += ["-i", str(source)]
    if duration_ms is not None:
        cmd += ["-t", f"{duration_ms / 1000:.6f}"]
    if loudnorm:
        cmd += ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"]
    cmd += ["-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS), "-sample_fmt", "s16", str(dest)]
    run(cmd)


def wav_frames(path: Path) -> bytes:
    with wave.open(str(path), "rb") as handle:
        assert handle.getframerate() == SAMPLE_RATE and handle.getnchannels() == CHANNELS
        return handle.readframes(handle.getnframes())


# cues that exist only as generated files (not in the shipped sprite yet);
# value = loop flag
NEW_CUES = {f"bgm_celeb_{i}": True for i in range(1, 7)}


def main() -> None:
    sounds = json.loads((AUDIO / "sounds.json").read_text())
    sprite: dict[str, list] = sounds["sprite"]
    for cue, loop in NEW_CUES.items():
        if cue not in sprite and (GEN / f"{cue}.mp3").exists():
            sprite[cue] = [0, 0, loop] if loop else [0, 0]
            sounds.setdefault("config", {})[cue] = {"volume": 1}

    # one-time backup of the shipped bundle
    BACKUP.mkdir(parents=True, exist_ok=True)
    for name in ("sounds.json", "sounds.mp3", "sounds.ogg", "sounds.m4a", "sounds.ac3"):
        if not (BACKUP / name).exists():
            shutil.copy2(AUDIO / name, BACKUP / name)

    replaced, kept = [], []
    tmp = Path(tempfile.mkdtemp(prefix="mirror_sprite_"))
    segments: dict[str, Path] = {}
    for cue, entry in sprite.items():
        seg = tmp / f"{cue}.wav"
        gen_file = GEN / f"{cue}.mp3"
        if gen_file.exists():
            to_wav(gen_file, seg, loudnorm=True)
            replaced.append(cue)
        else:
            start, duration = entry[0], entry[1]
            to_wav(AUDIO / "sounds.mp3", seg, start_ms=start, duration_ms=duration)
            kept.append(cue)
        segments[cue] = seg

    # lay out the master track: cue starts on whole seconds, >=1s gap after
    frame_bytes = CHANNELS * SAMPLE_WIDTH
    new_sprite: dict[str, list] = {}
    master = bytearray()
    cursor_ms = 0.0
    for cue, entry in sprite.items():
        start_ms = ceil(cursor_ms / 1000 + (1 if cursor_ms else 0)) * 1000
        pad_frames = int(round(start_ms / 1000 * SAMPLE_RATE)) - len(master) // frame_bytes
        master.extend(b"\x00" * (pad_frames * frame_bytes))

        frames = wav_frames(segments[cue])
        master.extend(frames)
        duration_ms = len(frames) / frame_bytes / SAMPLE_RATE * 1000
        new_entry: list = [start_ms, duration_ms]
        if len(entry) > 2 and entry[2]:
            new_entry.append(True)
        new_sprite[cue] = new_entry
        cursor_ms = start_ms + duration_ms

    master_wav = tmp / "master.wav"
    with wave.open(str(master_wav), "wb") as handle:
        handle.setnchannels(CHANNELS)
        handle.setsampwidth(SAMPLE_WIDTH)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(bytes(master))

    encodes = {
        "sounds.mp3": ["-c:a", "libmp3lame", "-b:a", "160k"],
        "sounds.ogg": ["-c:a", "libvorbis", "-q:a", "5"],
        "sounds.m4a": ["-c:a", "aac", "-b:a", "160k"],
        "sounds.ac3": ["-c:a", "ac3", "-b:a", "192k"],
    }
    for name, codec in encodes.items():
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(master_wav), *codec,
             str(AUDIO / name)])
        print(f"[sprite] wrote {name} ({(AUDIO / name).stat().st_size // 1024} KB)")

    sounds["sprite"] = new_sprite
    (AUDIO / "sounds.json").write_text(json.dumps(sounds, indent="\t") + "\n")
    print(f"[sprite] sounds.json updated — {len(replaced)} cues replaced, {len(kept)} kept")
    print("[sprite] replaced:", ", ".join(replaced))
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
