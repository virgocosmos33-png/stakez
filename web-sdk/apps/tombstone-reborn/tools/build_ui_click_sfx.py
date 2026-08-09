"""Add pleasant CC0 UI-click cues to the Howler audio sprite.

Sources: Kenney "Interface Sounds" pack (CC0 / public domain, www.kenney.nl).
Three cues are added for HUD button interactions:

    sfx_ui_click        <- select_007  (main, general HUD buttons)
    sfx_ui_click_soft   <- select_002  (soft, secondary / small controls)
    sfx_ui_click_heavy  <- toggle_002  (weightier, primary / SPIN accent)

Sources were chosen by loudness/crest analysis (clean body, low crest) so the
clicks read as crisp and present rather than thin. Each click is loudness-
matched (RMS target with a true-peak ceiling) so the three feel consistent;
per-cue taste is then set with the sounds.json config volume.

Pipeline (parallel-safe):
  1. Raw originals + license are copied into assets-raw/audio_gen/ui_click_src/.
  2. Cleaned, peak-normalised mp3 "gen masters" are written to
     assets-raw/audio_gen/<cue>.mp3  (same place/convention as every other cue
     so a future rebuild_audio_sprite.py run keeps working).
  3. The cues are SURGICALLY APPENDED to the existing sprite: the current
     sounds.mp3 is decoded as the base track and the new clicks are laid out
     after it on whole-second boundaries with a >=1s gap (same convention as
     rebuild_audio_sprite.py). Existing cue offsets are left untouched, so no
     other cue is disturbed. All four encodes (ogg/m4a/mp3/ac3) + sounds.json
     are rewritten.

Re-running is idempotent: cues already present in the sprite are skipped.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import wave
from math import ceil
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
AUDIO = APP / "static" / "assets" / "audio"
GEN = APP / "assets-raw" / "audio_gen"
SRC_REPO = GEN / "ui_click_src"          # raw originals kept in-repo
BACKUP = APP / "assets-backup" / "audio_pre_uiclick"

# where the freshly-extracted Kenney pack lives (only needed on first run;
# after that the raw originals are cached in SRC_REPO and this can be missing)
KENNEY_AUDIO = Path(tempfile.gettempdir()) / "kenney_ui_src" / "Audio"

SAMPLE_RATE = 44100
CHANNELS = 2
SAMPLE_WIDTH = 2  # 16-bit
# loudness-match each click to a common RMS, never exceeding the peak ceiling;
# final in-game taste/hierarchy is set per-cue via the sounds.json config volume
TARGET_MEAN_DB = -16.0
PEAK_CEIL_DB = -1.5

# cue -> (kenney source stem, sounds.json config volume)
CUES = {
    "sfx_ui_click": ("select_007", 0.70),
    "sfx_ui_click_soft": ("select_002", 0.55),
    "sfx_ui_click_heavy": ("toggle_002", 0.85),
}


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:6])}... failed:\n{result.stderr[-800:]}")
    return result.stderr + result.stdout


def audio_stats(path: Path) -> tuple[float, float]:
    """Return (max_volume_db, mean_volume_db) via ffmpeg volumedetect."""
    out = run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "volumedetect",
               "-f", "null", "NUL"])
    mx = mn = None
    for line in out.splitlines():
        if "max_volume:" in line:
            mx = float(line.split("max_volume:")[1].strip().split()[0])
        if "mean_volume:" in line:
            mn = float(line.split("mean_volume:")[1].strip().split()[0])
    if mx is None or mn is None:
        raise RuntimeError(f"no volume stats for {path}")
    return mx, mn


def to_wav(source: Path, dest: Path, af: str | None = None,
           start_ms: float | None = None, duration_ms: float | None = None) -> None:
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if start_ms is not None:
        cmd += ["-ss", f"{start_ms / 1000:.6f}"]
    cmd += ["-i", str(source)]
    if duration_ms is not None:
        cmd += ["-t", f"{duration_ms / 1000:.6f}"]
    if af:
        cmd += ["-af", af]
    cmd += ["-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS), "-sample_fmt", "s16", str(dest)]
    run(cmd)


def wav_frames(path: Path) -> bytes:
    with wave.open(str(path), "rb") as handle:
        assert handle.getframerate() == SAMPLE_RATE and handle.getnchannels() == CHANNELS
        return handle.readframes(handle.getnframes())


def stage_raw_originals() -> None:
    """Cache the untouched Kenney .ogg files + license inside the repo."""
    SRC_REPO.mkdir(parents=True, exist_ok=True)
    (SRC_REPO / "SOURCE.txt").write_text(
        "UI click SFX source\n"
        "===================\n"
        "Pack   : Kenney - Interface Sounds (v1.0)\n"
        "URL    : https://kenney.nl/assets/interface-sounds\n"
        "License: Creative Commons Zero (CC0 1.0) - public domain\n"
        "         http://creativecommons.org/publicdomain/zero/1.0/\n"
        "Credit : Kenney (www.kenney.nl) - optional, not required.\n\n"
        "Mapping (source .ogg -> sprite cue):\n"
        + "".join(f"  {stem}.ogg -> {cue}\n" for cue, (stem, _) in CUES.items())
    )
    for _cue, (stem, _vol) in CUES.items():
        src = KENNEY_AUDIO / f"{stem}.ogg"
        dst = SRC_REPO / f"{stem}.ogg"
        if not dst.exists():
            if not src.exists():
                raise SystemExit(
                    f"missing raw source {src} and no cached copy at {dst}; "
                    f"re-download the Kenney Interface Sounds pack first."
                )
            shutil.copy2(src, dst)


def build_gen_masters() -> None:
    """Write cleaned, peak-normalised mp3 masters into assets-raw/audio_gen/."""
    for cue, (stem, _vol) in CUES.items():
        src = SRC_REPO / f"{stem}.ogg"
        mx, mn = audio_stats(src)
        # loudness-match to TARGET_MEAN, but never push the peak past the ceiling
        gain = min(TARGET_MEAN_DB - mn, PEAK_CEIL_DB - mx)
        # trim leading silence, tiny in/out fades (no clicks), apply gain
        af = (
            "silenceremove=start_periods=1:start_threshold=-50dB:"
            "start_silence=0.001:detection=peak,"
            "afade=t=in:d=0.0015,areverse,afade=t=in:d=0.004,areverse,"
            f"volume={gain:.2f}dB"
        )
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
             "-af", af, "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS),
             "-c:a", "libmp3lame", "-b:a", "192k", str(GEN / f"{cue}.mp3")])
        print(f"[gen] {cue}.mp3  (from {stem}.ogg, {gain:+.1f} dB)")


def append_to_sprite() -> None:
    sounds = json.loads((AUDIO / "sounds.json").read_text())
    sprite: dict[str, list] = sounds["sprite"]
    config: dict[str, dict] = sounds.setdefault("config", {})

    todo = [c for c in CUES if c not in sprite]
    if not todo:
        print("[sprite] all UI-click cues already present - nothing to do")
        return

    # one-time backup of the shipped bundle
    BACKUP.mkdir(parents=True, exist_ok=True)
    for name in ("sounds.json", "sounds.mp3", "sounds.ogg", "sounds.m4a", "sounds.ac3"):
        if (AUDIO / name).exists() and not (BACKUP / name).exists():
            shutil.copy2(AUDIO / name, BACKUP / name)

    tmp = Path(tempfile.mkdtemp(prefix="uiclick_sprite_"))
    frame_bytes = CHANNELS * SAMPLE_WIDTH

    # base = current sprite decoded (existing cues stay at their exact offsets)
    base_wav = tmp / "base.wav"
    to_wav(AUDIO / "sounds.mp3", base_wav)
    master = bytearray(wav_frames(base_wav))
    cursor_ms = len(master) / frame_bytes / SAMPLE_RATE * 1000

    for cue in todo:
        seg = tmp / f"{cue}.wav"
        to_wav(GEN / f"{cue}.mp3", seg)  # already normalised; no re-processing
        frames = wav_frames(seg)

        start_ms = ceil(cursor_ms / 1000 + 1) * 1000  # whole second, >=1s gap
        pad_frames = int(round(start_ms / 1000 * SAMPLE_RATE)) - len(master) // frame_bytes
        master.extend(b"\x00" * (pad_frames * frame_bytes))
        master.extend(frames)

        dur_ms = len(frames) / frame_bytes / SAMPLE_RATE * 1000
        sprite[cue] = [start_ms, dur_ms]
        config[cue] = {"volume": CUES[cue][1]}
        cursor_ms = start_ms + dur_ms
        print(f"[sprite] + {cue}: start={start_ms}ms dur={dur_ms:.1f}ms vol={CUES[cue][1]}")

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
        if not (AUDIO / name).exists():
            continue
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(master_wav),
             *codec, str(AUDIO / name)])
        print(f"[sprite] wrote {name} ({(AUDIO / name).stat().st_size // 1024} KB)")

    sounds["sprite"] = sprite
    (AUDIO / "sounds.json").write_text(json.dumps(sounds, indent="\t") + "\n")
    print("[sprite] sounds.json updated")
    shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    stage_raw_originals()
    build_gen_masters()
    append_to_sprite()


if __name__ == "__main__":
    main()
