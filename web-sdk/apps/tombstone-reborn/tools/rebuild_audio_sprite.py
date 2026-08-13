"""Rebuild the Howler audio sprite from the western Tombstone Reborn cue set.

Sources per cue:
  - assets-raw/audio_gen/{cue}.mp3  (built by build_tombstone_audio.py) if present
  - otherwise the segment is extracted from the CURRENT sounds.mp3

That fallback is the leftover-detector: any cue it reports as "kept" is still
playing audio inherited from the cloned game. The target is zero kept cues.

Every cue is laid out on whole-second boundaries with >=1s of silence between
cues (same convention as the template sprite), then encoded to mp3/ogg/m4a/ac3.
sounds.json keeps its src + config blocks and loop flags.
"""

from __future__ import annotations

import json
import os
import shutil
import struct
import subprocess
import tempfile
import wave
from math import ceil
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
AUDIO = APP / "static" / "assets" / "audio"
MIRROR = APP / "assets" / "audio"  # second shipped tree, kept byte-identical
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
           loudnorm: bool = False, af: str | None = None) -> None:
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if start_ms is not None:
        cmd += ["-ss", f"{start_ms / 1000:.6f}"]
    cmd += ["-i", str(source)]
    if duration_ms is not None:
        cmd += ["-t", f"{duration_ms / 1000:.6f}"]
    if af is not None:
        cmd += ["-af", af]
    elif loudnorm:
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
NEW_CUES["sfx_tombstone_toll"] = False  # graveyard bell + slab boom for the top special drop
NEW_CUES["sfx_thunder"] = False  # mega-win lightning thunder clap
NEW_CUES["sfx_cell_seal_expand"] = False  # Cell Seal full-reel expand hit
NEW_CUES["sfx_cell_seal_harden"] = False  # Cell Seal harden / multiplier bump
NEW_CUES["sfx_cell_seal_h3_expand"] = False  # H3 expand video bed (full once)
NEW_CUES["sfx_bullet_wood"] = False  # pistol round slamming into weathered wood
NEW_CUES["sfx_bullet_ricochet"] = False  # occasional western ricochet whine after a hit
NEW_CUES["sfx_gunshot"] = False  # .44 magnum shot for the click-to-shoot board decal
NEW_CUES["sfx_ui_click"] = False
NEW_CUES["sfx_ui_click_heavy"] = False
NEW_CUES["sfx_ui_click_soft"] = False
NEW_CUES["tumble_win_5"] = False
# split feature: the seam itself tearing open, before any volley lands
NEW_CUES["sfx_split_seam_tear"] = False
# fire on linked cells / reel edges. Only the burn bed loops; ignite and the
# burn-out tail are one-shots so the lifecycle stays start -> sustain -> stop.
NEW_CUES["sfx_fire_ignite"] = False
NEW_CUES["sfx_fire_loop"] = True
NEW_CUES["sfx_fire_flare"] = False  # escalation accent as more cells link
NEW_CUES["sfx_fire_out"] = False
# target lock
NEW_CUES["sfx_lock_snap"] = False
NEW_CUES["sfx_lock_release"] = False
# clone / link charge
NEW_CUES["sfx_fuse_crackle"] = False
NEW_CUES["sfx_ember_whoosh"] = False
# feature events
NEW_CUES["sfx_reel_nudge"] = False
NEW_CUES["sfx_gunsmoke"] = False
NEW_CUES["sfx_tombstone_open"] = False
NEW_CUES["sfx_special_hit"] = False
NEW_CUES["sfx_bounty"] = False
# digUp: three strike variants plus the handle settling
NEW_CUES["sfx_shovel_strike_1"] = False
NEW_CUES["sfx_shovel_strike_2"] = False
NEW_CUES["sfx_shovel_strike_3"] = False
NEW_CUES["sfx_shovel_settle"] = False
# bonus-entry banner: one sting per bought mode plus the hand-off accent
NEW_CUES["sfx_bonus_entry_small"] = False
NEW_CUES["sfx_bonus_entry_super"] = False
NEW_CUES["sfx_bonus_handoff"] = False

