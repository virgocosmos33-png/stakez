"""Generate symbol masters through the Scenario API.

Reads GAME_CONFIG (threaded by game-builder regenerate_assets) so rethemes use
identity / promptContext / symbols[].name + artDirection from the active config.
Falls back to the legacy Madam Mirror set when GAME_CONFIG is unset.

Outputs land in tools/symbol_art/ as card_<id>_<slug>.png, which
repack_madam_symbols.py packs into the symbolsStatic atlas.

Usage:
    python tools/gen_symbols_mirror.py              # whole set from GAME_CONFIG
    python tools/gen_symbols_mirror.py h1 l5 me     # only these ids
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

MODEL = "model_bfl-flux-2-dev"
WIDTH = HEIGHT = 1024
OUT_DIR = Path(__file__).resolve().parent / "symbol_art"

# Legacy fallback when GAME_CONFIG is not set (Madam Mirror).
_LEGACY_STYLE = (
    "1897 Victorian gothic-horror slot symbol, single centered icon, full-bleed "
    "square plate, painterly illustration with thick dark outlines so it reads at "
    "small size, desaturated sepia and charcoal palette with cold absinthe-green "
    "rim light and faint blood-red accent, ornate antique daguerreotype card, "
    "film-grain vignette, dramatic candle-lit chiaroscuro, no text, no border "
    "frame, no watermark, high contrast, centered composition"
)
_LEGACY_SYMBOLS: dict[str, tuple[str, str]] = {
    "h1": ("card_h1_lady_mirror.png",
           "portrait of Lady Mirror, an elegant veiled Victorian medium in black lace"),
    "h2": ("card_h2_wife.png", "portrait of The Wife, a mournful Victorian widow"),
    "h3": ("card_h3_man.png", "portrait of The Man, a stern Victorian gentleman"),
    "h4": ("card_h4_young_woman.png", "portrait of The Maiden, blonde Victorian woman"),
    "h5": ("card_h5_dog.png", "portrait of The Dog, gaunt spectral black hound"),
    "l1": ("card_l1_ace.png", "ornate letter A ace playing-card rank"),
    "l2": ("card_l2_king.png", "ornate letter K king playing-card rank"),
    "l3": ("card_l3_queen.png", "ornate letter Q queen playing-card rank"),
    "l4": ("card_l4_jack.png", "ornate letter J jack playing-card rank"),
    "l5": ("card_l5_ten.png", "ornate number 10 playing-card rank"),
}


def _slug(name: str) -> str:
    s_ = re.sub(r"[^a-z0-9]+", "_", (name or "symbol").lower()).strip("_")
    return s_ or "symbol"


def _load_from_game_config() -> tuple[str, dict[str, tuple[str, str]]] | None:
    path = (os.environ.get("GAME_CONFIG") or "").strip()
    if not path or not Path(path).is_file():
        return None
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    pc = cfg.get("promptContext") or {}
    # Symbol plates need a SHORT style — full promptContext.style/extra names
    # padded walls, carts, graffiti and Flux paints entire rooms. Keep mood +
    # palette only; artDirection carries the per-symbol subject.
    palette = ", ".join(pc["palette"]) if pc.get("palette") else "#f4f1ec, #8a8680, #3a3632, #6b2a28"
    mood = pc.get("mood") or "sterile, haunted, clinical dread"
    style = (
        f"THE WHITE ROOM slot-machine symbol subject, mood {mood}, "
        f"palette {palette}, painterly illustration, thick readable edges, "
        f"ONE centered icon only filling most of the square, plain dark charcoal "
        f"void background (not a full room), no furniture, no medical cart, "
        f"no graffiti words, no title text, no watermark, high contrast, readable at 96px. "
        f"BANNED: baked UI frames, observation-window bezels, padded-cell wall borders, "
        f"fluorescent tube housings, circular chrome medallion, silver coin ring, "
        f"Madam Mirror oval, gothic filigree, purple neon, casino gem bezel"
    )
    symbols: dict[str, tuple[str, str]] = {}
    for sym in cfg.get("symbols") or []:
        sid = str(sym.get("id") or "").lower()
        if not sid:
            continue
        name = sym.get("name") or sid.upper()
        art = (sym.get("artDirection") or "").strip()
        kind = sym.get("kind") or "symbol"
        # Frame chrome is a SEPARATE UI sprite (symbolOutlineFrame). Never bake
        # observation bezels / padded windows / medallions into the card art.
        no_frame = (
            "SUBJECT ART ONLY on a plain dark charcoal void, full-bleed icon, "
            "NO decorative frame, NO observation-window bezel, NO padded-cell wall border, "
            "NO fluorescent tube housing, NO restraint buckles, NO circular chrome medallion, "
            "NO silver coin ring, NO square plate rim — UI outline frame is applied in-engine"
        )
        if kind == "high" or sid in {"w", "me"}:
            framing = (
                f"single centered character/subject filling most of the square, {no_frame}"
            )
        elif sid == "hm":
            framing = (
                f"single centered frosted glass / observation subject icon, {no_frame}"
            )
        elif kind == "low":
            framing = (
                "single centered physical prop icon filling most of the square on a dark "
                f"charcoal void, NOT a letter or card rank, sterile white/silver/grey medical item, "
                f"{no_frame}"
            )
        elif kind == "scatter":
            framing = f"single centered emblem icon on dark void, {no_frame}"
        else:
            framing = f"single centered emblem, {no_frame}"
        subject = (
            f"{name} ({sid.upper()} {kind} symbol): {art}. Composition: {framing}"
            if art
            else f"{name} ({sid.upper()}). Composition: {framing}"
        )
        filename = f"card_{sid}_{_slug(name)}.png"
        symbols[sid] = (filename, subject)
    if not symbols:
        return None
    print(f"gen_symbols_mirror: loaded {len(symbols)} symbols from GAME_CONFIG={path}")
    return style, symbols


_loaded = _load_from_game_config()
STYLE = _loaded[0] if _loaded else _LEGACY_STYLE
SYMBOLS = _loaded[1] if _loaded else _LEGACY_SYMBOLS


def generate_one(symbol_id: str, filename: str, subject: str) -> Path:
    prompt = f"{subject}. {STYLE}"
    job = s.request(
        "POST",
        f"/generate/custom/{MODEL}",
        {"prompt": prompt, "width": WIDTH, "height": HEIGHT, "numOutputs": 1},
    )
    job_id = job.get("job", {}).get("jobId") or job.get("jobId")
    if not job_id:
        raise RuntimeError(f"{symbol_id}: no jobId in response: {job}")
    print(f"{symbol_id}: job {job_id} submitted, polling...")

    result = s.wait_for_job(job_id)
    job_data = result.get("job", result)
    if job_data.get("status") != "success":
        raise RuntimeError(f"{symbol_id}: job {job_data.get('status')}: {job_data}")

    asset_ids = job_data.get("metadata", {}).get("assetIds") or []
    if not asset_ids:
        raise RuntimeError(f"{symbol_id}: job success but no assetIds: {job_data}")

    asset = s.request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
    url = asset.get("url")
    if not url:
        raise RuntimeError(f"{symbol_id}: asset {asset_ids[0]} has no url")

    dest = OUT_DIR / filename
    s.download(url, dest)
    print(f"{symbol_id}: saved {dest}")
    return dest


def _compose_low_fallback(sid: str) -> Path | None:
    """When Scenario is plan-limited, compose clinical item masters locally."""
    if sid not in {"l1", "l2", "l3", "l4", "l5"}:
        return None
    try:
        import compose_white_room_item_lows as compose  # noqa: WPS433
    except Exception as err:  # noqa: BLE001
        print(f"{sid}: compose import failed: {err}")
        return None
    return compose.compose_one(sid)


if __name__ == "__main__":
    wanted = [a.lower() for a in sys.argv[1:] if not a.startswith("--")] or list(SYMBOLS.keys())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    force = "--force" in sys.argv or os.environ.get("FORCE_SYMBOL_GEN", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }
    prefer_compose = os.environ.get("SYMBOL_COMPOSE_FALLBACK", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "only",
    }
    compose_only = os.environ.get("SYMBOL_COMPOSE_FALLBACK", "").strip().lower() == "only"
    for sid in wanted:
        if sid not in SYMBOLS:
            print(f"skip unknown id {sid!r}")
            continue
        filename, subject = SYMBOLS[sid]
        dest = OUT_DIR / filename
        if dest.is_file() and not force:
            print(f"{sid}: keep existing {dest.name} (FORCE_SYMBOL_GEN=1 to regen)")
            continue
        if compose_only:
            path = _compose_low_fallback(sid)
            if path is None:
                print(f"{sid}: no compose fallback")
            continue
        ok = False
        last_err = None
        for attempt in range(1, 4):
            try:
                generate_one(sid, filename, subject)
                ok = True
                break
            except Exception as error:  # noqa: BLE001
                last_err = error
                print(f"{sid}: attempt {attempt} failed: {error}")
                if attempt < 3:
                    time.sleep(10 * attempt)
        if not ok and (prefer_compose or (last_err and "429" in str(last_err)) or (last_err and "PlanLimit" in str(last_err))):
            print(f"{sid}: falling back to local item compose")
            _compose_low_fallback(sid)
        time.sleep(2)
    print("done")
