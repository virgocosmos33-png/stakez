"""Compose the staged big-win celebration track (NLC-style cue-forward).

One continuous 48s composition built from the Scenario-generated win-level
stems, escalating BIG -> SUPER -> MEGA -> EPIC -> UNHOLY -> MAX WIN. Every
stage starts on an impact hit, and the 8s stages are exported as six
contiguous slices (bgm_celeb_1..6). The game plays the slice matching the
current celebration stage; advancing (naturally or by skip-click) jumps the
playhead forward to the next stage boundary, so a skip lands on the next
musical impact instead of cutting the music dead.

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
TMP = Path(tempfile.mkdtemp(prefix="celeb_track_"))


def run(args: list[str]) -> None:
    result = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {' '.join(args[:8])}\n{result.stderr[-600:]}")


def extract_hit() -> Path:
    sounds = json.loads((AUDIO / "sounds.json").read_text())
    start, duration = sounds["sprite"]["sfx_celeb_hit"][0], sounds["sprite"]["sfx_celeb_hit"][1]
    out = TMP / "hit.wav"
    run(["-ss", f"{start / 1000:.3f}", "-i", str(AUDIO / "sounds.mp3"),
         "-t", f"{duration / 1000:.3f}", "-ar", "44100", "-ac", "2", str(out)])
    return out


def main() -> None:
    hit = extract_hit()

    # stage sources; UNHOLY reuses the epic stem pitched up with extra drive
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
        # normalize each stem to exactly one stage length, hit baked on the downbeat
        chain = f"[0:a]{extra + ',' if extra else ''}atrim=0:{STAGE_SECONDS},apad=whole_dur={STAGE_SECONDS}[m];"
        chain += f"[1:a]volume={0.75 + index * 0.05:.2f}[h];"
        chain += "[m][h]amix=inputs=2:normalize=0,alimiter=limit=0.97[out]"
        run(["-i", str(GEN / f"{stem}.mp3"), "-i", str(hit),
             "-filter_complex", chain, "-map", "[out]",
             "-ar", "44100", "-ac", "2", str(out)])
        slices.append(out)
        print(f"[celeb] stage {index + 1} <- {stem}{' (unholy drive)' if extra else ''}")

    # stitch the full composition (for reference/listening) then export the
    # slices the sprite actually uses -- each slice IS the composition between
    # its stage boundaries, so hopping slices == seeking the same piece
    concat_inputs: list[str] = []
    for piece in slices:
        concat_inputs += ["-i", str(piece)]
    labels = "".join(f"[{i}:a]" for i in range(len(slices)))
    run([*concat_inputs, "-filter_complex", f"{labels}concat=n={len(slices)}:v=0:a=1[out]",
         "-map", "[out]", "-b:a", "192k", str(GEN / "bgm_celeb_full_reference.mp3")])

    for index, piece in enumerate(slices):
        run(["-i", str(piece), "-b:a", "192k", str(GEN / f"bgm_celeb_{index + 1}.mp3")])
    print(f"[celeb] wrote bgm_celeb_1..{len(slices)} + full reference to {GEN}")


if __name__ == "__main__":
    main()
