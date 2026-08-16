"""Compose every Tombstone Reborn audio cue from the Layer AI stem library.

Why this exists: the Layer forge audio surface exposes no duration control, so
ElevenLabs auto-sizes each generation (0.48s - 10s here). Rather than accept one
short clip per cue, we generated a shared western stem library once and build the
real cues from it. Sharing stems across cues is also what makes the set sound
like one library instead of unrelated one-shots.

Inputs : assets-raw/audio_stems/{stem}.mp3   (fetch_layer_stems.py)
Outputs: assets-raw/audio_gen/{cue}.mp3      (consumed by rebuild_audio_sprite.py)

Every cue here, music included, is built only from Layer AI stems. Nothing is
sliced from a pre-existing bed, which is what finally severs the cloned game's
audio lineage.

Run: python tools/build_tombstone_audio.py
Then: python tools/rebuild_audio_sprite.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
STEMS = APP / "assets-raw" / "audio_stems"
GEN = APP / "assets-raw" / "audio_gen"

SAMPLE_RATE = 44100
CHANNELS = 2
# leave headroom so rebuild_audio_sprite.py's loudnorm pass has room to work and
# the mp3 decoder never overshoots into clipping
PEAK_CEILING_DB = -1.5
PEAK_CEILING_LINEAR = 10 ** (PEAK_CEILING_DB / 20)
LIMITER = f"alimiter=limit={PEAK_CEILING_LINEAR:.4f}:level=false"
LOOP_CROSSFADE_MS = 700

# Stems ElevenLabs returned already touching or over 0dBFS. Pulling them down at
# decode time keeps the mp3 decoder's overshoot out of every cue that uses them.
HOT_STEM_TRIM_DB = -2.5
# Every stem is trimmed to start at its own onset, defined relative to its own
# peak rather than an absolute dB gate. An absolute gate cannot work across a
# library whose stems peak anywhere from -28dBFS to 0dBFS: it either leaves a
# quiet lead-in on the loud stems (so a short trim_ms window captures the
# run-up instead of the hit) or eats the quiet ones whole.
ONSET_HEADROOM_DB = 20
HOT_STEMS = {
    "thunder_crack", "revolver_shot_close", "revolver_magnum", "revolver_volley", "harmonica_breath",
    "harmonica_lick", "dust_whoosh_hi", "brass_fanfare_short", "wood_splinter_crack",
    "fire_flare", "plank_tear", "shovel_strike_a", "shovel_strike_c",
    "reel_nudge_ratchet",
}

# The music beds are sequenced on an exact grid instead of tiled, so a loop can
# never drift or smear its downbeat. 120 BPM keeps an 8s loop at a whole 4 bars.
BEAT_MS = 500

# Shortest stem allowed as SUSTAINED material inside a looping cue.
#
# Tiling advances by (stem length - crossfade), so a 1s one-shot tiled under a
# bed re-triggers every 0.75s forever. That beat is unrelated to the music grid,
# so the ear separates it out and hears a second track droning underneath the
# song rather than one continuous pad. A drone and a moaning wind tiled that way
# under bgm_main is exactly the "demonic second loop" this guard exists to stop.
# Sustained beds must come from genuinely long recordings.
MIN_SUSTAIN_STEM_MS = 6000
CROSSFADE_MS = 250


def B(beats: float) -> int:
    """Beat position -> ms on the music grid."""
    return int(round(beats * BEAT_MS))


# Semitone ratios for pitching a single plucked bass note into a bass line.
NOTE = {"D": 1.0, "C": 0.8909, "E": 1.1225, "F": 1.1892, "A": 1.3348}

# One shared set of spaces, applied to the mix, is what makes the separately
# composed cues read as a single library recorded in the same graveyard.
# in_gain and out_gain are both unity on purpose: aecho scales its whole output
# by out_gain, so the usual "0.6:0.4" style preset quietly costs 13dB of direct
# signal and leaves the sprite's loudness pass to drag the noise floor back up.
# Here the dry signal passes untouched and the reverb amount is set only by the
# decays, with the limiter catching the sum.
SPACES: dict[str, str] = {
    "yard": "aecho=1:1:70|130|210:0.30|0.17|0.09",
    "canyon": "aecho=1:1:160|330|560:0.32|0.20|0.11",
    "room": "aecho=1:1:35|70:0.18|0.09",
}


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:8])}... failed:\n{result.stderr[-1200:]}")


class Layer:
    """One stem placed on a cue's timeline."""

    def __init__(
        self,
        stem: str,
        at_ms: int = 0,
        gain_db: float = 0.0,
        trim_ms: int | None = None,
        pitch: float = 1.0,
        fade_in_ms: int = 8,
        fade_out_ms: int = 120,
        tile_ms: int | None = None,
        sustain_ms: int | None = None,
        reverse: bool = False,
    ) -> None:
        self.stem = stem
        self.at_ms = at_ms
        self.gain_db = gain_db
        self.trim_ms = trim_ms
        self.pitch = pitch
        self.fade_in_ms = fade_in_ms
        self.fade_out_ms = fade_out_ms
        self.tile_ms = tile_ms
        # sustain_ms slows one take to fill the whole bed instead of repeating
        # it, so a looping cue has no seam to re-trigger on. tile_ms is still
        # fine for one-shots, where a seam happens once and is gone.
        self.sustain_ms = sustain_ms
        self.reverse = reverse
        if tile_ms is not None and sustain_ms is not None:
            raise ValueError(f"{stem}: choose either tile_ms or sustain_ms, not both")


def L(stem: str, at_ms: int = 0, gain_db: float = 0.0, **kwargs) -> Layer:
    return Layer(stem, at_ms=at_ms, gain_db=gain_db, **kwargs)


