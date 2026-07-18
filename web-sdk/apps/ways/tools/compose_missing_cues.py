"""Compose Madam Mirror replacements for every remaining template cue.

Scenario's creative-unit quota is exhausted, so the leftover Mining-Mayhem
sample cues are built by recombining the 25 already-generated seance stems
(glass bells, ghost choirs, antique ticks) plus the custom mirror-break /
celebration kit extracted from the current sprite. Output lands in
assets-raw/audio_gen/ so rebuild_audio_sprite.py swaps them in as replacements.

Run:  python tools/compose_missing_cues.py
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
GEN = APP / "assets-raw" / "audio_gen"
AUDIO = APP / "static" / "assets" / "audio"

TMP = Path(tempfile.mkdtemp(prefix="mirror_cues_"))


def run(args: list[str]) -> None:
    result = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {' '.join(args[:8])}\n{result.stderr[-600:]}")


def extract_from_sprite(cue: str) -> Path:
    """Pull one existing custom cue out of the shipped sprite as a wav."""
    sounds = json.loads((AUDIO / "sounds.json").read_text())
    start, duration = sounds["sprite"][cue][0], sounds["sprite"][cue][1]
    out = TMP / f"src_{cue}.wav"
    if not out.exists():
        run(["-ss", f"{start / 1000:.3f}", "-i", str(AUDIO / "sounds.mp3"),
             "-t", f"{duration / 1000:.3f}", "-ar", "44100", "-ac", "2", str(out)])
    return out


def gen(cue: str) -> Path:
    return GEN / f"{cue}.mp3"


def pitch(factor: float) -> str:
    """Pitch shift keeping duration (asetrate + atempo compensation)."""
    return f"asetrate=44100*{factor},aresample=44100,atempo={1 / factor:.6f}"


def compose(cue: str, inputs: list[Path], flt: str, duration: float) -> None:
    """filter_complex -> [out], trimmed/padded to an exact duration."""
    args: list[str] = []
    for source in inputs:
        args += ["-i", str(source)]
    full = f"{flt},atrim=0:{duration},apad=whole_dur={duration}[out]"
    args += ["-filter_complex", full, "-map", "[out]", "-b:a", "192k", str(GEN / f"{cue}.mp3")]
    run(args)
    print(f"[cue] {cue} ({duration}s)")


def main() -> None:
    mirror_break = extract_from_sprite("sfx_mirror_break")
    celeb_hit = extract_from_sprite("sfx_celeb_hit")

    # --- reels -----------------------------------------------------------
    # antique clock tick with glass resonance, pitch rising across the reels
    for i in range(5):
        factor = 1.0 + i * 0.055
        compose(
            f"sfx_reel_stop_{i + 1}",
            [gen("sfx_btn_general")],
            f"[0:a]{pitch(factor)},aecho=0.55:0.28:36:0.22,volume=1.1[m];[m]anull",
            0.45,
        )
    compose(
        "sfx_symbols_landing",
        [gen("sfx_btn_general"), gen("sfx_scatter_stop_3")],
        f"[0:a]{pitch(0.82)},volume=1.0[a];[1:a]volume=0.14[b];[a][b]amix=inputs=2:normalize=0",
        1.2,
    )
    compose(
        "sfx_royals_landing",
        [gen("sfx_btn_general"), gen("sfx_scatter_stop_2")],
        f"[0:a]{pitch(1.08)},volume=0.9[a];[1:a]volume=0.11[b];[a][b]amix=inputs=2:normalize=0",
        1.2,
    )

    # --- scatter / free spins -------------------------------------------
    compose("sfx_scatter_win", [gen("sfx_scatter_win_v2")], f"[0:a]{pitch(1.06)},volume=1.0", 2.0)
    compose(
        "sfx_superfreespin",
        [gen("jng_intro_fs"), gen("sfx_scatter_win_v2"), gen("sfx_youwon_panel")],
        f"[0:a]{pitch(0.94)},volume=1.0[a];"
        "[1:a]adelay=1200|1200,volume=0.9[b];"
        "[2:a]adelay=3200|3200,volume=0.55[c];"
        "[a][b][c]amix=inputs=3:normalize=0,alimiter=limit=0.97",
        6.0,
    )

    # --- wild / mirror ----------------------------------------------------
    compose(
        "sfx_wild_explode",
        [mirror_break, celeb_hit],
        f"[0:a]volume=1.1[a];[1:a]{pitch(0.78)},adelay=60|60,volume=0.8[b];"
        "[a][b]amix=inputs=2:normalize=0,alimiter=limit=0.97",
        1.4,
    )

    # --- win level stings: rising slices of the glass arpeggio ------------
    ladder = [
        ("sfx_winlevel_small", 0.95, 1.0),
        ("sfx_winlevel_standard", 1.0, 1.25),
        ("sfx_winlevel_nice", 1.06, 1.5),
        ("sfx_winlevel_substantial", 1.12, 2.5),
    ]
    for cue, factor, duration in ladder:
        compose(cue, [gen("sfx_multiplier_win")], f"[0:a]{pitch(factor)},volume=1.0", duration)
    compose("sfx_winlevel_end", [gen("sfx_youwon_panel")], "[0:a]volume=0.9", 2.0)

    # --- multiplier kit ----------------------------------------------------
    compose("sfx_multiplier_combine_b", [gen("sfx_multiplier_combine_a")], f"[0:a]{pitch(1.12)}", 1.05)
    explosions = [("a", 1.0, 0.8), ("b", 0.86, 2.0), ("c", 1.16, 1.2)]
    for suffix, factor, duration in explosions:
        compose(
            f"sfx_multiplier_explosion_{suffix}",
            [mirror_break, gen("sfx_scatter_reveal")],
            f"[0:a]{pitch(factor)},volume=1.05[a];[1:a]adelay=80|80,volume=0.35[b];"
            "[a][b]amix=inputs=2:normalize=0",
            duration,
        )
    compose("sfx_multiplier_reset", [gen("sfx_multiplier_up")], "[0:a]areverse,volume=0.9", 0.6)
    compose(
        "sfx_multiplier_update",
        [gen("sfx_multiplier_landing")],
        f"[0:a]{pitch(1.05)},aecho=0.5:0.3:60:0.3",
        1.6,
    )

    # --- tumble chime ladder (kept in the sprite for completeness) --------
    for i in range(5):
        factor = 1.0 + i * 0.09
        compose(
            f"tumble_win_{i + 1}",
            [gen(f"sfx_scatter_stop_{min(i + 1, 5)}")],
            f"[0:a]{pitch(factor)},volume=0.95",
            1.0,
        )

    print("[cue] all template cues recomposed")


if __name__ == "__main__":
    main()
