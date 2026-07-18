"""Generate the Madam Mirror symbol set (new schema) through the Scenario API.

New symbol schema (internal IDs kept, art/theme replaced):
  Highs (characters):  H1 Lady Mirror, H2 The Wife, H3 The Man,
                       H4 The Little Girl, H5 The Dog
  Lows (playing cards): L1 Ace, L2 King, L3 Queen, L4 Jack, L5 Ten

Specials W / S / HM are left untouched by default.

Outputs land in tools/symbol_art/ as card_<id>_<name>.png (full-bleed squares),
which repack_symbols.py then packs into the symbolsStatic atlas.

Usage:
    python tools/gen_symbols_mirror.py              # generate the whole set
    python tools/gen_symbols_mirror.py h1 l5        # only these ids
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

MODEL = "model_bfl-flux-2-dev"
WIDTH = HEIGHT = 1024
OUT_DIR = Path(__file__).resolve().parent / "symbol_art"

# Shared style so every card reads as one cohesive haunted set at ~120px.
STYLE = (
    "1897 Victorian gothic-horror slot symbol, single centered icon, full-bleed "
    "square plate, painterly illustration with thick dark outlines so it reads at "
    "small size, desaturated sepia and charcoal palette with cold absinthe-green "
    "rim light and faint blood-red accent, ornate antique daguerreotype card, "
    "film-grain vignette, dramatic candle-lit chiaroscuro, no text, no border "
    "frame, no watermark, high contrast, centered composition"
)

# id -> (output filename, subject prompt)
SYMBOLS: dict[str, tuple[str, str]] = {
    # High symbols — the five characters
    "h1": ("card_h1_lady_mirror.png",
           "portrait of Lady Mirror, an elegant veiled Victorian medium in black "
           "lace, pale face with glowing white eyes behind a gauzy veil, a cracked "
           "hand mirror held to her chest, regal and menacing, the premium symbol"),
    "h2": ("card_h2_wife.png",
           "portrait of The Wife, a mournful Victorian widow in a high-collared "
           "black mourning gown, gaunt sorrowful face, a wedding ring on a chain, "
           "tears of dark ichor, ghostly and elegant"),
    "h3": ("card_h3_man.png",
           "portrait of The Man, a stern Victorian gentleman in a black frock coat "
           "and top hat, cold hollow eyes, faint seance rope burn on his neck, "
           "aristocratic and sinister"),
    "h4": ("card_h4_little_girl.png",
           "portrait of The Little Girl, a pale Victorian child in a lace dress "
           "holding a cracked porcelain doll, blank black eyes, unsettling faint "
           "smile, eerie and delicate"),
    "h5": ("card_h5_dog.png",
           "portrait of The Dog, a gaunt spectral black hound with glowing "
           "absinthe-green eyes and bared teeth, wispy shadow fur, a Victorian "
           "collar, loyal but menacing familiar"),
    # Low symbols — ornate haunted playing-card ranks
    "l1": ("card_l1_ace.png",
           "ornate letter A ace playing-card rank, single large gothic serif 'A' "
           "with a small carved spade beneath it, engraved antique silver filigree, "
           "haunted parlor card"),
    "l2": ("card_l2_king.png",
           "ornate letter K king playing-card rank, single large gothic serif 'K' "
           "with a small tarnished crown above it, engraved antique silver "
           "filigree, haunted parlor card"),
    "l3": ("card_l3_queen.png",
           "ornate letter Q queen playing-card rank, single large gothic serif 'Q' "
           "with a small mourning-veil motif, engraved antique silver filigree, "
           "haunted parlor card"),
    "l4": ("card_l4_jack.png",
           "ornate letter J jack playing-card rank, single large gothic serif 'J' "
           "with a small dagger motif, engraved antique silver filigree, haunted "
           "parlor card"),
    "l5": ("card_l5_ten.png",
           "ornate number 10 playing-card rank, single large gothic serif '10' "
           "engraved in antique silver filigree, haunted parlor card"),
}


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


if __name__ == "__main__":
    wanted = [a.lower() for a in sys.argv[1:]] or list(SYMBOLS.keys())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for sid in wanted:
        if sid not in SYMBOLS:
            print(f"skip unknown id {sid!r}")
            continue
        filename, subject = SYMBOLS[sid]
        for attempt in range(1, 4):
            try:
                generate_one(sid, filename, subject)
                break
            except Exception as error:  # noqa: BLE001
                print(f"{sid}: attempt {attempt} failed: {error}")
                if attempt < 3:
                    time.sleep(10 * attempt)
        time.sleep(2)
    print("done")