def pulse(stem: str, beats: tuple[float, ...], gain_db: float, **kwargs) -> list[Layer]:
    """Place one stem on several grid positions.

    Rhythmic material has to be repeated on the grid rather than crossfade-tiled:
    tiling shortens each join and walks the downbeat out of time.
    """
    return [L(stem, B(beat), gain_db, **kwargs) for beat in beats]


def bass_line(notes: tuple[tuple[float, str], ...], gain_db: float) -> list[Layer]:
    """A plucked bass figure, one stem pitched to each note of the line."""
    return [
        L("bass_note_d", B(beat), gain_db, pitch=NOTE[note], fade_out_ms=90)
        for beat, note in notes
    ]


# ---------------------------------------------------------------- cue recipes
# duration_ms is the final hard length of the cue; loop cues get a tail->head
# crossfade so they repeat without a seam.
CUES: dict[str, dict] = {
    # --- signature graveyard impact (replaces the Madam-era sfx_madams_eye) ---
    "sfx_tombstone_toll": {
        "duration_ms": 2000,
        "layers": [
            L("bell_toll_iron", 0, -1),
            L("timpani_thump", 0, -3),
            L("tombstone_slam", 20, -2),
            L("gravel_pour", 160, -9, trim_ms=1400),
            L("grit_fall_light", 420, -10),
        ],
    },
    "sfx_thunder": {
        "duration_ms": 4200,
        "layers": [
            L("thunder_crack", 0, -5),
            L("thunder_rumble_deep", 60, -1),
            L("wind_gust_dry", 1300, -13),
        ],
    },
    # --- board / feature one-shots ---
    "sfx_wild_explode": {
        "duration_ms": 1450,
        "layers": [
            L("revolver_shot_close", 0, -4),
            L("smoke_hiss", 130, -11),
            L("brass_shell_drop", 190, -10, trim_ms=1000),
        ],
    },
    "sfx_multiplier_landing": {
        "duration_ms": 1100,
        "layers": [
            L("wood_knock_firm", 0, -2, trim_ms=700),
            L("brass_stab", 0, -8),
            L("grit_fall_light", 130, -13),
        ],
    },
    "sfx_multiplier_combine_a": {
        "duration_ms": 1050,
        "layers": [
            L("brass_shell_drop", 0, -3, trim_ms=850),
            L("padlock_clank", 40, -9),
        ],
    },
    "sfx_multiplier_combine_b": {
        "duration_ms": 1250,
        "layers": [
            L("padlock_clank", 0, -2),
            L("iron_bars_slam", 30, -7),
            L("gravel_pour", 160, -14, trim_ms=900),
        ],
    },
    "sfx_multiplier_explosion_a": {
        "duration_ms": 1050,
        "layers": [
            L("gunpowder_pop", 0, -1),
            L("grit_fall_light", 160, -10),
        ],
    },
    "sfx_multiplier_explosion_b": {
        "duration_ms": 2000,
        "layers": [
            L("dynamite_blast", 0, -2),
            L("wood_splinter_crack", 90, -9),
            L("gravel_pour", 260, -7),
        ],
    },
    "sfx_multiplier_explosion_c": {
        "duration_ms": 1150,
        "layers": [
            L("gunpowder_pop", 0, -3),
            L("brass_stab", 0, -7),
            L("smoke_hiss", 110, -11),
        ],
    },
    "sfx_multiplier_reset": {
        "duration_ms": 950,
        "layers": [
            L("brass_counter_ticks", 0, -2, trim_ms=600),
            L("hammer_cock", 430, -7),
        ],
    },
    "sfx_multiplier_up": {
        "duration_ms": 1700,
        "layers": [
            L("brass_ratchet_up", 0, -1),
            L("dust_whoosh_mid", 0, -13),
            L("padlock_clank", 900, -8),
        ],
    },
    "sfx_multiplier_update": {
        "duration_ms": 1650,
        "layers": [
            L("brass_counter_ticks", 0, -1),
            L("wood_knock_firm", 1050, -7, trim_ms=500),
        ],
    },
    "sfx_multiplier_win": {
        "duration_ms": 3700,
        "layers": [
            L("brass_fanfare_short", 0, -5),
            L("guitar_tremolo_dark", 0, -9),
            L("revolver_echo_distant", 700, -1),
            L("bell_accent_small", 1200, -6),
            L("brass_swell_low", 1300, -13, trim_ms=2300),
        ],
    },
    # --- anticipation ---
    "sfx_anticipation_start": {
        "duration_ms": 1400,
        "layers": [
            L("wind_gust_dry", 0, -5),
            L("low_drone_iron", 0, -7),
            L("spur_jingle", 220, -13, trim_ms=600),
        ],
    },
    "sfx_anticipation": {
        "duration_ms": 8000,
        "loop": True,
        "layers": [
            # one take stretched across the whole bed: this loops under a spin,
            # so a repeated one-shot here would beat against the music
            L("wind_moan_low", 0, -5, sustain_ms=8000, fade_out_ms=0),
            L("rope_creak", 1900, -10),
            L("rope_creak", 5300, -13, pitch=0.92),
            L("thunder_rumble_deep", 2600, -17),
        ],
    },
    # --- cell seal ---
    "sfx_cell_seal_expand": {
        "duration_ms": 2000,
        "layers": [
            L("iron_bars_slam", 0, -1),
            L("timpani_thump", 0, -9),
            L("iron_groan", 110, -7),
            L("gravel_pour", 320, -11),
        ],
    },
    "sfx_cell_seal_harden": {
        "duration_ms": 1200,
        "layers": [
            L("padlock_clank", 0, -1),
            L("chain_drag", 150, -9, trim_ms=900),
        ],
    },
    "sfx_cell_seal_h3_expand": {
        "duration_ms": 6000,
        "layers": [
            L("low_drone_iron", 0, -12, tile_ms=6000, fade_out_ms=600),
            L("iron_groan", 0, -5),
            L("chain_drag", 900, -9),
            L("iron_groan", 2100, -7, pitch=0.9),
            L("gravel_pour", 2400, -13),
            L("iron_bars_slam", 4500, -1),
            L("thunder_rumble_deep", 4500, -9),
        ],
    },
    # --- win tiers ---
    "sfx_winlevel_small": {
        "duration_ms": 1250,
        "layers": [
            L("wood_plank_thud", 0, -2, trim_ms=900),
            L("brass_stab", 40, -8, trim_ms=800),
            L("thunder_rumble_deep", 0, -14, trim_ms=1250),
        ],
    },
    "sfx_winlevel_nice": {
        "duration_ms": 1700,
        "layers": [
            L("wood_plank_thud", 0, -1, trim_ms=1100),
            L("brass_stab", 50, -7),
            L("revolver_echo_distant", 80, -6, trim_ms=900),
            L("thunder_rumble_deep", 0, -12, trim_ms=1700),
            L("chain_drag", 120, -11, trim_ms=700),
        ],
    },
    "sfx_win_ways": {
        "duration_ms": 1700,
        "layers": [
            L("wood_plank_thud", 0, -1, trim_ms=1100),
            L("brass_stab", 50, -7),
            L("revolver_echo_distant", 80, -6, trim_ms=900),
            L("thunder_rumble_deep", 0, -12, trim_ms=1700),
            L("chain_drag", 120, -11, trim_ms=700),
        ],
    },
    "sfx_winlevel_standard": {
        "duration_ms": 1450,
        "layers": [
            L("guitar_chord_accent", 0, -4, trim_ms=1250),
            L("brass_stab", 0, -12),
            L("coin_cascade_a", 160, -13),
        ],
    },
    "sfx_winlevel_substantial": {
        "duration_ms": 2900,
        "layers": [
            L("brass_fanfare_short", 0, -6),
            L("guitar_tremolo_dark", 0, -10),
            L("revolver_echo_distant", 620, -3),
            L("coin_cascade_b", 900, -9),
        ],
    },
    "sfx_winlevel_end": {
        "duration_ms": 1950,
        "layers": [
            L("harmonica_breath", 0, -6),
            L("guitar_tremolo_dark", 0, -13),
            L("grit_fall_light", 700, -12),
            L("brass_shell_drop", 900, -15, trim_ms=1000),
        ],
    },
    "sfx_youwon_panel": {
        "duration_ms": 2600,
        "layers": [
            L("wood_plank_thud", 0, -1),
            L("brass_stab", 60, -7),
            L("chain_drag", 130, -9),
            L("gravel_pour", 360, -12),
            L("grit_fall_light", 900, -14),
        ],
    },
    "sfx_bigwin_coinloop": {
        "duration_ms": 8000,
        "loop": True,
        "layers": [
            # the pour is one stretched take so it never re-triggers; the
            # individual rattles are placed on the beat so they stay in time.
            # The pour is stretched PAST the loop length and cut short, so the
            # wrap never lands on the padded silence at the end of the stretch.
            L("coin_cascade_b", 0, -6, sustain_ms=8600, fade_out_ms=0),
            # a stretch tops out at 8x, so the pour runs ~110ms short of the
            # wrap; the beat 15.5 rattle is cut off by the loop end and covers
            # that hole, which is why the tail has no gap
            *pulse("coin_cascade_a", (0, 2, 4, 6, 8, 10, 12, 14, 15.5), -9, trim_ms=900),
        ],
    },
    # --- free spin / feature entry ---
    "sfx_fs_respins": {
        "duration_ms": 3700,
        "layers": [
            L("revolver_load", 0, -3),
            L("dust_whoosh_lo", 0, -11),
            L("low_drone_iron", 600, -11, tile_ms=3000),
            L("hammer_cock", 1600, -2),
            L("brass_stab", 2000, -8),
        ],
    },
    "sfx_superfreespin": {
        "duration_ms": 5700,
        "layers": [
            L("bell_toll_iron", 0, -4),
            L("thunder_rumble_deep", 0, -9),
            L("brass_swell_low", 900, -7, trim_ms=4200),
            L("revolver_volley", 1700, -8),
            L("wind_gust_dry", 3400, -13),
            L("iron_bars_slam", 4700, -4),
        ],
    },
    "jng_intro_fs": {
        "duration_ms": 1900,
        "layers": [
            L("spur_jingle", 0, -4),
            L("harmonica_lick", 300, -7, trim_ms=1200),
            L("wood_knock_firm", 1450, -7, trim_ms=420),
        ],
    },
    # --- celebration layers ---
    "sfx_celeb_whoosh": {
        "duration_ms": 1800,
        "layers": [
            L("dust_whoosh_mid", 0, -1),
            L("dust_whoosh_lo", 110, -7),
            L("gravel_pour", 420, -16),
        ],
    },
    "sfx_celeb_whoosh_hi": {
        "duration_ms": 1200,
        "layers": [
            L("dust_whoosh_hi", 0, -4),
            L("dust_whoosh_mid", 150, -11),
        ],
    },
    "sfx_celeb_whoosh_lo": {
        "duration_ms": 2500,
        "layers": [
            L("dust_whoosh_lo", 0, -2, pitch=0.8),
            L("thunder_rumble_deep", 0, -14, trim_ms=2500),
        ],
    },
    "sfx_celeb_swell": {
        "duration_ms": 3900,
        "layers": [
            L("brass_swell_low", 0, -2, trim_ms=3900),
            L("guitar_tremolo_dark", 0, -14),
            L("timpani_roll", 2500, -8),
        ],
    },
    "sfx_celeb_wobble": {
        "duration_ms": 3900,
        "layers": [
            L("low_drone_iron", 0, -6, tile_ms=3900),
            L("iron_groan", 600, -8),
            L("brass_swell_low", 1200, -11, trim_ms=2500),
        ],
    },
    "sfx_celeb_buildup": {
        "duration_ms": 3900,
        "layers": [
            L("timpani_roll", 0, -5),
            L("drum_tom_groove", 0, -7, tile_ms=3400),
            L("brass_swell_low", 500, -4, trim_ms=3300),
            L("thunder_rumble_deep", 1800, -13),
            L("dust_whoosh_hi", 3100, -11),
        ],
    },
    "sfx_celeb_hit": {
        "duration_ms": 1800,
        "layers": [
            L("revolver_shot_close", 0, -5),
            L("timpani_thump", 0, -3),
            L("tombstone_slam", 20, -4),
            L("brass_stab", 0, -7),
            L("gravel_pour", 220, -14),
        ],
    },
    "sfx_celeb_maxslam": {
        "duration_ms": 6700,
        "layers": [
            L("thunder_crack", 0, -7),
            L("timpani_thump", 0, -4),
            L("iron_bars_slam", 0, -9),
            L("bell_toll_iron", 120, -4),
            L("brass_swell_low", 500, -5, trim_ms=5200),
            L("revolver_volley", 900, -7),
            L("thunder_rumble_deep", 2000, -7),
            L("wind_moan_low", 3900, -15, tile_ms=2800),
        ],
    },
    # --- UI: dry mechanical gunmetal, no chimes ---
    "sfx_ui_click": {
        "duration_ms": 250,
        "layers": [L("hammer_cock", 0, -2, trim_ms=240)],
    },
    "sfx_ui_click_soft": {
        "duration_ms": 400,
        "layers": [
            L("spur_jingle", 0, -4, trim_ms=380),
            L("grit_fall_light", 0, -12),
        ],
    },
    "sfx_ui_click_heavy": {
        "duration_ms": 700,
        "layers": [
            L("wood_knock_firm", 0, -2, trim_ms=600),
            L("padlock_clank", 0, -9),
        ],
    },
    "sfx_btn_general": {
        "duration_ms": 700,
        "layers": [
            L("hammer_cock", 0, -3, trim_ms=650),
            L("wood_knock_firm", 0, -11, trim_ms=500),
        ],
    },
    "sfx_btn_spin": {
        "duration_ms": 1000,
        "layers": [
            L("revolver_load", 0, -4, trim_ms=900),
            L("spur_jingle", 0, -15, trim_ms=600),
            L("hammer_cock", 320, -2, trim_ms=650),
        ],
    },
    # --- split feature -------------------------------------------------------
    # The whole volley impact lives in ONE cue: muzzle crack on the seam, the
    # splintered bullet hole, brass sparks and the dust plume. Firing four
    # separate one-shots per volley is what turns a split into a machine-gun, so
    # the layers are baked in and the volley rule stays one hit per volley.
    # The SHOOTING sound: a CLEAN pistol gunshot, nothing else. Every hit on a
    # multiplier is a sheriff's .45 revolver/magnum firing — its OWN dedicated
    # Layer AI take (revolver_magnum), separate from revolver_shot_close so the
    # bullet hit has a distinct, heavier gun than the wild-explode crack. Just
    # the gunpowder blast with a faint barrel-smoke tail. NO wood splinter,
    # knock, gravel or grit: those "debris" layers made it read as something
    # thudding into wood instead of a gun going off. This is the pistol, period.
    "sfx_bullet_wood": {
        "duration_ms": 1100,
        "layers": [
            L("revolver_magnum", 0, 0),
            L("smoke_hiss", 140, -17),
        ],
    },
    # The FINAL round of a volley: the magnum crack that RICOCHETS off iron. The
    # iron_plaque_clang stem is literally "a bullet striking a hanging iron
    # plaque", so it carries the real metal zing; the distant echo is the whine
    # ringing away across the canyon. This cue plays ALONE on the last shot.
    "sfx_bullet_ricochet": {
        "duration_ms": 1700,
        "layers": [
            L("revolver_shot_close", 0, -3),
            L("iron_plaque_clang", 20, -4),
            L("revolver_echo_distant", 90, -2),
            L("brass_sparks", 120, -11),
            L("smoke_hiss", 170, -14),
            L("grit_fall_light", 600, -17),
        ],
    },
    "sfx_split_seam_tear": {
        "duration_ms": 1600,
        "layers": [
            L("plank_tear", 0, -2),
            L("wood_splinter_crack", 60, -7),
            L("iron_groan", 100, -12),
            L("gravel_pour", 400, -15, trim_ms=1000),
        ],
    },
    # --- fire on linked cells / reel edges -----------------------------------
    "sfx_fire_ignite": {
        "duration_ms": 1100,
        "layers": [
            L("fire_ignite", 0, -2),
            L("gunpowder_pop", 0, -10),
            L("fire_flare", 60, -8),
            L("smoke_hiss", 300, -14),
        ],
    },
    "sfx_fire_loop": {
        "duration_ms": 4000,
        "loop": True,
        "layers": [
            L("fire_loop_bed", 0, -4, sustain_ms=4000, fade_out_ms=0),
            L("fuse_crackle", 0, -15, sustain_ms=4000, fade_out_ms=0),
            L("wind_moan_low", 0, -21, sustain_ms=4000, fade_out_ms=0),
        ],
    },
    "sfx_fire_flare": {
        "duration_ms": 900,
        "layers": [
            L("fire_flare", 0, -3),
            L("ember_whoosh", 0, -10, trim_ms=900),
        ],
    },
    "sfx_fire_out": {
        "duration_ms": 1800,
        "layers": [
            L("fire_burnout", 0, -2),
            L("smoke_hiss", 150, -9),
            L("grit_fall_light", 500, -13),
        ],
    },
    # --- target lock ---------------------------------------------------------
    "sfx_lock_snap": {
        "duration_ms": 700,
        "layers": [
            L("gunsight_snap", 0, -1),
            L("padlock_clank", 0, -12, trim_ms=500),
            L("brass_stab", 0, -16),
        ],
    },
    "sfx_lock_release": {
        "duration_ms": 500,
        # the quietest stem in the library, so it is the one cue that needs gain
        # rather than attenuation to sit with the rest
        "layers": [
            L("gunsight_release", 0, 8),
            L("grit_fall_light", 60, -8),
        ],
    },
    # --- clone / link charge -------------------------------------------------
    "sfx_fuse_crackle": {
        "duration_ms": 1700,
        "layers": [
            L("fuse_crackle", 0, -3, trim_ms=1700),
            L("gunpowder_pop", 1400, -12),
        ],
    },
    "sfx_ember_whoosh": {
        "duration_ms": 1300,
        "layers": [
            L("ember_whoosh", 0, -2, trim_ms=1300),
            L("dust_whoosh_hi", 0, -12),
            L("fire_flare", 100, -14),
        ],
    },
    # --- feature events ------------------------------------------------------
    "sfx_reel_nudge": {
        "duration_ms": 900,
        "layers": [
            L("reel_nudge_ratchet", 0, -2, trim_ms=900),
            L("wood_knock_firm", 0, -10, trim_ms=500),
        ],
    },
    # The accent as the bonus-entry banner lets go into the bought spin. Built
    # from stems rather than drawn whole: the model would only ever return a bare
    # click for this, eight draws of it, with the dust tail the banner needs
    # missing every time. The two entry stings either side of it are whole Layer
    # takes (tools/fetch_bonus_entry_sfx.py) — this one cue is composed.
    "sfx_bonus_handoff": {
        "duration_ms": 1500,
        "layers": [
            L("hammer_cock", 0, -1),
            L("grit_fall_light", 130, -5),
            L("dust_whoosh_lo", 170, -13),
        ],
    },
    "sfx_gunsmoke": {
        "duration_ms": 1800,
        "layers": [
            L("revolver_shot_close", 0, -3),
            L("smoke_hiss", 140, -7),
            L("dust_whoosh_mid", 200, -13),
            L("brass_shell_drop", 400, -14, trim_ms=1200),
        ],
    },
    "sfx_tombstone_open": {
        "duration_ms": 2400,
        "layers": [
            L("stone_slab_grind", 0, -2),
            L("coffin_lid_creak", 200, -8),
            L("iron_groan", 400, -14),
            L("gravel_pour", 900, -12),
            L("grit_fall_light", 1500, -14),
        ],
    },
    "sfx_special_hit": {
        "duration_ms": 1300,
        "layers": [
            L("iron_plaque_clang", 0, -1),
            L("revolver_shot_close", 0, -10),
            L("bell_accent_small", 60, -8),
        ],
    },
    "sfx_bounty": {
        "duration_ms": 2600,
        "layers": [
            L("brass_sting_celeb", 0, -2),
            L("bell_accent_small", 100, -10),
            L("coin_cascade_a", 200, -10),
            L("spur_jingle", 600, -15),
        ],
    },
    # --- digUp: the shovel planting itself in a cell -------------------------
    # Three genuinely different strikes (different source takes, not one clip
    # repitched) so staggered multi-cell digs never sound copy-pasted. The
    # handle shiver is a separate event-level accent, fired once after the last
    # blade lands rather than once per cell.
    "sfx_shovel_strike_1": {
        "duration_ms": 1500,
        "layers": [
            L("shovel_strike_a", 0, -1),
            L("wood_splinter_crack", 20, -9),
            L("bell_accent_small", 30, -11),
            L("gravel_pour", 180, -13, trim_ms=1100),
            L("grit_fall_light", 600, -15),
        ],
    },
    "sfx_shovel_strike_2": {
        "duration_ms": 1400,
        "layers": [
            L("shovel_strike_b", 0, -1),
            L("wood_knock_firm", 0, -8, trim_ms=500),
            L("bell_accent_small", 30, -13, pitch=1.08),
            L("gravel_pour", 160, -14, trim_ms=1000),
            L("grit_fall_light", 550, -16),
        ],
    },
    "sfx_shovel_strike_3": {
        "duration_ms": 1450,
        "layers": [
            L("shovel_strike_c", 0, -1, pitch=0.94),
            L("wood_splinter_crack", 25, -10, pitch=0.9),
            L("bell_accent_small", 40, -12, pitch=0.92),
            L("gravel_pour", 200, -13, trim_ms=1050),
            L("grit_fall_light", 620, -15),
        ],
    },
    "sfx_shovel_settle": {
        "duration_ms": 700,
        "layers": [
            L("shovel_handle_shiver", 0, -2),
            L("grit_fall_light", 120, -12),
        ],
    },
    # --- symbol landings -----------------------------------------------------
    "sfx_symbols_landing": {
        "duration_ms": 600,
        "layers": [
            L("wood_plank_thud", 0, -4, trim_ms=560),
            L("grit_fall_light", 60, -16),
        ],
    },
    "sfx_royals_landing": {
        "duration_ms": 600,
        "layers": [
            L("wood_knock_firm", 0, -4, trim_ms=560),
            L("grit_fall_light", 60, -17),
        ],
    },
    # --- scatter (the tombstone symbol): the iron bell is its voice ----------
    "sfx_scatter_reveal": {
        "duration_ms": 1600,
        "layers": [
            L("bell_toll_iron", 0, -3),
            L("brass_stab", 0, -10),
            L("dust_whoosh_hi", 100, -13),
            L("grit_fall_light", 500, -15),
        ],
    },
    "sfx_scatter_win": {
        "duration_ms": 2200,
        "layers": [
            L("bell_toll_iron", 0, -4),
            L("brass_sting_celeb", 100, -5),
            L("coin_cascade_a", 400, -13),
            L("spur_jingle", 900, -16),
        ],
    },
    "sfx_scatter_win_v2": {
        "duration_ms": 3000,
        "layers": [
            L("bell_toll_iron", 0, -5),
            L("timpani_thump", 0, -8),
            L("brass_fanfare_short", 100, -6),
            L("coin_cascade_b", 600, -11),
            L("revolver_echo_distant", 1400, -6),
        ],
    },
    **{
        f"sfx_scatter_stop_{index}": {
            "duration_ms": 900,
            "layers": [
                L("bell_toll_iron", 0, -4, trim_ms=850, pitch=pitch),
                L("wood_plank_thud", 0, -9, trim_ms=600),
                L("grit_fall_light", 80, -16),
            ],
        }
        for index, pitch in enumerate((1.0, 1.06, 1.12, 1.19, 1.26), start=1)
    },
    # --- reel stops: the most-heard cue in the game, one wooden family on a
    # rising pitch ladder so reel 1..5 read as the same board being struck ---
    **{
        f"sfx_reel_stop_{index}": {
            "duration_ms": 600,
            "layers": [
                L("wood_plank_thud", 0, -3, trim_ms=560, pitch=pitch),
                L("padlock_clank", 0, -15, trim_ms=500),
                L("grit_fall_light", 70, -15),
            ],
        }
        for index, pitch in enumerate((1.0, 1.05, 1.11, 1.17, 1.24), start=1)
    },
    # --- cascade / tumble ticks: one stem, rising pitch across the set ---
    **{
        f"tumble_win_{index}": {
            "duration_ms": 900,
            "layers": [
                L("brass_shell_drop", 0, -3, trim_ms=800, pitch=pitch),
                *([L("coin_cascade_a", 0, -15)] if index >= 4 else []),
            ],
        }
        for index, pitch in enumerate((1.0, 1.06, 1.13, 1.2, 1.28), start=1)
    },
}

