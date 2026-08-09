"""Reskin the forked White Room atlas with the generated Tombstone Reborn art.

- Repacks sprites/symbolsStatic/symbolsStatic.png in place: each mapped frame
  gets the new art baked into the same portrait-card shape the White Room reels
  use (rounded portrait pane + dark bezel inside the 300x300 cell), so the reel
  look carries over 1:1. `_blur` frames get a vertical smear of the new card,
  `_burn` frames a darkened ember tint.
- scene_bg_v5.webp   <- tr_scene_bg.png   (cover-fit 1920x1088)
- mirror/logo_v3.png <- tr_logo.png       (alpha keyed from black)
- mirror/wr_wild.png <- tr_w_revolver.png (portrait card, gold bezel)
- tombstone/buy_small.png / buy_super.png (bonus-buy card art)

Everything is written to BOTH trees (assets-src/ staging + static/assets/
served) per the assets skill.
"""

import json
import os
import shutil

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
GEN = r"C:\Users\Emex33\.cursor\projects\c-Users-Emex33-Desktop-stakez\assets"

STATIC = os.path.join(APP, "static", "assets")
SRC = os.path.join(APP, "assets-src")

ART = {
    "h1": "tr_h1_gunslinger.png",
    "h2": "tr_h2_duchess.png",
    "h3": "tr_h3_butcher.png",
    "h4": "tr_h4_cardshark.png",
    "h5": "tr_h5_preacher.png",
    "l1": "tr_l1_bullet.png",
    "l2": "tr_l2_whiskey.png",
    "l3": "tr_l3_spur.png",
    "l4": "tr_l4_horseshoe.png",
    "l5": "tr_l5_cards.png",
    "w": "tr_w_revolver.png",
    "s": "tr_s_tombstone.png",
}

# card geometry inside a 300x300 cell (mirrors constants.SYMBOL_CARD_W/H:
# height 292/300 of the cell, width 0.775 of the height)
CARD_H_FRAC = 292 / 300
CARD_W_FRAC = 0.775
CORNER_FRAC = 0.055

BEZEL = (14, 11, 8, 255)        # dark iron-wood bezel
BEZEL_GOLD = (150, 112, 48, 255)  # wild's gold bezel


def cover_fit(art: Image.Image, w: int, h: int) -> Image.Image:
    """center-crop the art to cover w x h without squashing"""
    aw, ah = art.size
    scale = max(w / aw, h / ah)
    art = art.resize((max(1, round(aw * scale)), max(1, round(ah * scale))), Image.LANCZOS)
    aw, ah = art.size
    left, top = (aw - w) // 2, (ah - h) // 2
    return art.crop((left, top, left + w, top + h))