# Keys retired with the Madam Mirror clone: dropped from the sprite so no
# legacy segment can survive a rebuild.
RETIRED_CUES = (
    "sfx_madams_eye",  # renamed to sfx_tombstone_toll
    "sfx_mirror_break",
    "sfx_xways_split",
    "sfx_claw_split",  # split volleys use sfx_bullet_wood + optional ricochet
    "sfx_cell_seal_h3_loop",  # the last-3s visual loop is silent
    "bgm_winlevel_big",
    "bgm_winlevel_superwin",
    "bgm_winlevel_mega",
    "bgm_winlevel_epic",
    "bgm_winlevel_max",
    # No free-spins feature exists: the math declares no freespin triggers, both
    # buy modes are one enhanced spin, and the FreeSpin overlays are deleted.
    # Nothing could start this bed, so it is not worth the sprite bytes.
    "bgm_freespin",
)

# Strip digital silence from both ends of a cue, leaving the audio itself
# alone. Used for the looping music beds so they wrap without a gap.
_TRIM_ONE_END = (
    "silenceremove=start_periods=1:start_threshold=-50dB"
    ":start_silence=0:detection=peak"
)
TRIM_EDGES = f"{_TRIM_ONE_END},areverse,{_TRIM_ONE_END},areverse"

# per-cue loudness overrides: these are normalized MUCH hotter than the default
# -16 LUFS bed so they punch through everything
CUE_FILTERS = {
    # The music beds are finished, already-mastered tracks supplied by the
    # player, not cues we assembled. They go in untouched: a loudness pass
    # would re-compress someone else's master and change the song they asked
    # for. "anull" is how a cue opts out of the default normalisation.
    #
    # The bed gets its edges trimmed instead. Every MP3 carries roughly 25ms of
    # encoder delay at the head and padding at the tail - on loop1 that is 98ms
    # of digital silence, which the player would hear as a hiccup every time the
    # bed wraps. Cutting it here, in the WAV domain before the sprite is
    # assembled, is what makes the loop gapless. This removes silence only; not
    # a sample of the music is touched.
    "bgm_main": TRIM_EDGES,
    # The six celebration stages are separate Layer AI takes. They are trimmed
    # for a gapless loop but their level is left alone: fetch_celeb_beds.py
    # already placed each stage on a rising loudness ladder, and a normalising
    # pass here would flatten that escalation straight back out.
    **{f"bgm_celeb_{i}": TRIM_EDGES for i in range(1, 7)},
    "sfx_tombstone_toll": "loudnorm=I=-9:TP=-0.1:LRA=5",
    # thunder should hit hard alongside the lightning burst
    "sfx_thunder": "loudnorm=I=-10:TP=-0.3:LRA=6",
    # bullet hits stack under the board shake — sit above the -16 bed
    "sfx_bullet_wood": "loudnorm=I=-11:TP=-0.5:LRA=7",
    "sfx_bullet_ricochet": "loudnorm=I=-13:TP=-0.8:LRA=8",
    # click-to-shoot .44 magnum: a raw downloaded one-shot, punchy above the bed
    "sfx_gunshot": "loudnorm=I=-11:TP=-0.5:LRA=7",
    # the seam tearing is the headline moment of a split
    "sfx_split_seam_tear": "loudnorm=I=-11:TP=-0.5:LRA=7",
    # the shovel has to land like it stuck in something solid
    "sfx_shovel_strike_1": "loudnorm=I=-11:TP=-0.5:LRA=7",
    "sfx_shovel_strike_2": "loudnorm=I=-11:TP=-0.5:LRA=7",
    "sfx_shovel_strike_3": "loudnorm=I=-11:TP=-0.5:LRA=7",
    # the burn bed sits UNDER everything: it sustains for whole spins, so it is
    # normalized well below the one-shot cues to stay a bed and not a wall
    "sfx_fire_loop": "loudnorm=I=-22:TP=-3:LRA=6",
    "sfx_fire_ignite": "loudnorm=I=-13:TP=-0.8:LRA=8",
    "sfx_tombstone_open": "loudnorm=I=-12:TP=-0.6:LRA=7",
    # Bonus entry. Trimmed, not normalised: the generator pads a take out to the
    # requested length with digital silence, so the window has to be cut back to
    # the cue itself or Howler holds the voice open over a second of nothing.
    # Level is already set on these two by fetch_bonus_entry_sfx.py, which
    # measures each take and applies a fixed gain - a loudnorm pass here landed
    # the small sting 7 dB under target because its long decay drags the
    # integrated reading down, leaving the headline quieter than the accent.
    "sfx_bonus_entry_small": TRIM_EDGES,
    "sfx_bonus_entry_super": TRIM_EDGES,
    # The hand-off is a stem composition with an even envelope, so the standard
    # single pass hits its target and it stays on the normal path. It is an
    # accent as the banner lets go, so it sits below both stings.
    "sfx_bonus_handoff": f"{TRIM_EDGES},loudnorm=I=-15:TP=-1:LRA=8",
}