# --- music beds are NOT built here ------------------------------------------
# bgm_main and bgm_celeb_1..6 are finished tracks, not cues assembled from
# stems, and they live in assets-raw/audio_gen as whole files:
#
#   bgm_main      the player's own loop1 (18.22s) - the base bed they asked for
#   bgm_celeb_*   six western Layer AI beds, one take each, escalating 1 -> 6
#                 (see tools/celeb_bed_candidates.json for the draws)
#
# There is no second bed. A bgm_freespin existed for a free-spins feature this
# game does not have, and nothing could start it: the math declares no freespin
# triggers, both buy modes are one enhanced spin, and the only call sites tested
# a 'SUPERSPIN' bet mode that is not declared either. loop3 stays in
# assets-raw/music as a source, unassigned.
#
# The beds were briefly sequenced from one-second stems here. That is what put a
# tiled drone and a moaning wind under the base music, re-triggering every
# 0.75s against a 0.5s beat, which is the "second demonic track" the player
# heard over their song. Music does not get composed from one-shots: leave
# these files alone and let rebuild_audio_sprite.py pick them up as they are.
# Regenerate the celebration stages with tools/fetch_celeb_beds.py.

SPACE_BY_CUE: dict[str, tuple[str, ...]] = {
    "yard": (
        "sfx_tombstone_toll", "sfx_wild_explode", "sfx_multiplier_landing",
        "sfx_multiplier_combine_a", "sfx_multiplier_combine_b",
        "sfx_multiplier_explosion_a", "sfx_multiplier_explosion_b",
        "sfx_multiplier_explosion_c", "sfx_cell_seal_expand", "sfx_cell_seal_harden",
        "sfx_cell_seal_h3_expand", "sfx_youwon_panel", "sfx_celeb_hit",
        "sfx_winlevel_small", "sfx_anticipation_start",
        # feature VFX all share the yard so they sit in the same space as the board
        "sfx_bullet_wood", "sfx_split_seam_tear", "sfx_fire_ignite", "sfx_fire_out",
        "sfx_fire_flare", "sfx_ember_whoosh", "sfx_reel_nudge", "sfx_gunsmoke",
        "sfx_tombstone_open", "sfx_special_hit", "sfx_bounty",
        "sfx_shovel_strike_1", "sfx_shovel_strike_2", "sfx_shovel_strike_3",
        "sfx_shovel_settle", "sfx_bonus_handoff", "sfx_symbols_landing", "sfx_royals_landing",
        "sfx_scatter_reveal",
        "sfx_scatter_stop_1", "sfx_scatter_stop_2", "sfx_scatter_stop_3",
        "sfx_scatter_stop_4", "sfx_scatter_stop_5",
    ),
    "canyon": (
        "sfx_thunder", "sfx_multiplier_win", "sfx_winlevel_nice", "sfx_winlevel_standard",
        "sfx_winlevel_substantial", "sfx_winlevel_end", "sfx_fs_respins",
        "sfx_superfreespin", "jng_intro_fs", "sfx_celeb_swell", "sfx_celeb_wobble",
        "sfx_celeb_buildup", "sfx_celeb_maxslam",
        # a ricochet is the one split sound that reads as leaving the board
        "sfx_bullet_ricochet", "sfx_scatter_win", "sfx_scatter_win_v2",
    ),
    "room": (
        "sfx_multiplier_reset", "sfx_multiplier_up", "sfx_multiplier_update",
        "tumble_win_1", "tumble_win_2", "tumble_win_3", "tumble_win_4", "tumble_win_5",
        "sfx_ui_click", "sfx_ui_click_soft", "sfx_ui_click_heavy",
        "sfx_btn_general", "sfx_btn_spin",
        "sfx_reel_stop_1", "sfx_reel_stop_2", "sfx_reel_stop_3",
        "sfx_reel_stop_4", "sfx_reel_stop_5",
        "sfx_lock_snap", "sfx_lock_release", "sfx_fuse_crackle",
    ),
}
for space_name, cue_names in SPACE_BY_CUE.items():
    for cue_name in cue_names:
        CUES[cue_name]["space"] = space_name


