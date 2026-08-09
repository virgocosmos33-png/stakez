"""Fill leftover audio cues when Scenario cannot regenerate them.

Madam Mirror path: recombine seance stems (legacy).
THE WHITE ROOM path: recombine ONLY masters already stamped in
manifest_white_room.json (sterile asylum DNA) so Madam-era gothic never
re-enters the Howler sprite. Stamps composed cues into the WR manifest.

Run:  python tools/compose_missing_cues.py
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
GEN = APP / "assets-raw" / "audio_gen"
AUDIO = APP / "static" / "assets" / "audio"
MANIFEST = GEN / "manifest_white_room.json"
SOUNDS_JSON = AUDIO / "sounds.json"

TMP = Path(tempfile.mkdtemp(prefix="wr_cues_"))

SKIP = {"sfx_ui_click", "sfx_ui_click_soft", "sfx_ui_click_heavy"}


def run(args: list[str]) -> None:
    result = subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {' '.join(args[:8])}\n{result.stderr[-600:]}")


def gen(cue: str) -> Path:
    return GEN / f"{cue}.mp3"


def pitch(factor: float) -> str:
    return f"asetrate=44100*{factor},aresample=44100,atempo={1 / factor:.6f}"


def compose(cue: str, inputs: list[Path], flt: str, duration: float) -> None:
    for source in inputs:
        if not source.exists():
            raise FileNotFoundError(f"missing stem {source.name} for {cue}")
    args: list[str] = []
    for source in inputs:
        args += ["-i", str(source)]
    full = f"{flt},atrim=0:{duration},apad=whole_dur={duration}[out]"
    args += ["-filter_complex", full, "-map", "[out]", "-b:a", "192k", str(GEN / f"{cue}.mp3")]
    run(args)
    print(f"[cue] {cue} ({duration}s)", flush=True)


def stamp(manifest: dict, cue: str, note: str) -> None:
    manifest[cue] = {
        "file": f"{cue}.mp3",
        "model": "compose_wr_stems",
        "theme": "the_white_room",
        "note": note,
    }


def compose_white_room_gaps() -> None:
    manifest: dict = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text())
    sprite = set(json.loads(SOUNDS_JSON.read_text()).get("sprite", {}))
    missing = sorted(sprite - set(manifest) - SKIP)
    if not missing:
        # Still stamp Kenney UI clicks so they leave the gap list.
        for cue in SKIP:
            if cue in sprite and cue not in manifest and gen(cue).exists():
                stamp(manifest, cue, "kenney_cc0_sterile_ui")
        MANIFEST.write_text(json.dumps(manifest, indent=1))
        print("[cue] WR gaps: none", flush=True)
        return

    print(f"[cue] WR compose gaps: {len(missing)}", flush=True)
    for cue in missing:
        print(f"[cue] gap {cue}", flush=True)

    # Required WR stems (Scenario-generated). Fail loud if absent.
    need = [
        "sfx_btn_general",
        "sfx_scatter_reveal",
        "sfx_scatter_stop_1",
        "sfx_scatter_stop_2",
        "sfx_mirror_break",
        "sfx_youwon_panel",
        "sfx_winlevel_small",
        "sfx_winlevel_nice",
        "sfx_winlevel_substantial",
        "bgm_celeb_1",
        "bgm_celeb_3",
        "bgm_celeb_5",
        "sfx_bigwin_coinloop",
        "sfx_madams_eye",
        "sfx_xways_split",
    ]
    for cue in need:
        if not gen(cue).exists():
            raise FileNotFoundError(f"WR stem missing: {cue}.mp3 — cannot compose gaps")

    def do(cue: str, inputs: list[str], flt: str, duration: float, note: str) -> None:
        if cue not in missing and cue in manifest:
            return
        if cue not in sprite and cue not in missing:
            return
        compose(cue, [gen(c) for c in inputs], flt, duration)
        stamp(manifest, cue, note)

    # --- scatter / anticipation / FS ------------------------------------
    do(
        "sfx_scatter_stop_3",
        ["sfx_scatter_stop_2"],
        f"[0:a]{pitch(1.08)},volume=1.05",
        1.0,
        "pitch from sfx_scatter_stop_2",
    )
    do(
        "sfx_scatter_stop_4",
        ["sfx_scatter_stop_2"],
        f"[0:a]{pitch(1.16)},volume=1.05",
        1.0,
        "pitch from sfx_scatter_stop_2",
    )
    do(
        "sfx_scatter_stop_5",
        ["sfx_scatter_stop_2"],
        f"[0:a]{pitch(1.24)},volume=1.08",
        1.0,
        "pitch from sfx_scatter_stop_2",
    )
    do(
        "sfx_anticipation_start",
        ["sfx_btn_general", "sfx_scatter_reveal"],
        f"[0:a]{pitch(1.35)},volume=0.9[a];[1:a]atrim=0:0.35,volume=0.35[b];[a][b]amix=inputs=2:normalize=0",
        1.0,
        "ceramic tick + dust blip",
    )
    do(
        "sfx_anticipation",
        ["bgm_celeb_3", "sfx_madams_eye"],
        "[0:a]volume=0.85[a];[1:a]aloop=loop=-1:size=44100,volume=0.25[b];"
        "[a][b]amix=inputs=2:normalize=0,alimiter=limit=0.95",
        7.5,
        "celeb bed + eye pulse loop",
    )
    do(
        "jng_intro_fs",
        ["sfx_youwon_panel", "sfx_scatter_reveal"],
        f"[0:a]{pitch(1.05)},volume=0.95[a];[1:a]adelay=200|200,volume=0.45[b];"
        "[a][b]amix=inputs=2:normalize=0",
        2.0,
        "youwon + scatter dust",
    )
    do(
        "sfx_scatter_win",
        ["sfx_scatter_reveal", "sfx_winlevel_nice"],
        f"[0:a]volume=0.9[a];[1:a]{pitch(1.04)},adelay=400|400,volume=0.85[b];"
        "[a][b]amix=inputs=2:normalize=0",
        2.0,
        "scatter reveal + nice win",
    )
    do(
        "sfx_scatter_win_v2",
        ["sfx_scatter_reveal", "sfx_youwon_panel", "sfx_winlevel_substantial"],
        "[0:a]volume=0.85[a];[1:a]adelay=500|500,volume=0.7[b];"
        "[2:a]adelay=900|900,volume=0.55[c];"
        "[a][b][c]amix=inputs=3:normalize=0,alimiter=limit=0.96",
        3.5,
        "scatter + youwon + substantial",
    )
    do(
        "sfx_superfreespin",
        ["bgm_celeb_5", "sfx_youwon_panel", "sfx_madams_eye"],
        "[0:a]volume=0.9[a];[1:a]adelay=1800|1800,volume=0.75[b];"
        "[2:a]adelay=3200|3200,volume=0.55[c];"
        "[a][b][c]amix=inputs=3:normalize=0,alimiter=limit=0.96",
        6.0,
        "celeb5 + youwon + eye",
    )
    do(
        "sfx_fs_respins",
        ["sfx_winlevel_nice", "bgm_celeb_1"],
        f"[0:a]{pitch(1.08)},volume=0.95[a];[1:a]atrim=0:3.5,volume=0.35[b];"
        "[a][b]amix=inputs=2:normalize=0",
        3.5,
        "nice win over celeb1 bed",
    )
    do(
        "sfx_royals_landing",
        ["sfx_btn_general", "sfx_scatter_reveal"],
        f"[0:a]{pitch(1.1)},volume=0.95[a];[1:a]atrim=0:0.5,volume=0.2[b];"
        "[a][b]amix=inputs=2:normalize=0",
        1.2,
        "ceramic + dust",
    )
    do(
        "sfx_wild_explode",
        ["sfx_mirror_break", "sfx_xways_split"],
        f"[0:a]volume=1.05[a];[1:a]{pitch(0.9)},adelay=40|40,volume=0.7[b];"
        "[a][b]amix=inputs=2:normalize=0,alimiter=limit=0.97",
        1.4,
        "pane break + cell fracture",
    )
    do(
        "sfx_winlevel_end",
        ["sfx_youwon_panel"],
        f"[0:a]{pitch(0.92)},volume=0.9",
        2.0,
        "pitched youwon resolve",
    )
    do(
        "sfx_thunder",
        ["sfx_madams_eye", "sfx_mirror_break"],
        f"[0:a]{pitch(0.7)},volume=1.1[a];[1:a]adelay=120|120,volume=0.55[b];"
        "[a][b]amix=inputs=2:normalize=0,alimiter=limit=0.97",
        4.0,
        "eye boom + pane grit",
    )

    # --- multiplier kit --------------------------------------------------
    do(
        "sfx_multiplier_landing",
        ["sfx_btn_general"],
        f"[0:a]{pitch(0.88)},aecho=0.4:0.25:40:0.2,volume=1.05",
        1.0,
        "pitched ceramic stamp",
    )
    do(
        "sfx_multiplier_up",
        ["sfx_winlevel_small"],
        f"[0:a]{pitch(1.12)},volume=1.0",
        1.5,
        "rising small win",
    )
    do(
        "sfx_multiplier_update",
        ["sfx_btn_general", "sfx_winlevel_small"],
        f"[0:a]{pitch(1.2)},volume=0.8[a];[1:a]atrim=0:0.8,volume=0.55[b];"
        "[a][b]amix=inputs=2:normalize=0",
        1.6,
        "tick + ping",
    )
    do(
        "sfx_multiplier_reset",
        ["sfx_winlevel_small"],
        "[0:a]areverse,volume=0.9",
        0.6,
        "reversed small win",
    )
    do(
        "sfx_multiplier_combine_a",
        ["sfx_btn_general", "sfx_xways_split"],
        f"[0:a]{pitch(1.05)},volume=0.9[a];[1:a]atrim=0:0.6,volume=0.4[b];"
        "[a][b]amix=inputs=2:normalize=0",
        1.2,
        "ceramic + fracture",
    )
    do(
        "sfx_multiplier_combine_b",
        ["sfx_btn_general", "sfx_xways_split"],
        f"[0:a]{pitch(1.18)},volume=0.9[a];[1:a]atrim=0:0.7,{pitch(1.1)},volume=0.45[b];"
        "[a][b]amix=inputs=2:normalize=0",
        1.05,
        "brighter combine",
    )
    do(
        "sfx_multiplier_explosion_a",
        ["sfx_mirror_break"],
        f"[0:a]{pitch(1.15)},volume=1.0",
        0.8,
        "short pane pop",
    )
    do(
        "sfx_multiplier_explosion_b",
        ["sfx_mirror_break", "sfx_scatter_reveal"],
        f"[0:a]{pitch(0.92)},volume=1.05[a];[1:a]adelay=80|80,volume=0.35[b];"
        "[a][b]amix=inputs=2:normalize=0",
        2.0,
        "pane + dust",
    )
    do(
        "sfx_multiplier_explosion_c",
        ["sfx_mirror_break", "sfx_xways_split"],
        f"[0:a]{pitch(1.2)},volume=1.05[a];[1:a]{pitch(1.1)},volume=0.5[b];"
        "[a][b]amix=inputs=2:normalize=0",
        1.2,
        "pane + split",
    )
    do(
        "sfx_multiplier_win",
        ["sfx_youwon_panel", "sfx_winlevel_substantial"],
        "[0:a]volume=0.85[a];[1:a]adelay=400|400,volume=0.7[b];"
        "[a][b]amix=inputs=2:normalize=0,alimiter=limit=0.96",
        3.8,
        "youwon + substantial",
    )

    # --- celebration kit -------------------------------------------------
    do(
        "sfx_celeb_whoosh",
        ["bgm_celeb_1", "sfx_scatter_reveal"],
        "[0:a]highpass=f=400,volume=0.7[a];[1:a]volume=0.55[b];"
        "[a][b]amix=inputs=2:normalize=0",
        2.4,
        "airy celeb + dust",
    )
    do(
        "sfx_celeb_whoosh_hi",
        ["bgm_celeb_3", "sfx_scatter_reveal"],
        f"[0:a]{pitch(1.15)},highpass=f=600,volume=0.7[a];[1:a]{pitch(1.2)},volume=0.45[b];"
        "[a][b]amix=inputs=2:normalize=0",
        1.8,
        "bright whoosh",
    )
    do(
        "sfx_celeb_whoosh_lo",
        ["bgm_celeb_1", "sfx_madams_eye"],
        f"[0:a]{pitch(0.75)},lowpass=f=800,volume=0.85[a];[1:a]atrim=0:1.5,{pitch(0.65)},volume=0.35[b];"
        "[a][b]amix=inputs=2:normalize=0",
        3.0,
        "low HVAC whoosh",
    )
    do(
        "sfx_celeb_swell",
        ["bgm_celeb_3"],
        "[0:a]afade=t=in:st=0:d=1.2,volume=1.0",
        4.1,
        "celeb3 swell",
    )
    do(
        "sfx_celeb_wobble",
        ["bgm_celeb_3"],
        "tremolo=f=4.5:d=0.55,volume=1.0",
        4.0,
        "fluorescent wobble",
    )
    do(
        "sfx_celeb_buildup",
        ["bgm_celeb_5", "sfx_winlevel_substantial"],
        "[0:a]afade=t=in:st=0:d=2.0,volume=0.9[a];[1:a]adelay=2000|2000,volume=0.5[b];"
        "[a][b]amix=inputs=2:normalize=0",
        4.5,
        "celeb5 rise + hit",
    )
    do(
        "sfx_celeb_hit",
        ["sfx_madams_eye", "sfx_btn_general"],
        f"[0:a]atrim=0:1.2,volume=1.1[a];[1:a]{pitch(0.7)},adelay=40|40,volume=0.5[b];"
        "[a][b]amix=inputs=2:normalize=0",
        1.6,
        "eye punch",
    )
    do(
        "sfx_celeb_maxslam",
        ["bgm_celeb_5", "sfx_madams_eye", "sfx_mirror_break"],
        "[0:a]volume=0.85[a];[1:a]adelay=800|800,volume=0.9[b];"
        "[2:a]adelay=1200|1200,volume=0.7[c];"
        "[a][b][c]amix=inputs=3:normalize=0,alimiter=limit=0.96",
        6.6,
        "whiteout slam",
    )

    # --- tumble ladder ---------------------------------------------------
    for i in range(5):
        src = f"sfx_scatter_stop_{min(i + 1, 2) if i < 2 else min(i + 1, 5)}"
        # Prefer composed stops if present, else stop_2
        stem = src if gen(src).exists() else "sfx_scatter_stop_2"
        do(
            f"tumble_win_{i + 1}",
            [stem],
            f"[0:a]{pitch(1.0 + i * 0.09)},volume=0.95",
            1.0,
            f"pitch ladder from {stem}",
        )

    for cue in SKIP:
        if cue in sprite and cue not in manifest and gen(cue).exists():
            stamp(manifest, cue, "kenney_cc0_sterile_ui")

    MANIFEST.write_text(json.dumps(manifest, indent=1))
    still = sorted(sprite - set(manifest) - SKIP)
    print(f"[cue] WR compose done; manifest={len(manifest)} still_missing={still}", flush=True)


def compose_madam_legacy() -> None:
    """Original Madam Mirror compose path (kept for non-WR games)."""
    mirror_break = GEN / "sfx_mirror_break.mp3"
    if not mirror_break.exists():
        print("[cue] legacy: no mirror_break master; skip")
        return
    for i in range(5):
        factor = 1.0 + i * 0.055
        compose(
            f"sfx_reel_stop_{i + 1}",
            [gen("sfx_btn_general")],
            f"[0:a]{pitch(factor)},aecho=0.55:0.28:36:0.22,volume=1.1[m];[m]anull",
            0.45,
        )
    print("[cue] legacy madam compose finished")


def main() -> None:
    game = (os.environ.get("GAME_NAME") or "").strip().lower()
    if game in {"the_white_room", "white_room"} or MANIFEST.exists():
        compose_white_room_gaps()
        return
    compose_madam_legacy()


if __name__ == "__main__":
    main()
