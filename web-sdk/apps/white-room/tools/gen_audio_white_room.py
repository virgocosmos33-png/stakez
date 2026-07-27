"""Generate THE WHITE ROOM themed audio cues via Scenario (ElevenLabs).

Asylum / sterile-horror tone — NOT Madam Mirror gothic. Downloads mp3s into
assets-raw/audio_gen/ for rebuild_audio_sprite.py.

Covers config.audio.cues PLUS every remaining Howler sprite cue still absent
from manifest_white_room.json (P2 Madam-era wipe).

Run:  python tools/gen_audio_white_room.py
      python tools/gen_audio_white_room.py --gaps    # only cues missing from WR manifest
      python tools/gen_audio_white_room.py --force   # overwrite all PLAN masters
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

APP = Path(__file__).resolve().parents[1]
OUT_DIR = APP / "assets-raw" / "audio_gen"
MANIFEST = OUT_DIR / "manifest_white_room.json"
SOUNDS_JSON = APP / "static" / "assets" / "audio" / "sounds.json"

MUSIC = "model_elevenlabs-music-v2"
SFX = "model_elevenlabs-sound-effects-v2"

NEG = " no gothic choir, no music box, no church organ, no victorian glass bells, no seance"

# cue -> (model, payload)
PLAN: dict[str, tuple[str, dict]] = {
    # --- music (config) --------------------------------------------------
    "bgm_main": (
        MUSIC,
        {
            "prompt": (
                "Long seamless looping background music bed for casino slot THE WHITE ROOM — "
                "feel like being INSIDE a psychiatric hospital / padded isolation ward. "
                "Ambient underscore (NOT a short stinger or SFX): continuous fluorescent tube buzz, "
                "sterile HVAC drone, distant echoing corridors, muffled metal doors, soft clinical dread pads, "
                "sparse unsettling dissonant layers, occasional remote pipe ticks. "
                "Atmosphere includes distant muffled screams, moans, unrest and patient voices far down the hall "
                "(wordless non-lyrical vocal textures only — NO sung lyrics, NO choir hymnal, NO lead vocalist). "
                "Hypnotic patient bed that leaves midrange headroom for reel SFX. "
                "60–90s evolving A/A'/B form, loop-friendly start and end matching energy, "
                "no full stops, no dramatic event hits," + NEG + "."
            ),
            "durationSeconds": 90,
            # Keep wordless distant unrest; do NOT forceInstrumental (it strips atmosphere vocals).
            "forceInstrumental": False,
            "outputFormat": "mp3_44100_192",
        },
    ),
    "bgm_freespin": (
        MUSIC,
        {
            "prompt": (
                "Long seamless looping BONUS / free-spin background music for casino slot THE WHITE ROOM "
                "(Her Side) — a special psychotic dark song, denser and more intense than the base hospital bed. "
                "Dark industrial horror underscore with asylum breakdown energy: heavier pulse, grinding low end, "
                "sharper fluorescent flicker textures, denser dissonant layers, colder metallic overtones, "
                "distant screams and unrest closer and more restless "
                "(wordless non-lyrical only — NO sung lyrics, NO choir, NO lead vocalist). "
                "Still a usable continuous slot BGM loop (NOT a short SFX stinger), unmistakable escalation "
                "from the sterile psych-ward base score. Seamless loop-friendly endpoints, "
                "no full stops," + NEG + "."
            ),
            "durationSeconds": 90,
            "forceInstrumental": False,
            "outputFormat": "mp3_44100_192",
        },
    ),
    # Evolving celebration bed: ONE contiguous 48s instrumental score (ElevenLabs Music),
    # then compose_celeb_track.py slices into bgm_celeb_1..6 stage cues. Do NOT use SFX
    # stings here — celebration music must progress forward with each win tier.
    "bgm_celeb_full": (
        MUSIC,
        {
            "prompt": (
                "Instrumental psychological-horror asylum score for a casino slot win celebration. "
                "One continuous 48-second piece that evolves forward through six escalating stages "
                "(about 8 seconds each), never resetting: "
                "(1) sparse fluorescent hum and muted metallic hit over a sterile sub-drone; "
                "(2) rising clinical tension pad with cold percussion pulses; "
                "(3) denser white-noise bloom and stainless metallic impacts; "
                "(4) urgent industrial pulse with fluorescent flicker buzz; "
                "(5) overexposed memory-wipe noise surge; "
                "(6) maximum whiteout obliteration with cascading metallic hits and cold industrial rumble. "
                "No vocals, no choir, no gothic organ, no music box, no pop melody. "
                "Dark cinematic film-score energy, seamless stage transitions, each stage opens on an impact."
                + NEG
            ),
            "durationSeconds": 48,
            "forceInstrumental": True,
            "outputFormat": "mp3_44100_192",
        },
    ),
    # Stage slices are produced by compose_celeb_track.py from bgm_celeb_full —
    # keep stubs out of the SFX generator so regenerate_audio cannot overwrite music with blips.

    # --- win-level beds (P2 Madam-era) -----------------------------------
    "bgm_winlevel_big": (
        SFX,
        {
            "text": "Sterile win bed loop: soft fluorescent hum swell with muted stainless pings, padded-cell dread, seamless",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "bgm_winlevel_superwin": (
        SFX,
        {
            "text": "Sterile super-win bed: denser white-noise bloom and cold metallic pulse hits, clinical, seamless loop",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "bgm_winlevel_mega": (
        SFX,
        {
            "text": "Mega-win sterile bed: bright fluorescent buzz bloom, hard ceramic/metal impacts, asylum dread loop",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "bgm_winlevel_epic": (
        SFX,
        {
            "text": "Epic-win sterile bed: cascading white-noise whiteout with stainless hits and HVAC rumble, seamless",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    "bgm_winlevel_max": (
        SFX,
        {
            "text": "Max-win sterile bed: maximum whiteout noise bloom, fluorescent flicker, industrial cold hits, loop",
            "durationSeconds": 8,
            "loop": True,
        },
    ),
    # --- ui (config) -----------------------------------------------------
    "sfx_btn_general": (
        SFX,
        {"text": "Soft ceramic tile tap UI click, sterile short tick, dry and clinical", "durationSeconds": 0.5},
    ),
    "sfx_btn_spin": (
        SFX,
        {"text": "Quick sterile whoosh with hard ceramic click, clinical UI spin press", "durationSeconds": 1},
    ),
    # --- reels (config) --------------------------------------------------
    "sfx_reel_stop_1": (
        SFX,
        {"text": "Low ceramic tile tick reel stop, dry padded-cell knock, short", "durationSeconds": 0.5},
    ),
    "sfx_reel_stop_2": (
        SFX,
        {"text": "Ceramic tile tick reel stop, slightly higher pitch, sterile short", "durationSeconds": 0.5},
    ),
    "sfx_reel_stop_3": (
        SFX,
        {"text": "Ceramic tile tick reel stop, medium pitch, clinical short", "durationSeconds": 0.5},
    ),
    "sfx_reel_stop_4": (
        SFX,
        {"text": "Ceramic tile tick reel stop, higher pitch with faint metal rim, short", "durationSeconds": 0.5},
    ),
    "sfx_reel_stop_5": (
        SFX,
        {"text": "Highest ceramic tile tick reel stop with thin metallic edge, urgent short", "durationSeconds": 0.5},
    ),
    "sfx_symbols_landing": (
        SFX,
        {"text": "Soft ceramic symbols landing thud with brief sterile room tone, short", "durationSeconds": 1.2},
    ),
    "sfx_scatter_reveal": (
        SFX,
        {
            "text": "Memory Reset scatter reveal: pale dust dissolve whoosh into cold ash hiss, clinical horror sting",
            "durationSeconds": 1.5,
        },
    ),
    # --- scatter stops / anticipation (P2) -------------------------------
    "sfx_scatter_stop_1": (
        SFX,
        {"text": "Scatter land stop 1: soft dust settle thud with faint ceramic tick, sterile short", "durationSeconds": 1.0},
    ),
    "sfx_scatter_stop_2": (
        SFX,
        {"text": "Scatter land stop 2: dust settle with slightly brighter ceramic tick, clinical short", "durationSeconds": 1.0},
    ),
    "sfx_scatter_stop_3": (
        SFX,
        {"text": "Scatter land stop 3: firmer ash hiss and ceramic tick, rising urgency, short", "durationSeconds": 1.0},
    ),
    "sfx_scatter_stop_4": (
        SFX,
        {"text": "Scatter land stop 4: sharper dust snap and metal rim tick, tense sterile short", "durationSeconds": 1.0},
    ),
    "sfx_scatter_stop_5": (
        SFX,
        {"text": "Scatter land stop 5: brightest ash snap and thin stainless edge, urgent clinical short", "durationSeconds": 1.0},
    ),
    "sfx_anticipation_start": (
        SFX,
        {"text": "Anticipation start: sudden fluorescent tube flicker buzz blip, sterile short cue", "durationSeconds": 1.0},
    ),
    "sfx_anticipation": (
        SFX,
        {
            "text": "Anticipation hold: rising fluorescent hum tension with distant heartbeat pulse, cold padded cell, ~7s",
            "durationSeconds": 7.5,
        },
    ),
    "jng_intro_fs": (
        SFX,
        {
            "text": "Free-spin intro sting: sterile white-noise bloom into cold metallic hit, clinical asylum jingle, short",
            "durationSeconds": 2.0,
        },
    ),
    "sfx_scatter_win": (
        SFX,
        {
            "text": "Scatter win confirm: ash dissolve whoosh into two cold stainless pings, sterile horror triumph",
            "durationSeconds": 2.0,
        },
    ),
    "sfx_scatter_win_v2": (
        SFX,
        {
            "text": "Scatter win v2: denser dust whiteout bloom with metallic fanfare pings, clinical celebration",
            "durationSeconds": 3.5,
        },
    ),
    "sfx_superfreespin": (
        SFX,
        {
            "text": "Super free-spin trigger: long white-noise whiteout swell, fluorescent flicker, cold industrial boom",
            "durationSeconds": 6.0,
        },
    ),
    "sfx_fs_respins": (
        SFX,
        {
            "text": "Free-spin respin award: sterile metallic ping cascade with soft HVAC bloom, clinical short bed",
            "durationSeconds": 3.5,
        },
    ),
    "sfx_royals_landing": (
        SFX,
        {"text": "High symbol land: soft porcelain medallion thud with brief fluorescent room tone, clinical", "durationSeconds": 1.2},
    ),
    "sfx_wild_explode": (
        SFX,
        {
            "text": "Wild explode: sealed-face rupture — dry porcelain crack burst then cold ash puff, sterile horror",
            "durationSeconds": 1.4,
        },
    ),
    # --- win levels (config + P2 end) ------------------------------------
    "sfx_winlevel_small": (
        SFX,
        {"text": "Small sterile win chime, single soft metallic ping in a white room, short", "durationSeconds": 1.0},
    ),
    "sfx_winlevel_nice": (
        SFX,
        {"text": "Nice win: two cold metallic pings with faint white-noise bloom, clinical", "durationSeconds": 1.5},
    ),
    "sfx_winlevel_standard": (
        SFX,
        {"text": "Standard win: metallic arpeggio of stainless hits over soft fluorescent hum bloom", "durationSeconds": 1.25},
    ),
    "sfx_winlevel_substantial": (
        SFX,
        {"text": "Substantial win: denser metallic hits and white-noise surge, sterile triumph, short", "durationSeconds": 2.5},
    ),
    "sfx_winlevel_end": (
        SFX,
        {"text": "Win level end sting: final cold metallic resolve ping with dying fluorescent hum, sterile", "durationSeconds": 2.0},
    ),
    "sfx_bigwin_coinloop": (
        SFX,
        {
            "text": "Continuous cascade of ceramic chip clinks and cold silver dust sparkles, sterile treasure loop, seamless loop",
            "durationSeconds": 15,
            "loop": True,
        },
    ),
    # --- tumble ladder (P2) ----------------------------------------------
    "tumble_win_1": (
        SFX,
        {"text": "Tumble win 1: soft ceramic chip clink, dry sterile short", "durationSeconds": 1.0},
    ),
    "tumble_win_2": (
        SFX,
        {"text": "Tumble win 2: two ceramic chip clinks slightly brighter, clinical short", "durationSeconds": 1.0},
    ),
    "tumble_win_3": (
        SFX,
        {"text": "Tumble win 3: three quick ceramic clinks with faint metal rim, sterile short", "durationSeconds": 1.0},
    ),
    "tumble_win_4": (
        SFX,
        {"text": "Tumble win 4: denser ceramic cascade clinks, rising pitch, clinical short", "durationSeconds": 1.0},
    ),
    "tumble_win_5": (
        SFX,
        {"text": "Tumble win 5: brightest ceramic cascade with thin stainless sparkle, urgent sterile short", "durationSeconds": 1.0},
    ),
    # --- multiplier kit (P2) ---------------------------------------------
    "sfx_multiplier_landing": (
        SFX,
        {"text": "Multiplier land: soft stainless stamp thud on ceramic, sterile short", "durationSeconds": 1.0},
    ),
    "sfx_multiplier_up": (
        SFX,
        {"text": "Multiplier up: rising cold metallic tick ladder, clinical short", "durationSeconds": 1.5},
    ),
    "sfx_multiplier_update": (
        SFX,
        {"text": "Multiplier update: digital CRT blip with stainless ping, sterile clinical", "durationSeconds": 1.6},
    ),
    "sfx_multiplier_reset": (
        SFX,
        {"text": "Multiplier reset: downward fluorescent power-down buzz blip, dry sterile short", "durationSeconds": 0.6},
    ),
    "sfx_multiplier_combine_a": (
        SFX,
        {"text": "Multiplier combine A: two ceramic chips magnet-snap together, sterile short", "durationSeconds": 1.2},
    ),
    "sfx_multiplier_combine_b": (
        SFX,
        {"text": "Multiplier combine B: denser ceramic snap merge with soft white-noise puff, clinical", "durationSeconds": 1.05},
    ),
    "sfx_multiplier_explosion_a": (
        SFX,
        {"text": "Multiplier explosion A: small porcelain pop burst, dry sterile short", "durationSeconds": 0.8},
    ),
    "sfx_multiplier_explosion_b": (
        SFX,
        {"text": "Multiplier explosion B: harder porcelain shatter burst with ash puff, clinical", "durationSeconds": 2.0},
    ),
    "sfx_multiplier_explosion_c": (
        SFX,
        {"text": "Multiplier explosion C: sharp stainless impact then ceramic grit spray, sterile horror", "durationSeconds": 1.2},
    ),
    "sfx_multiplier_win": (
        SFX,
        {"text": "Multiplier win: cold metallic fanfare of three pings over white-noise bloom, clinical", "durationSeconds": 3.8},
    ),
    # --- celebration kit (P2) --------------------------------------------
    "sfx_celeb_whoosh": (
        SFX,
        {"text": "Celebration whoosh: cold sterile air rush through padded corridor, clinical whoosh", "durationSeconds": 2.4},
    ),
    "sfx_celeb_whoosh_hi": (
        SFX,
        {"text": "Celebration whoosh high: brighter sterile air rush with thin fluorescent edge", "durationSeconds": 1.8},
    ),
    "sfx_celeb_whoosh_lo": (
        SFX,
        {"text": "Celebration whoosh low: deep HVAC air rush underbed, cold padded-cell whoosh", "durationSeconds": 3.0},
    ),
    "sfx_celeb_swell": (
        SFX,
        {"text": "Celebration swell: rising white-noise bloom and fluorescent hum swell, sterile dread", "durationSeconds": 4.1},
    ),
    "sfx_celeb_wobble": (
        SFX,
        {"text": "Celebration wobble: wavering fluorescent tube buzz modulation, clinical uneasy tone", "durationSeconds": 4.0},
    ),
    "sfx_celeb_buildup": (
        SFX,
        {"text": "Celebration buildup: escalating white-noise tension with metallic ticks, sterile asylum rise", "durationSeconds": 4.5},
    ),
    "sfx_celeb_hit": (
        SFX,
        {"text": "Celebration hit: hard stainless impact with short white-noise slap, clinical punch", "durationSeconds": 1.6},
    ),
    "sfx_celeb_maxslam": (
        SFX,
        {"text": "Celebration max slam: massive cold industrial boom plus ceramic shatter whiteout, sterile", "durationSeconds": 6.6},
    ),
    "sfx_thunder": (
        SFX,
        {
            "text": "Mega-win thunder: distant industrial transformer crack and fluorescent bank surge, clinical boom, no storm rain",
            "durationSeconds": 4.0,
        },
    ),
    # --- theme specific (config) -----------------------------------------
    "sfx_xways_split": (
        SFX,
        {"text": "Cell fracture split: sharp porcelain crack then cold pane snap, sterile horror", "durationSeconds": 1.2},
    ),
    "sfx_cell_seal_expand": (
        SFX,
        {
            "text": (
                "Cell Seal symbol expand hit: padded wall seal slam — heavy rubberized restraint buckle "
                "latch, observation-pane hydraulic whoosh as character fills the reel, short fluorescent "
                "tube surge, clinical horror impact, no glass shatter choir"
                + NEG
            ),
            "durationSeconds": 1.6,
        },
    ),
    "sfx_cell_seal_harden": (
        SFX,
        {
            "text": (
                "Cell Seal harden bump: tighter metal buckle cinch click with short sterile pressure hiss "
                "and cold fluorescent blip, multiplier seal strengthens, clinical short"
                + NEG
            ),
            "durationSeconds": 1.1,
        },
    ),
    "sfx_mirror_break": (
        SFX,
        {
            "text": "Observation pane glass fracture: frosted clinical glass crack and shatter, dried-blood grit, no magical chime",
            "durationSeconds": 1.5,
        },
    ),
    "sfx_madams_eye": (
        SFX,
        {
            "text": "CCTV eye blink sting: electronic shutter blink, CRT buzz blip, cold clinical boom hit",
            "durationSeconds": 2.0,
        },
    ),
    "sfx_youwon_panel": (
        SFX,
        {
            "text": "You-won panel: sterile metallic fanfare of cold pings with white-noise bloom, clinical celebration",
            "durationSeconds": 3.0,
        },
    ),
}

# Kenney CC0 UI clicks — already sterile; kept out of Scenario regen.
SKIP_SCENARIO = {"sfx_ui_click", "sfx_ui_click_soft", "sfx_ui_click_heavy"}


def find_asset_urls(job_payload: dict) -> list[str]:
    job = job_payload.get("job", job_payload)
    asset_ids = (job.get("metadata") or {}).get("assetIds") or []
    urls = []
    for asset_id in asset_ids:
        info = s.request("GET", f"/assets/{asset_id}")
        asset = info.get("asset", info)
        url = asset.get("url")
        if url:
            urls.append(url)
    return urls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="regenerate even if in WR manifest")
    parser.add_argument(
        "--gaps",
        action="store_true",
        help="only cues missing from manifest_white_room (P2 Madam-era wipe)",
    )
    parser.add_argument("--only", default="", help="comma-separated cue ids")
    args = parser.parse_args()

    force = bool(args.force)
    gaps = bool(args.gaps)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, dict] = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text())

    plan = dict(PLAN)
    if args.only:
        wanted = {c.strip() for c in args.only.split(",") if c.strip()}
        plan = {k: v for k, v in PLAN.items() if k in wanted}

    # Drop Kenney UI clicks from Scenario plan (build_ui_click_sfx owns them).
    for cue in SKIP_SCENARIO:
        plan.pop(cue, None)

    if gaps:
        # Prefer regenerating anything the Howler sprite still needs that is
        # not yet stamped in the White Room manifest.
        sprite_cues: set[str] = set()
        if SOUNDS_JSON.exists():
            sprite_cues = set(json.loads(SOUNDS_JSON.read_text()).get("sprite", {}))
        needed = (sprite_cues or set(plan)) - set(manifest) - SKIP_SCENARIO
        plan = {k: v for k, v in plan.items() if k in needed}
        # Also generate PLAN cues that have no mp3 yet even if not in sprite.
        for cue, spec in PLAN.items():
            if cue in SKIP_SCENARIO:
                continue
            if cue not in manifest and not (OUT_DIR / f"{cue}.mp3").exists():
                plan[cue] = spec

    todo = {
        cue: spec
        for cue, spec in plan.items()
        if force or cue not in manifest or not (OUT_DIR / f"{cue}.mp3").exists()
    }
    if force or gaps:
        for cue in list(todo):
            p = OUT_DIR / f"{cue}.mp3"
            if p.exists() and (force or cue not in manifest):
                p.unlink()

    print(
        f"[gen-wr] {len(todo)} cues to generate (force={force}, gaps={gaps}, "
        f"kept={len(plan) - len(todo)}, manifest={len(manifest)})",
        flush=True,
    )
    for cue in todo:
        print(f"[gen-wr] TODO {cue}", flush=True)

    if not todo:
        print("[gen-wr] nothing to do", flush=True)
        return

    # Probe once — hard 429 means compose_missing_cues must fill gaps.
    first_cue = next(iter(todo))
    first_model, first_payload = todo[first_cue]
    try:
        s.request("POST", f"/generate/custom/{first_model}", first_payload)
    except Exception as error:  # noqa: BLE001
        err = str(error)
        if "429" in err or "RateLimit" in err or "Too Many Requests" in err:
            print(
                f"[gen-wr] RATE LIMIT PROBE FAIL — deferring {len(todo)} cues to compose: {err[:200]}",
                flush=True,
            )
            print(f"[gen-wr] done: deferred; manifest={len(manifest)}", flush=True)
            return
        print(f"[gen-wr] probe non-rate error (continuing): {err[:200]}", flush=True)

    rate_limited = False
    for cue, (model, payload) in todo.items():
        if rate_limited:
            print(f"[gen-wr] SKIP {cue}: prior hard rate-limit (compose will fill)", flush=True)
            continue
        job_id = None
        for attempt in range(3):
            try:
                response = s.request("POST", f"/generate/custom/{model}", payload)
                job = response.get("job", response)
                job_id = job.get("jobId") or job.get("id")
                break
            except Exception as error:  # noqa: BLE001
                err = str(error)
                if "429" in err or "RateLimit" in err or "Too Many Requests" in err:
                    print(f"[gen-wr] HARD RATE LIMIT on {cue}: {err[:240]}", flush=True)
                    rate_limited = True
                    break
                print(f"[gen-wr] LAUNCH FAILED {cue}: {error}", flush=True)
                break
        if not job_id:
            continue
        try:
            job = s.wait_for_job(job_id, poll_seconds=5, timeout_seconds=900)
            status = job.get("job", job).get("status")
            if status != "success":
                print(f"[gen-wr] FAILED {cue}: status={status}", flush=True)
                continue
            urls = find_asset_urls(job)
            if not urls:
                print(f"[gen-wr] FAILED {cue}: no assets in job", flush=True)
                continue
            dest = OUT_DIR / f"{cue}.mp3"
            s.download(urls[0], dest)
            manifest[cue] = {"jobId": job_id, "file": dest.name, "model": model, "theme": "the_white_room"}
            MANIFEST.write_text(json.dumps(manifest, indent=1))
            print(f"[gen-wr] saved {cue} ({dest.stat().st_size // 1024} KB)", flush=True)
        except Exception as error:  # noqa: BLE001
            print(f"[gen-wr] FAILED {cue}: {error}", flush=True)

    present = sum(1 for c in PLAN if (OUT_DIR / f"{c}.mp3").exists())
    print(f"[gen-wr] done: {present}/{len(PLAN)} PLAN masters on disk; manifest={len(manifest)}", flush=True)


if __name__ == "__main__":
    main()