class Builder:
    def __init__(self, tmp: Path) -> None:
        self.tmp = tmp
        self.decoded: dict[str, Path] = {}
        self.tiled: dict[tuple[str, int], Path] = {}

    def decode(self, stem: str) -> Path:
        if stem not in self.decoded:
            source = STEMS / f"{stem}.mp3"
            if not source.exists():
                raise FileNotFoundError(f"missing stem {source} - run fetch_layer_stems.py first")
            dest = self.tmp / f"stem_{stem}.wav"
            # ElevenLabs pads the front of most clips, and often puts the loudest
            # moment well inside the clip. Trimming to the onset here is what makes
            # a layer's at_ms the moment you actually hear it, and a short trim_ms
            # window capture the hit rather than the run-up to it.
            onset_gate = peak_db(source) - ONSET_HEADROOM_DB
            chain = [
                f"silenceremove=start_periods=1:start_duration=0:start_threshold={onset_gate:.1f}dB"
            ]
            if stem in HOT_STEMS:
                chain.append(f"volume={HOT_STEM_TRIM_DB}dB")
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(source),
                 "-af", ",".join(chain),
                 "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS), "-sample_fmt", "s16", str(dest)])
            self.decoded[stem] = dest
        return self.decoded[stem]

    def tile(self, stem: str, target_ms: int) -> Path:
        """Repeat a stem past target_ms, crossfading each join so there is no click."""
        key = (stem, target_ms)
        if key in self.tiled:
            return self.tiled[key]
        source = self.decode(stem)
        current = source
        xfade = CROSSFADE_MS / 1000
        while duration_ms(current) < target_ms:
            nxt = self.tmp / f"tile_{stem}_{target_ms}_{duration_ms(current)}.wav"
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-i", str(current), "-i", str(source),
                 "-filter_complex", f"[0:a][1:a]acrossfade=d={xfade}:c1=tri:c2=tri[out]",
                 "-map", "[out]", "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS),
                 "-sample_fmt", "s16", str(nxt)])
            current = nxt
        self.tiled[key] = current
        return current

    def sustain(self, stem: str, target_ms: int) -> Path:
        """Stretch one take to fill a bed, so nothing re-triggers inside a loop.

        atempo bottoms out at 0.5, so large ratios are reached by chaining it.
        Beds are noise-like (wind, fire, coins), which is the material that
        survives heavy stretching without smearing into artefacts.
        """
        key = (stem, -target_ms)
        if key in self.tiled:
            return self.tiled[key]
        source = self.decode(stem)
        factor = duration_ms(source) / target_ms
        chain: list[str] = []
        remaining = factor
        while remaining < 0.5:
            chain.append("atempo=0.5")
            remaining /= 0.5
        if remaining < 1.0:
            chain.append(f"atempo={remaining:.6f}")
        chain.append("anull" if not chain else "dynaudnorm=f=250:g=15:p=0.85:m=6")
        dest = self.tmp / f"sustain_{stem}_{target_ms}.wav"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(source),
             "-af", ",".join(chain), "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS),
             "-sample_fmt", "s16", str(dest)])
        self.tiled[key] = dest
        return dest

    def layer_source(self, layer: Layer) -> Path:
        if layer.sustain_ms is not None:
            return self.sustain(layer.stem, layer.sustain_ms)
        if layer.tile_ms is not None:
            return self.tile(layer.stem, layer.tile_ms)
        return self.decode(layer.stem)

    def layer_chain(self, layer: Layer, source: Path) -> str:
        """Filter chain for one layer: pitch, trim, fades, gain, timeline offset."""
        chain: list[str] = []
        if layer.reverse:
            chain.append("areverse")
        if layer.pitch != 1.0:
            chain += [f"asetrate={int(SAMPLE_RATE * layer.pitch)}", f"aresample={SAMPLE_RATE}"]
        effective_ms = duration_ms(source) / layer.pitch
        if layer.trim_ms is not None:
            effective_ms = min(effective_ms, layer.trim_ms)
            chain += [f"atrim=0:{layer.trim_ms / 1000:.4f}", "asetpts=N/SR/TB"]
        if layer.fade_out_ms:
            fade = min(layer.fade_out_ms, effective_ms * 0.5)
            chain.append(
                f"afade=t=out:st={(effective_ms - fade) / 1000:.4f}:d={fade / 1000:.4f}:curve=tri"
            )
        if layer.fade_in_ms:
            chain.append(f"afade=t=in:st=0:d={min(layer.fade_in_ms, effective_ms * 0.4) / 1000:.4f}")
        chain.append(f"volume={layer.gain_db}dB")
        if layer.at_ms:
            chain.append(f"adelay={layer.at_ms}|{layer.at_ms}")
        return ",".join(chain)

    def compose(self, name: str, spec: dict) -> Path:
        duration_ms_target = spec["duration_ms"]
        is_loop = bool(spec.get("loop"))
        # a loop is rendered longer than the target, then the tail is folded back
        render_ms = duration_ms_target + (LOOP_CROSSFADE_MS if is_loop else 0)

        inputs: list[str] = []
        filters: list[str] = []
        labels: list[str] = []
        for index, layer in enumerate(spec["layers"]):
            source = self.layer_source(layer)
            inputs += ["-i", str(source)]
            filters.append(f"[{index}:a]" + self.layer_chain(layer, source) + f"[l{index}]")
            labels.append(f"[l{index}]")

        mix = (
            "".join(labels)
            + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0[mixed]"
        )
        # apad first so the reverb tail has room to decay instead of being cut,
        # and so the rendered file lands on exactly the declared sprite duration
        space = SPACES[spec["space"]] if spec.get("space") else None
        tail = (
            f"[mixed]apad=whole_dur={render_ms / 1000:.4f}"
            + (f",{space}" if space else "")
            + f",atrim=0:{render_ms / 1000:.4f},asetpts=N/SR/TB,{LIMITER}[out]"
        )
        staged = self.tmp / f"cue_{name}.wav"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
             "-filter_complex", ";".join([*filters, mix, tail]), "-map", "[out]",
             "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS), "-sample_fmt", "s16", str(staged)])

        if is_loop:
            staged = self.fold_loop(name, staged, duration_ms_target)
        else:
            faded = self.tmp / f"cue_{name}_faded.wav"
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(staged),
                 "-af", f"afade=t=out:st={(duration_ms_target - 90) / 1000:.4f}:d=0.09",
                 "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS), "-sample_fmt", "s16", str(faded)])
            staged = faded
        return staged

    def fold_loop(self, name: str, source: Path, target_ms: int) -> Path:
        """Crossfade the overrun tail back over the head so the cue loops cleanly."""
        head = self.tmp / f"loop_{name}_head.wav"
        tail = self.tmp / f"loop_{name}_tail.wav"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(source),
             "-t", f"{target_ms / 1000:.4f}", "-c:a", "pcm_s16le", str(head)])
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss",
             f"{target_ms / 1000:.4f}", "-i", str(source), "-c:a", "pcm_s16le", str(tail)])
        folded = self.tmp / f"loop_{name}.wav"
        # tail is faded in over the head's opening so start and end match
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-i", str(head), "-i", str(tail), "-filter_complex",
             f"[1:a]afade=t=in:st=0:d={LOOP_CROSSFADE_MS / 1000:.4f}[t];"
             f"[0:a][t]amix=inputs=2:normalize=0:dropout_transition=0[m];"
             f"[m]atrim=0:{target_ms / 1000:.4f},asetpts=N/SR/TB,{LIMITER}[out]",
             "-map", "[out]", "-ar", str(SAMPLE_RATE), "-ac", str(CHANNELS),
             "-sample_fmt", "s16", str(folded)])
        return folded


