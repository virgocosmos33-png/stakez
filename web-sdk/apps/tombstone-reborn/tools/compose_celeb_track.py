"""Compose the staged big-win celebration track (cue-forward evolving bed).

Primary path: slice one contiguous ElevenLabs Music master
(`bgm_celeb_full.mp3` or `bgm_celeb_full_reference.mp3`) into six 8s stage
cues (`bgm_celeb_1..6` = BIG..MAX). Advancing a celebration scene — naturally
or via skip — jumps music to the next stage boundary so the bed evolves
forward instead of restarting a short FX sting.

Fallback: if no master exists, rebuild from win-level stems (legacy).

Run:  python tools/compose_celeb_track.py
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
GEN = APP / "assets-raw" / "audio_gen"
AUDIO = APP / "static" / "assets" / "audio"

STAGE_SECONDS = 8.0
STAGE_COUNT = 6
TMP = Path(tempfile.mkdtemp(prefix="celeb_track_"))


def run(args: list[str]) -> None:
    result = subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {' '.join(args[:8])}\n{result.stderr[-600:]}")


def extract_hit() -> Path:
    sounds = json.loads((AUDIO / "sounds.json").read_text())
    start, duration = sounds["sprite"]["sfx_celeb_hit"][0], sounds["sprite"]["sfx_celeb_hit"][1]
    out = TMP / "hit.wav"
    run(
        [
            "-ss",
            f"{start / 1000:.3f}",
            "-i",
            str(AUDIO / "sounds.mp3"),
            "-t",
            f"{duration / 1000:.3f}",
            "-ar",
            "44100",
            "-ac",
            "2",
            str(out),
        ]
    )
    return out


def find_master() -> Path | None:
    for name in ("bgm_celeb_full.mp3", "bgm_celeb_full_reference.mp3"):
        path = GEN / name
        if path.is_file() and path.stat().st_size > 200_000:
            return path
    return None


def slice_from_master(master: Path, hit: Path) -> None:
    """Cut contiguous 8s stages from one evolving composition (clean — no SFX bake).

    Older builds mixed Madam-era sfx_celeb_hit into every slice; that made the
    "new" bed still sound like the old celebration kit. Stage impacts live in
    the ElevenLabs master itself; FE advances by swapping bgm_celeb_N.
    """
    del hit  # kept in signature for legacy stitch_from_stems callers
    print(f"[celeb] slicing evolving master {master.name} (clean, no hit bake)")
    slices: list[Path] = []
    for index in range(STAGE_COUNT):
        out = TMP / f"stage_{index + 1}.wav"
        start = index * STAGE_SECONDS
        run(
            [
                "-ss",
                f"{start:.3f}",
                "-i",
                str(master),
                "-t",
                f"{STAGE_SECONDS:.3f}",
                "-ar",
                "44100",
                "-ac",
                "2",
                "-af",
                f"apad=whole_dur={STAGE_SECONDS},atrim=0:{STAGE_SECONDS}",
                str(out),
            ]
        )
        slices.append(out)
        print(f"[celeb] stage {index + 1} <- {start:.0f}–{start + STAGE_SECONDS:.0f}s")

    # Refresh full reference from the stamped slices (game-ready listening copy).
    concat_inputs: list[str] = []
    for piece in slices:
        concat_inputs += ["-i", str(piece)]
    labels = "".join(f"[{i}:a]" for i in range(len(slices)))
    run(
        [
            *concat_inputs,
            "-filter_complex",
            f"{labels}concat=n={len(slices)}:v=0:a=1[out]",
            "-map",
            "[out]",
            "-b:a",
            "192k",
            str(GEN / "bgm_celeb_full_reference.mp3"),
        ]
    )

    for index, piece in enumerate(slices):
        run(["-i", str(piece), "-b:a", "192k", str(GEN / f"bgm_celeb_{index + 1}.mp3")])
    print(f"[celeb] wrote bgm_celeb_1..{STAGE_COUNT} + full reference to {GEN}")


def stitch_from_stems(hit: Path) -> None:
    """Legacy fallback when no ElevenLabs master is present."""
    stages = [
        ("bgm_winlevel_big", None),
        ("bgm_winlevel_superwin", None),
        ("bgm_winlevel_mega", None),
        ("bgm_winlevel_epic", None),
        ("bgm_winlevel_epic", "asetrate=44100*1.0705,aresample=44100,atempo=0.934145,volume=1.12"),
        ("bgm_winlevel_max", None),
    ]
    slices: list[Path] = []
    for index, (stem, extra) in enumerate(stages):
        out = TMP / f"stage_{index + 1}.wav"
        chain = f"[0:a]{extra + ',' if extra else ''}atrim=0:{STAGE_SECONDS},apad=whole_dur={STAGE_SECONDS}[m];"
        chain += f"[1:a]volume={0.75 + index * 0.05:.2f}[h];"
        chain += "[m][h]amix=inputs=2:normalize=0,alimiter=limit=0.97[out]"
        run(
            [
                "-i",
                str(GEN / f"{stem}.mp3"),
                "-i",
                str(hit),
                "-filter_complex",
                chain,
                "-map",
                "[out]",
                "-ar",
                "44100",
                "-ac",
                "2",
                str(out),
            ]
        )
        slices.append(out)
        print(f"[celeb] stage {index + 1} <- {stem}{' (unholy drive)' if extra else ''}")

    concat_inputs: list[str] = []
    for piece in slices:
        concat_inputs += ["-i", str(piece)]
    labels = "".join(f"[{i}:a]" for i in range(len(slices)))
    run(
        [
            *concat_inputs,
            "-filter_complex",
            f"{labels}concat=n={len(slices)}:v=0:a=1[out]",
            "-map",
            "[out]",
            "-b:a",
            "192k",
            str(GEN / "bgm_celeb_full_reference.mp3"),
        ]
    )
    for index, piece in enumerate(slices):
        run(["-i", str(piece), "-b:a", "192k", str(GEN / f"bgm_celeb_{index + 1}.mp3")])
    print(f"[celeb] wrote bgm_celeb_1..{len(slices)} + full reference to {GEN}")


def main() -> None:
    hit = extract_hit()
    master = find_master()
    if master is not None:
        slice_from_master(master, hit)
    else:
        print("[celeb] no evolving master — falling back to win-level stems")
        stitch_from_stems(hit)


if __name__ == "__main__":
    main()