def portrait_card(art: Image.Image, cell_w: int, cell_h: int, bezel=BEZEL) -> Image.Image:
    """bake the art into a rounded portrait pane centered in the cell"""
    card_h = round(cell_h * CARD_H_FRAC)
    card_w = round(card_h * CARD_W_FRAC)
    radius = max(6, round(card_h * CORNER_FRAC))

    pane = cover_fit(art.convert("RGB"), card_w, card_h).convert("RGBA")

    # rounded mask
    mask = Image.new("L", (card_w, card_h), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=radius, fill=255)
    pane.putalpha(mask)

    # bezel: stroke just inside the pane edge + 1px inner highlight
    d = ImageDraw.Draw(pane)
    d.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=radius, outline=bezel, width=4)
    d.rounded_rectangle(
        [3, 3, card_w - 4, card_h - 4],
        radius=max(3, radius - 3),
        outline=(255, 240, 210, 40),
        width=1,
    )

    cell = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
    cell.paste(pane, ((cell_w - card_w) // 2, (cell_h - card_h) // 2), pane)
    return cell


def smear(card: Image.Image, w: int, h: int) -> Image.Image:
    """vertical motion smear of the card for the spin state"""
    base = card.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    steps = 14
    span = round(h * 0.30)
    for i in range(steps):
        dy = round((i / (steps - 1) - 0.5) * span)
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        layer.paste(base, (0, dy), base)
        layer.putalpha(layer.split()[3].point(lambda a: a * 2 // steps))
        out = Image.alpha_composite(out, layer)
    return out.filter(ImageFilter.GaussianBlur(2))


def burn(card: Image.Image) -> Image.Image:
    """darkened ember-tinted variant"""
    dark = ImageEnhance.Brightness(card).enhance(0.45)
    tint = Image.new("RGBA", card.size, (200, 80, 20, 70))
    tint.putalpha(Image.composite(tint.split()[3], Image.new("L", card.size, 0), card.split()[3]))
    return Image.alpha_composite(dark, tint)


def both_trees(rel: str):
    return [os.path.join(STATIC, rel), os.path.join(SRC, rel)]


def save_both(img: Image.Image, rel: str, **kwargs):
    for path in both_trees(rel):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path, **kwargs)
    print("wrote", rel)


def repack_atlas():
    rel_json = os.path.join("sprites", "symbolsStatic", "symbolsStatic.json")
    rel_png = os.path.join("sprites", "symbolsStatic", "symbolsStatic.png")
    atlas_json = json.load(open(os.path.join(STATIC, rel_json)))
    sheet = Image.open(os.path.join(STATIC, rel_png)).convert("RGBA")

    frames = atlas_json["frames"]

    def frame_rect(key):
        f = frames[key]
        assert not f.get("rotated"), f"rotated frame not supported: {key}"
        r = f["frame"]
        return r["x"], r["y"], r["w"], r["h"]

    def blit(key, img):
        x, y, w, h = frame_rect(key)
        if img.size != (w, h):
            img = img.resize((w, h), Image.LANCZOS)
        # clear the old pixels then paste with alpha
        sheet.paste(Image.new("RGBA", (w, h), (0, 0, 0, 0)), (x, y))
        sheet.paste(img, (x, y), img)

    for sid, fname in ART.items():
        art = Image.open(os.path.join(GEN, fname))
        base_key = f"{sid}.webp" if f"{sid}.webp" in frames else f"{sid}.png"
        if base_key not in frames:
            print("skip (no frame):", sid)
            continue
        _, _, w, h = frame_rect(base_key)
        bezel = BEZEL_GOLD if sid == "w" else BEZEL
        card = portrait_card(art, w, h, bezel=bezel)
        blit(base_key, card)

        for suffix, maker in (("_blur", None), ("_burn", None)):
            key = base_key.replace(".", f"{suffix}.")
            if key not in frames:
                continue
            _, _, bw, bh = frame_rect(key)
            if suffix == "_blur":
                blit(key, smear(card, bw, bh))
            else:
                blit(key, burn(card).resize((bw, bh), Image.LANCZOS))
        print("repacked", sid)

    for path in both_trees(rel_png):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        sheet.save(path)
    # Pixi loads whatever meta.image names — currently symbolsStatic.webp
    rel_webp = os.path.join("sprites", "symbolsStatic", "symbolsStatic.webp")
    for path in both_trees(rel_webp):
        sheet.save(path, "WEBP", quality=90, method=6)
    # keep the json identical in both trees (unchanged, but assert sync)
    shutil.copyfile(os.path.join(STATIC, rel_json), os.path.join(SRC, rel_json))
    print("atlas repacked (png + webp)")


def scene():
    art = Image.open(os.path.join(GEN, "tr_scene_bg.png"))
    bg = cover_fit(art.convert("RGB"), 1920, 1088)
    save_both(bg, os.path.join("sprites", "scene", "scene_bg_v5.webp"), quality=82, method=6)


def logo():
    art = Image.open(os.path.join(GEN, "tr_logo.png")).convert("RGB")
    # alpha from luminance (bright mark on pure black)
    gray = art.convert("L")
    alpha = gray.point(lambda v: min(255, round(v * 2.2)))
    rgba = art.convert("RGBA")
    rgba.putalpha(alpha)
    box = alpha.getbbox()
    if box:
        rgba = rgba.crop(box)
    save_both(rgba, os.path.join("sprites", "mirror", "logo_v3.png"))


def wild_card():
    # the standalone wild sprite: same portrait card at the original file's size
    rel = os.path.join("sprites", "mirror", "wr_wild.png")
    old = Image.open(os.path.join(STATIC, rel))
    art = Image.open(os.path.join(GEN, "tr_w_revolver.png"))
    card = portrait_card(art, *old.size, bezel=BEZEL_GOLD)
    save_both(card, rel)


def buy_cards():
    for name, fname in (("buy_small.png", "tr_s_tombstone.png"), ("buy_super.png", "tr_w_revolver.png")):
        art = Image.open(os.path.join(GEN, fname))
        card = cover_fit(art.convert("RGB"), 512, 512).convert("RGBA")
        save_both(card, os.path.join("sprites", "tombstone", name))


if __name__ == "__main__":
    repack_atlas()
    scene()
    logo()
    wild_card()
    buy_cards()
    print("DONE tombstone reskin")