def peak_db(path: Path) -> float:
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af",
         "astats=measure_overall=Peak_level:measure_perchannel=none", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    for line in result.splitlines():
        if "Peak level dB" in line:
            return float(line.split()[-1])
    raise RuntimeError(f"could not measure peak of {path}")


def duration_ms(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    ).stdout.strip()
    return float(out) * 1000 if out else 0.0


def encode(source: Path, dest: Path) -> None:
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(source),
         "-c:a", "libmp3lame", "-b:a", "192k", str(dest)])


def check_sustained_beds(builder: Builder) -> None:
    """Refuse to tile a bed inside a looping cue.

    A looping cue repeats forever, so a tile seam inside it re-triggers forever
    too, at (stem length - crossfade). That period has nothing to do with the
    music grid, so the ear pulls it out of the mix and hears a second track
    droning under the song. Beds in loops must be stretched, not repeated.
    """
    offenders: list[str] = []
    for name, spec in CUES.items():
        if not spec.get("loop"):
            continue
        for layer in spec["layers"]:
            if layer.tile_ms is None:
                continue
            usable = duration_ms(builder.decode(layer.stem))
            advance = (usable - CROSSFADE_MS) / 1000
            offenders.append(
                f"{name}: '{layer.stem}' ({usable / 1000:.2f}s) tiled -> re-triggers"
                f" every {advance:.2f}s forever; use sustain_ms instead"
            )
    if offenders:
        raise SystemExit("tiled bed inside a looping cue:\n  " + "\n  ".join(offenders))