def main() -> None:
    sounds = json.loads((AUDIO / "sounds.json").read_text())
    sprite: dict[str, list] = sounds["sprite"]
    for cue, loop in NEW_CUES.items():
        if cue not in sprite and (GEN / f"{cue}.mp3").exists():
            sprite[cue] = [0, 0, loop] if loop else [0, 0]
            sounds.setdefault("config", {})[cue] = {"volume": 1}
    for cue in RETIRED_CUES:
        sprite.pop(cue, None)
        sounds.get("config", {}).pop(cue, None)

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
            to_wav(gen_file, seg, loudnorm=True, af=CUE_FILTERS.get(cue))
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

    def publish(staged: Path, dest: Path) -> None:
        """Replace dest even when OneDrive briefly locks the previous file."""
        import time

        last_err: Exception | None = None
        for attempt in range(8):
            try:
                if dest.exists():
                    try:
                        dest.chmod(0o666)
                    except OSError:
                        pass
                    try:
                        dest.unlink()
                    except OSError:
                        # Fall through to replace/copy over the locked inode.
                        pass
                try:
                    staged.replace(dest)
                except OSError:
                    shutil.copy2(staged, dest)
                    staged.unlink(missing_ok=True)
                return
            except OSError as err:
                last_err = err
                time.sleep(0.4 * (attempt + 1))
        raise RuntimeError(f"could not publish {dest.name}: {last_err}")

    for name, codec in encodes.items():
        # Encode to temp then replace — avoids OneDrive/editor locks on sounds.*
        staged = tmp / name
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(master_wav), *codec,
             str(staged)])
        dest = AUDIO / name
        publish(staged, dest)
        print(f"[sprite] wrote {name} ({dest.stat().st_size // 1024} KB)")

    sounds["sprite"] = new_sprite
    staged_json = tmp / "sounds.json"
    staged_json.write_text(json.dumps(sounds, indent="\t") + "\n")
    publish(staged_json, AUDIO / "sounds.json")
    print(f"[sprite] sounds.json updated — {len(replaced)} cues replaced, {len(kept)} kept")
    print("[sprite] replaced:", ", ".join(replaced))
    shutil.rmtree(tmp, ignore_errors=True)

    # The app names two audio trees, static/assets/audio and assets/audio, and
    # the loader can read either. Today static/assets is a directory junction
    # onto assets, so the two names are one set of bytes and there is nothing to
    # copy. If that junction is ever replaced by a real folder, a rebuild that
    # touched only one side would leave the other serving the previous sprite -
    # a stale offset map read against new audio, which plays a cue as the tail
    # of its neighbour. So mirror when they are genuinely separate.
    if os.path.exists(MIRROR) and os.path.samefile(AUDIO, MIRROR):
        print("[sprite] assets/audio is the same tree as static/assets/audio (junction)")
    else:
        MIRROR.mkdir(parents=True, exist_ok=True)
        for name in (*encodes, "sounds.json"):
            shutil.copy2(AUDIO / name, MIRROR / name)
        print(f"[sprite] mirrored {len(encodes) + 1} files to {MIRROR.relative_to(APP)}")
    if kept:
        # anything here is still audio inherited from the cloned game
        print("[sprite] LEGACY LEFTOVERS (no western master):", ", ".join(kept))
        raise SystemExit(1)
    print("[sprite] no legacy segments remain — every cue has a western master")


if __name__ == "__main__":
    main()
