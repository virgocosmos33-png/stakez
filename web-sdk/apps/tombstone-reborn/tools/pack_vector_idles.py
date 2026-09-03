"""Stamp the organized Desktop symbol folders onto the live atlas.

SOURCE OF TRUTH — only these three folders:
  new symbols/symbol/high paying symbols
  new symbols/symbol/low paying symbols
  new symbols/symbol/special symbols

Never HEAD painted busts. Never a restyle guess. Faces only, no plates.

Run: python tools/pack_vector_idles.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time

import shutil

from PIL import Image, ImageFilter

import _symbol_faces as faces_lib

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, ".."))
REPO = os.path.normpath(os.path.join(APP, "..", "..", ".."))
KIT = os.path.join(REPO, "VFXPACKSHEETS", "tombstone-reborn-symbols")
NEW = os.path.join(
	os.path.expanduser("~"),
	"Desktop",
	"TR2 FInal symbopls sheet",
	"TR2 FInal symbopls sheet for TR2 Symbols",
	"new symbols",
)

CELL = 300
CARD_H = 292
CARD_W = round(CARD_H * 0.775)
ATLAS = "symbolsStatic.v22"

# Island crop of the 3+2 high sheet. Mapped by character, not prop order.
ISLAND_HIGHS_DIR = os.path.join(
	os.path.expanduser("~"),
	"Documents",
	"ISLAND CROP",
	"output",
	"81fd4c81-cb0e-4b3b-83b7-8521acd7874d",
)
ISLAND_HIGHS = {
	"h1-gunslinger": "OpenAI Playground 2026-09-01 at 19.03.28.png",
	"h2-duchess": "OpenAI Playground 2026-09-01 at 19.03.23.png",
	"h3-butcher": "OpenAI Playground 2026-09-01 at 19.03.33.png",
	"h4-card-shark": "OpenAI Playground 2026-09-01 at 20.03.38.png",
	"h5-preacher": "OpenAI Playground 2026-09-01 at 19.03.48.png",
}

# Island crop of the 3+2 royal sheet. Top LTR = 10 / J / Q, bottom LTR = K / A.
ISLAND_LOWS_DIR = os.path.join(
	os.path.expanduser("~"),
	"Documents",
	"ISLAND CROP",
	"output",
	"164ab71d-a1f6-4eb8-8c24-5352c6366be5",
)
ISLAND_LOWS = {
	"l1-bullet": "prop_05.png",
	"l2-whiskey": "prop_04.png",
	"l3-spur": "prop_03.png",
	"l4-horseshoe": "prop_02.png",
	"l5-dead-mans-hand": "prop_01.png",
}
RESTYLE_LOWS = {
	"l1-bullet": "l1_ace.png",
	"l2-whiskey": "l2_king.png",
	"l3-spur": "l3_queen.png",
	"l4-horseshoe": "l4_jack.png",
	"l5-dead-mans-hand": "l5_ten.png",
}

# Sheet row1 LTR = H1-H5, row2 LTR = L1-L5, row3 LTR = W / SU / S / GS / SH.
# Island names are not left-to-right; this map is from the art.
PROP = {
	"h1-gunslinger": os.path.join("symbol", "high paying symbols", "OpenAI Playground 2026-09-01 at 03.33.35.png"),
	"h2-duchess": os.path.join("symbol", "high paying symbols", "OpenAI Playground 2026-09-01 at 03.31.16.png"),
	"h3-butcher": os.path.join("symbol", "high paying symbols", "OpenAI Playground 2026-09-01 at 03.30.59.png"),
	"h4-card-shark": os.path.join("symbol", "high paying symbols", "OpenAI Playground 2026-09-01 at 03.31.09.png"),
	"h5-preacher": os.path.join("symbol", "high paying symbols", "OpenAI Playground 2026-09-01 at 03.31.04.png"),
	"l1-bullet": os.path.join("symbol", "low paying symbols", "prop_05.png"),
	"l2-whiskey": os.path.join("symbol", "low paying symbols", "111b665c-0779-4d1e-b98e-13f226f09dd3 - Copy.png"),
	"l3-spur": os.path.join("symbol", "low paying symbols", "prop_03.png"),
	"l4-horseshoe": os.path.join("symbol", "low paying symbols", "prop_02.png"),
	"l5-dead-mans-hand": os.path.join("symbol", "low paying symbols", "111b665c-0779-4d1e-b98e-13f226f09dd3.png"),
	"w-revolver": os.path.join("symbol", "special symbols", "OpenAI Playground 2026-09-01 at 03.33.10.png"),
	"s-tombstone": os.path.join("symbol", "special symbols", "OpenAI Playground 2026-09-01 at 03.32.28.png"),
	"su-super-scatter": "prop_15.png",
	"gs-gunsmoke": os.path.join("symbol", "special symbols", "OpenAI Playground 2026-09-01 at 03.32.19.png"),
	"sh-mark": os.path.join("symbol", "special symbols", "OpenAI Playground 2026-09-01 at 03.32.39.png"),
}

READY = {
	"h1.webp": os.path.join(KIT, "h1-gunslinger", "idle.png"),
	"h2.webp": os.path.join(KIT, "h2-duchess", "idle.png"),
	"h3.webp": os.path.join(KIT, "h3-butcher", "idle.png"),
	"h4.webp": os.path.join(KIT, "h4-card-shark", "idle.png"),
	"h5.webp": os.path.join(KIT, "h5-preacher", "idle.png"),
	"l1.webp": os.path.join(KIT, "l1-bullet", "idle.png"),
	"l2.webp": os.path.join(KIT, "l2-whiskey", "idle.png"),
	"l3.webp": os.path.join(KIT, "l3-spur", "idle.png"),
	"l4.webp": os.path.join(KIT, "l4-horseshoe", "idle.png"),
	"l5.webp": os.path.join(KIT, "l5-dead-mans-hand", "idle.png"),
	"w.png": os.path.join(KIT, "w-revolver", "idle.png"),
	"s.png": os.path.join(KIT, "s-tombstone", "idle.png"),
}

FEATURE_PNGS = {
	"wr_wild.png": os.path.join(KIT, "w-revolver", "idle.png"),
	"tr_scatter.png": os.path.join(KIT, "s-tombstone", "idle.png"),
	"tr_scatter_super.png": os.path.join(KIT, "su-super-scatter", "idle.png"),
	"tr_gs.png": os.path.join(KIT, "gs-gunsmoke", "idle.png"),
	"tr_sh.png": os.path.join(KIT, "sh-mark", "idle.png"),
}

MIRROR_DIRS = [
	os.path.join(APP, "assets", "sprites", "mirror"),
	os.path.join(APP, "static", "assets", "sprites", "mirror"),
	os.path.join(APP, "assets-src", "sprites", "mirror"),
	os.path.join(APP, "assets-src", "assets", "sprites", "mirror"),
]

ATLAS_DIRS = [
    os.path.join(APP, "assets", "sprites", "symbolsStatic"),
    os.path.join(APP, "static", "assets", "sprites", "symbolsStatic"),
    os.path.join(APP, "assets-src", "assets", "sprites", "symbolsStatic"),
    os.path.join(APP, "assets-src", "sprites", "symbolsStatic"),
]
PAYTABLE_DIRS = [
    os.path.join(APP, "assets", "paytable"),
    os.path.join(APP, "static", "assets", "paytable"),
    os.path.join(APP, "assets-src", "paytable"),
    os.path.join(APP, "assets-src", "assets", "paytable"),
]
SPINE_DIRS = [
    os.path.join(APP, "assets", "spines", "mm_symbols"),
    os.path.join(APP, "static", "assets", "spines", "mm_symbols"),
    os.path.join(APP, "assets-src", "spines", "mm_symbols"),
    os.path.join(APP, "assets-src", "assets", "spines", "mm_symbols"),
]


def _atomic_save(img: Image.Image, dest: str, **kwargs) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    root, ext = os.path.splitext(dest)
    tmp = f"{root}.__tmp__{ext}"
    img.save(tmp, **kwargs)
    for attempt in range(12):
        try:
            os.replace(tmp, dest)
            return
        except OSError:
            if attempt == 11:
                raise
            time.sleep(0.4)


def alpha_crop(im: Image.Image) -> Image.Image:
    bbox = im.getchannel("A").getbbox()
    return im.crop(bbox) if bbox else im


def fit_cell(src: Image.Image, w: int = CELL, h: int = CELL) -> Image.Image:
    src = alpha_crop(src.convert("RGBA"))
    box_w = max(1, CARD_W - 12)
    box_h = max(1, CARD_H - 12)
    scale = min(box_w / src.width, box_h / src.height)
    nw = max(1, round(src.width * scale))
    nh = max(1, round(src.height * scale))
    fitted = src.resize((nw, nh), Image.LANCZOS)
    cell = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cell.paste(fitted, ((w - nw) // 2, (h - nh) // 2), fitted)
    return cell


def vertical_smear(card: Image.Image, spread: int = 26, steps: int = 9) -> Image.Image:
    out = Image.new("RGBA", card.size, (0, 0, 0, 0))
    for i in range(-steps, steps + 1):
        dy = round(i / steps * spread)
        layer = card.copy()
        fade = max(0.06, 1.0 - abs(i) / steps)
        layer.putalpha(layer.getchannel("A").point(lambda v, f=fade: int(v * f)))
        shifted = Image.new("RGBA", card.size, (0, 0, 0, 0))
        shifted.paste(layer, (0, dy), layer)
        out = Image.alpha_composite(out, shifted)
    return out.filter(ImageFilter.GaussianBlur(1.2))


PLATE_DIR = os.path.join(APP, "assets-raw", "cell_backplates")
PLATE_HIGH = os.path.join(PLATE_DIR, "plate_high.png")
PLATE_LOW = os.path.join(PLATE_DIR, "plate_low.png")
HIGHS = {"h1.webp", "h2.webp", "h3.webp", "h4.webp", "h5.webp"}
LOWS = {"l1.webp", "l2.webp", "l3.webp", "l4.webp", "l5.webp"}


def _load_plate(path: str) -> Image.Image | None:
    if not os.path.isfile(path):
        return None
    return Image.open(path).convert("RGBA")


def stack_plate(face: Image.Image, plate: Image.Image | None) -> Image.Image:
    if plate is None:
        return face
    cell = Image.new("RGBA", face.size, (0, 0, 0, 0))
    cell.alpha_composite(plate.resize(face.size, Image.LANCZOS))
    cell.alpha_composite(face)
    return cell


def load_ready() -> dict[str, Image.Image]:
    cards: dict[str, Image.Image] = {}
    for frame, path in READY.items():
        if not os.path.isfile(path):
            print(f"  skip missing {path}")
            continue
        src = Image.open(path).convert("RGBA")
        if frame in HIGHS:
            cards[frame] = faces_lib.high_cell(src)
        elif frame in LOWS:
            cards[frame] = faces_lib.card_cell(src)
        elif frame == "s.png":
            cards[frame] = faces_lib.scatter_cell(src)
        else:
            cards[frame] = fit_cell(src)
        print(f"  {os.path.basename(os.path.dirname(path)):18s} {src.size} -> {frame}")
    return cards


def stack_paying(faces: dict[str, Image.Image]) -> dict[str, Image.Image]:
    # Faces only. The wood / blood cell backboards are retired.
    return dict(faces)


def stamp_atlas(dest_dir: str, cards: dict[str, Image.Image]) -> None:
    json_path = os.path.join(dest_dir, f"{ATLAS}.json")
    webp_path = os.path.join(dest_dir, f"{ATLAS}.webp")
    png_path = os.path.join(dest_dir, f"{ATLAS}.png")
    if not os.path.isfile(json_path) or not os.path.isfile(webp_path):
        print(f"  skip atlas: {dest_dir}")
        return
    with open(json_path, encoding="utf-8") as handle:
        atlas = json.load(handle)
    sheet = Image.open(webp_path).convert("RGBA")
    n = 0
    for frame, card in cards.items():
        meta = atlas["frames"].get(frame)
        if not meta:
            continue
        box = meta["frame"]
        fitted = card if (card.width, card.height) == (box["w"], box["h"]) else card.resize(
            (box["w"], box["h"]), Image.LANCZOS
        )
        sheet.paste(fitted, (box["x"], box["y"]))
        n += 1
        blur_name = frame.replace(".", "_blur.")
        blur_meta = atlas["frames"].get(blur_name)
        if blur_meta:
            b = blur_meta["frame"]
            smear = vertical_smear(fitted)
            if smear.size != (b["w"], b["h"]):
                smear = smear.resize((b["w"], b["h"]), Image.LANCZOS)
            sheet.paste(smear, (b["x"], b["y"]))
            n += 1
    _atomic_save(sheet, webp_path, lossless=True)
    if os.path.isfile(png_path):
        _atomic_save(sheet, png_path)
    print(f"  stamped {n} frames -> {dest_dir}")


def write_paytable(cards: dict[str, Image.Image]) -> None:
    for dest in PAYTABLE_DIRS:
        if not os.path.isdir(dest) and dest != PAYTABLE_DIRS[0]:
            continue
        os.makedirs(dest, exist_ok=True)
        for frame, card in cards.items():
            _atomic_save(card, os.path.join(dest, f"{frame.split('.')[0]}.png"))
        print(f"  paytable -> {dest}")


def patch_spine(spine_dir: str, cards: dict[str, Image.Image]) -> None:
    atlas_path = os.path.join(spine_dir, "mm_symbols.atlas")
    png_path = os.path.join(spine_dir, "mm_symbols.png")
    if not os.path.isfile(atlas_path) or not os.path.isfile(png_path):
        return
    lines = open(atlas_path, encoding="utf-8").read().splitlines()
    sheet = Image.open(png_path).convert("RGBA")
    n = 0
    for i, line in enumerate(lines):
        if not line.strip().startswith("bounds:"):
            continue
        name = lines[i - 1].strip()
        frame = f"{name}.webp" if f"{name}.webp" in cards else f"{name}.png"
        if frame not in cards:
            continue
        x, y, w, h = (int(v) for v in line.split(":")[1].split(","))
        sheet.paste(cards[frame].resize((w, h), Image.LANCZOS), (x, y))
        n += 1
    if n:
        _atomic_save(sheet, png_path)
        webp = os.path.join(spine_dir, "mm_symbols.webp")
        if os.path.isfile(webp):
            _atomic_save(sheet, webp, lossless=True)
        page = (lines[0] or "").strip()
        if page and page not in {"mm_symbols.png", "mm_symbols.webp"}:
            extra = os.path.join(spine_dir, page)
            if page.endswith(".webp"):
                _atomic_save(sheet, extra, lossless=True)
            else:
                _atomic_save(sheet, extra)
        print(f"  spine patched {n} -> {spine_dir}")


def install_kit() -> None:
    if not os.path.isdir(NEW):
        raise SystemExit(f"missing new symbols: {NEW}")
    for slug, filename in PROP.items():
        src = os.path.join(NEW, filename)
        if not os.path.isfile(src):
            print(f"  skip missing {filename}")
            continue
        dest_dir = os.path.join(KIT, slug)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "idle.png")
        shutil.copy2(src, dest)
        print(f"  kit {filename} -> {slug}/idle.png")


def write_features() -> None:
    for name, path in FEATURE_PNGS.items():
        if not os.path.isfile(path):
            print(f"  skip feature {name}")
            continue
        src_im = Image.open(path).convert("RGBA")
        card = faces_lib.scatter_cell(src_im) if name == "tr_scatter.png" else fit_cell(src_im)
        for dest in MIRROR_DIRS:
            if not os.path.isdir(dest) and dest != MIRROR_DIRS[0]:
                continue
            os.makedirs(dest, exist_ok=True)
            _atomic_save(card, os.path.join(dest, name))
        print(f"  feature {name}")


def write_expanding_wild() -> None:
    script = os.path.join(HERE, "make_expanding_wild.py")
    subprocess.check_call([sys.executable, script], cwd=APP)
    src = os.path.join(APP, "assets", "sprites", "mirror", "wr_wild_expand.png")
    if not os.path.isfile(src):
        return
    card = Image.open(src).convert("RGBA")
    for dest in MIRROR_DIRS:
        os.makedirs(dest, exist_ok=True)
        _atomic_save(card, os.path.join(dest, "wr_wild_expand.png"))
    pay = os.path.join(APP, "static", "assets", "paytable", "wexpand.png")
    if os.path.isfile(pay):
        tile = Image.open(pay).convert("RGBA")
        for dest in PAYTABLE_DIRS:
            os.makedirs(dest, exist_ok=True)
            _atomic_save(tile, os.path.join(dest, "wexpand.png"))
    print("  feature wr_wild_expand.png")


RESTYLE_DIR = os.path.join(APP, "assets-raw", "symbol_restyle")
RESTYLE_KIT = {
    "h1-gunslinger": "h1_gunslinger.png",
    "h2-duchess": "h2_duchess.png",
    "h3-butcher": "h3_butcher.png",
    "h4-card-shark": "h4_cardshark.png",
    "h5-preacher": "h5_preacher.png",
    "w-revolver": "w_wild.png",
    "s-tombstone": "s_scatter.png",
    "su-super-scatter": "su_super.png",
    "gs-gunsmoke": "gs_gunsmoke.png",
    "sh-mark": "sh_mark.png",
}
RESTYLE_FEATURES = {
    "wr_wild.png": "w_wild.png",
    "tr_scatter.png": "s_scatter.png",
    "tr_scatter_super.png": "su_super.png",
    "tr_gs.png": "gs_gunsmoke.png",
    "tr_sh.png": "sh_mark.png",
    "tr_sp.png": "sp_split.png",
    "tr_nw.png": "nw_nudge.png",
    "tr_ts.png": "ts_tombstone.png",
    "tr_nudge_wild.png": "w_wild.png",
}

_restyle_highs = False


def install_restyle() -> None:
    os.makedirs(RESTYLE_DIR, exist_ok=True)
    for slug, filename in RESTYLE_KIT.items():
        src = os.path.join(RESTYLE_DIR, filename)
        if not os.path.isfile(src):
            print(f"  skip missing restyle {filename}")
            continue
        dest_dir = os.path.join(KIT, slug)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "idle.png")
        shutil.copy2(src, dest)
        print(f"  restyle {filename} -> {slug}/idle.png")


def write_restyle_features() -> None:
    for name, filename in RESTYLE_FEATURES.items():
        src = os.path.join(RESTYLE_DIR, filename)
        if not os.path.isfile(src):
            print(f"  skip feature {name}")
            continue
        src_im = Image.open(src).convert("RGBA")
        card = faces_lib.scatter_cell(src_im) if name == "tr_scatter.png" else fit_cell(src_im)
        for dest in MIRROR_DIRS:
            if not os.path.isdir(dest) and dest != MIRROR_DIRS[0]:
                continue
            os.makedirs(dest, exist_ok=True)
            _atomic_save(card, os.path.join(dest, name))
        print(f"  feature {name}")


HIGH_SPECIAL_SLUGS = (
    "h1-gunslinger",
    "h2-duchess",
    "h3-butcher",
    "h4-card-shark",
    "h5-preacher",
    "w-revolver",
    "s-tombstone",
    "gs-gunsmoke",
    "sh-mark",
)
HIGH_SPECIAL_FRAMES = set(HIGHS) | {"w.png", "s.png"}


def install_island_highs() -> None:
    if not os.path.isdir(ISLAND_HIGHS_DIR):
        raise SystemExit(f"missing island highs: {ISLAND_HIGHS_DIR}")
    os.makedirs(RESTYLE_DIR, exist_ok=True)
    for slug, filename in ISLAND_HIGHS.items():
        src = os.path.join(ISLAND_HIGHS_DIR, filename)
        if not os.path.isfile(src):
            raise SystemExit(f"missing {src}")
        dest_dir = os.path.join(KIT, slug)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(src, os.path.join(dest_dir, "idle.png"))
        restyle = RESTYLE_KIT.get(slug)
        if restyle:
            shutil.copy2(src, os.path.join(RESTYLE_DIR, restyle))
        print(f"  island {filename} -> {slug}/idle.png")


def install_island_lows() -> None:
    if not os.path.isdir(ISLAND_LOWS_DIR):
        raise SystemExit(f"missing island lows: {ISLAND_LOWS_DIR}")
    os.makedirs(RESTYLE_DIR, exist_ok=True)
    for slug, filename in ISLAND_LOWS.items():
        src = os.path.join(ISLAND_LOWS_DIR, filename)
        if not os.path.isfile(src):
            raise SystemExit(f"missing {src}")
        dest_dir = os.path.join(KIT, slug)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(src, os.path.join(dest_dir, "idle.png"))
        restyle = RESTYLE_LOWS.get(slug)
        if restyle:
            shutil.copy2(src, os.path.join(RESTYLE_DIR, restyle))
        print(f"  island {filename} -> {slug}/idle.png")


def install_highs_specials() -> None:
    if os.path.isdir(ISLAND_HIGHS_DIR):
        install_island_highs()
    for slug in HIGH_SPECIAL_SLUGS:
        if slug in ISLAND_HIGHS and os.path.isfile(os.path.join(KIT, slug, "idle.png")):
            continue
        src = os.path.join(NEW, PROP[slug])
        if not os.path.isfile(src):
            raise SystemExit(f"missing {src}")
        dest_dir = os.path.join(KIT, slug)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "idle.png")
        shutil.copy2(src, dest)
        print(f"  kit {os.path.basename(src)} -> {slug}/idle.png")


_SYMBOL_FX_SUFFIX = (
	"_plate",
	"_clip",
	"_aura",
	"_glow",
	"_streak",
	"_ring",
	"_wisp1",
	"_wisp2",
	"_wisp3",
	"_shard1",
	"_shard2",
	"_shard3",
	"_shard4",
)


def hide_plate_slots() -> None:
    paying = [f"h{i}" for i in range(1, 6)] + [f"l{i}" for i in range(1, 6)] + ["w", "s"]
    n = 0
    for dest in SPINE_DIRS:
        for gid in paying:
            path = os.path.join(dest, f"{gid}.json")
            if not os.path.isfile(path):
                continue
            data = json.loads(open(path, encoding="utf-8").read())
            hide_names = tuple(f"{gid}{sfx}" for sfx in _SYMBOL_FX_SUFFIX)
            changed = False
            for slot in data.get("slots") or []:
                if slot.get("name") in hide_names and slot.get("attachment"):
                    slot["attachment"] = None
                    changed = True
                if slot.get("blend"):
                    del slot["blend"]
                    changed = True
            skins = data.get("skins") or []
            if skins:
                atts = skins[0].get("attachments") or {}
                for slot_name in hide_names:
                    if slot_name in atts:
                        del atts[slot_name]
                        changed = True
            if changed:
                with open(path, "w", encoding="utf-8", newline="\n") as handle:
                    json.dump(data, handle, separators=(",", ":"))
                n += 1
    print(f"  hid plate/blend slots on {n} skeletons")


def write_nudge_wild_from_wild() -> None:
    wild = os.path.join(APP, "assets", "sprites", "mirror", "wr_wild.png")
    if not os.path.isfile(wild):
        return
    card = Image.open(wild).convert("RGBA")
    for dest in MIRROR_DIRS:
        os.makedirs(dest, exist_ok=True)
        _atomic_save(card, os.path.join(dest, "tr_nudge_wild.png"))
    print("  feature tr_nudge_wild.png")


if __name__ == "__main__":
    lows_only = "--lows-only" in sys.argv
    island_lows = "--island-lows" in sys.argv or lows_only
    restyle = "--restyle" in sys.argv
    highs_specials = "--highs-specials" in sys.argv
    island_highs = "--island-highs" in sys.argv
    no_plates = "--no-plates" in sys.argv
    _restyle_highs = restyle or highs_specials or no_plates or island_highs
    print("Installing desktop sheet symbols onto live v13...")
    if island_lows:
        print("  lows from island crop (A K Q J 10 plaques)")
        install_island_lows()
        faces = {k: v for k, v in load_ready().items() if k in LOWS}
        if len(faces) != 5:
            raise SystemExit(f"expected 5 low faces, got {sorted(faces)}")
        stacked = stack_paying(faces)
        for dest in ATLAS_DIRS:
            stamp_atlas(dest, stacked)
        for dest in SPINE_DIRS:
            patch_spine(dest, faces)
        write_paytable(stacked)
        hide_plate_slots()
        print("done")
        raise SystemExit(0)
    if island_highs:
        print("  highs from island crop (faces only)")
        install_island_highs()
        faces = {k: v for k, v in load_ready().items() if k in HIGHS}
        if len(faces) != 5:
            raise SystemExit(f"expected 5 high faces, got {sorted(faces)}")
        stacked = stack_paying(faces)
        for dest in ATLAS_DIRS:
            stamp_atlas(dest, stacked)
        for dest in SPINE_DIRS:
            patch_spine(dest, faces)
        write_paytable(stacked)
        hide_plate_slots()
        print("done")
        raise SystemExit(0)
    if no_plates:
        print("  faces only (no wood / blood backboards)")
        install_kit()
        faces = {k: v for k, v in load_ready().items() if k in HIGHS or k in LOWS}
        stacked = stack_paying(faces)
        for dest in ATLAS_DIRS:
            stamp_atlas(dest, stacked)
        for dest in SPINE_DIRS:
            patch_spine(dest, faces)
        write_paytable(stacked)
        hide_plate_slots()
        print("done")
        raise SystemExit(0)
    if highs_specials:
        print("  highs + specials from desktop folders")
        install_highs_specials()
        faces = {k: v for k, v in load_ready().items() if k in HIGH_SPECIAL_FRAMES}
        stacked = stack_paying(faces)
        for dest in ATLAS_DIRS:
            stamp_atlas(dest, stacked)
        for dest in SPINE_DIRS:
            patch_spine(dest, {k: v for k, v in faces.items() if k in HIGHS})
        write_paytable(stacked)
        write_features()
        write_nudge_wild_from_wild()
        write_expanding_wild()
        print("done")
        raise SystemExit(0)
    if restyle:
        print("  sticker restyle (highs + specials)")
        install_restyle()
        want = set(HIGHS) | {"w.png", "s.png"}
        faces = {k: v for k, v in load_ready().items() if k in want and os.path.isfile(READY[k])}
        stacked = stack_paying(faces)
        for dest in ATLAS_DIRS:
            stamp_atlas(dest, stacked)
        for dest in SPINE_DIRS:
            patch_spine(dest, {k: v for k, v in faces.items() if k in HIGHS})
        write_paytable(stacked)
        write_restyle_features()
        write_expanding_wild()
        print("done")
        raise SystemExit(0)
    if lows_only:
        print("  lows only (A K Q J 10)")
        for slug in (
            "l1-bullet",
            "l2-whiskey",
            "l3-spur",
            "l4-horseshoe",
            "l5-dead-mans-hand",
        ):
            src = os.path.join(NEW, PROP[slug])
            if not os.path.isfile(src):
                raise SystemExit(f"missing {src}")
            dest_dir = os.path.join(KIT, slug)
            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, "idle.png")
            shutil.copy2(src, dest)
            print(f"  kit {PROP[slug]} -> {slug}/idle.png")
        faces = {k: v for k, v in load_ready().items() if k in LOWS}
    else:
        install_kit()
        faces = load_ready()
    if not faces:
        raise SystemExit("no ready idles")
    stacked = stack_paying(faces)
    for dest in ATLAS_DIRS:
        stamp_atlas(dest, stacked)
    for dest in SPINE_DIRS:
        patch_spine(dest, faces)
    write_paytable(stacked)
    if not lows_only:
        write_features()
        write_expanding_wild()
    print("done")