def main() -> None:
    GEN.mkdir(parents=True, exist_ok=True)
    # Naming cues on the command line rebuilds just those, so tuning one loop
    # does not mean re-encoding all eighty.
    wanted = set(sys.argv[1:])
    unknown = wanted - set(CUES)
    if unknown:
        raise SystemExit(f"unknown cue(s): {', '.join(sorted(unknown))}")
    tmp = Path(tempfile.mkdtemp(prefix="tombstone_audio_"))
    builder = Builder(tmp)
    report: dict[str, float] = {}
    try:
        check_sustained_beds(builder)
        for name, spec in CUES.items():
            if wanted and name not in wanted:
                continue
            staged = builder.compose(name, spec)
            encode(staged, GEN / f"{name}.mp3")
            report[name] = duration_ms(GEN / f"{name}.mp3")
            kind = "bgm" if name.startswith("bgm_") else "cue"
            print(f"[{kind}] {name:28} {report[name]:7.0f} ms  ({len(spec['layers'])} layers)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    manifest_path = GEN / "manifest_layer_build.json"
    # a partial rebuild must not erase the record of the cues it skipped
    previous: dict[str, float] = {}
    if wanted and manifest_path.is_file():
        previous = json.loads(manifest_path.read_text(encoding="utf-8")).get("cues", {})
    manifest_path.write_text(
        json.dumps({"cues": {**previous, **report}}, indent=2), encoding="utf-8"
    )
    print(f"\n[done] {len(report)} cues written to {GEN}")


if __name__ == "__main__":
    main()
