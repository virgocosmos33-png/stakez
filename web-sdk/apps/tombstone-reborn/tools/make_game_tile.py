"""Bake the Stake submission tile for THE WHITE ROOM.

Stake rejected the Madam Mirror tile for "dark(er) edges which might clash with
Stake's background", so this one is built to stay bright all the way out to the
border: the key art is high-key to begin with, the frame edge gets an explicit
lift toward white, and the script prints the darkest border pixel it ends up with
so the result can be checked against that rejection without guessing.

Outputs, into submission/ (deliberately NOT static/ — these are uploaded to the
Stake submission form by hand and would otherwise be copied verbatim into the
game build, costing over a megabyte of download for art no player ever sees):
  TheWhiteRoom-Tile.png  1024x1536 composite — this is the thumbnail itself
  TheWhiteRoom-BG.jpg    1024x1536 empty room, no character and no title
  TheWhiteRoom-FG.png    1024x1536 character alone, transparent (chroma-keyed)

Stake wants the two layers to be genuinely separable — BG is the environment on
its own and FG is the character on its own — so the scene art is an EMPTY room
(assets-raw/tile/scene.png; the older render with the character baked in is kept
beside it as scene_with_hero.png) and the character is composited on top here.
That means the placement below defines both the FG layer and the tile, so the
two can never drift apart.

Sources live in assets-raw/tile/. The title is the shipping game logo
(assets-raw/mirror/logo_v3_master.png), recoloured to the same red/white/keyline
treatment the SCATTER cards use — the logo is off-white on its own and would
vanish against a white room.

Run:  python tools/make_game_tile.py
"""

import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "assets-raw"))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "submission"))

SCENE = os.path.join(RAW, "tile", "scene.png")
HERO = os.path.join(RAW, "tile", "hero_magenta.png")
LOGO = os.path.join(RAW, "mirror", "logo_v3_master.png")

W, H = 1024, 1536

# Shared with tools/make_scatter_words.py — the title has to look like it came
# off the same press as the SCATTER cards.
RED = (214, 22, 40, 255)
WHITE = (252, 252, 250, 255)
KEYLINE = (26, 24, 22, 255)

LOGO_MAX_W = 0.78  # of tile width
LOGO_MAX_H = 0.42  # of tile height
LOGO_BOTTOM = 64  # px of clear floor under the lockup

HERO_HEIGHT = 0.66  # of tile height — a head-and-shoulders bust, not a full figure
HERO_MAX_W = 0.86  # of tile width — keeps wide shoulders inside Stake's safe area
HERO_BOTTOM = 0.30  # clear room under the bust, as a fraction of tile height
HERO_FADE = 0.28  # bottom fraction of the figure dissolved into the floor haze

EDGE_LIFT = 0.26  # how far the outer frame is pulled toward white
EDGE_START = 0.60  # normalised radius where the lift begins


def cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Scale to fill, centre-crop the overflow."""
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    w, h = round(img.width * scale), round(img.height * scale)
    img = img.resize((w, h), Image.LANCZOS)
    return img.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th))


def lift_edges(img: Image.Image) -> Image.Image:
    """Pull the outer frame toward white.

    Radius is measured on the square-normalised frame so the corners — the exact
    thing called out in the rejection — get the strongest lift.
    """
    px = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / np.sqrt(2)
    t = (np.clip((r - EDGE_START) / (1.0 - EDGE_START), 0.0, 1.0) ** 1.4 * EDGE_LIFT)[..., None]
    px = px * (1.0 - t) + np.float32(1.0) * t
    return Image.fromarray((np.clip(px, 0, 1) * 255).astype(np.uint8), "RGB")


def darkest_border(img: Image.Image, band: int = 24) -> tuple[float, tuple[int, int]]:
    """Luminance (0-255) of the darkest pixel in the outer `band` px, and where.

    The location matters: a single dark prop touching the frame is fine, a dark
    corner is the thing that got Madam Mirror sent back.
    """
    px = np.asarray(img.convert("RGB"), dtype=np.float32)
    lum = px[..., 0] * 0.299 + px[..., 1] * 0.587 + px[..., 2] * 0.114
    edge = np.full_like(lum, 255.0)
    edge[:band] = lum[:band]
    edge[-band:] = lum[-band:]
    edge[:, :band] = lum[:, :band]
    edge[:, -band:] = lum[:, -band:]
    y, x = np.unravel_index(int(edge.argmin()), edge.shape)
    return float(edge[y, x]), (int(x), int(y))


def key_magenta(img: Image.Image) -> Image.Image:
    """Cut the figure off its magenta ground.

    Keys on how magenta a pixel is — (R+B)/2 - G, which is 1 for #FF00FF and 0
    for anything neutral — then erodes a couple of pixels to lose the green
    fringe the generator leaves around the silhouette, and finally despills both
    casts so no magenta or green survives inside the cut.
    """
    px = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    r, g, b = px[..., 0], px[..., 1], px[..., 2]

    mag = (r + b) * 0.5 - g
    alpha = np.clip((0.35 - mag) / 0.20, 0.0, 1.0)

    mask = Image.fromarray((alpha * 255).astype(np.uint8), "L")
    for _ in range(3):  # erode past the fringe
        mask = mask.filter(ImageFilter.MinFilter(3))
    mask = mask.filter(ImageFilter.GaussianBlur(1.1))
    alpha = np.asarray(mask, dtype=np.float32) / 255.0

    # despill green: no channel should sit above the R/B average by much
    ceiling = (r + b) * 0.5 + 0.06
    g = np.minimum(g, ceiling)
    # despill magenta: pull R and B back down toward G where the cast remains
    mag = (r + b) * 0.5 - g
    spill = np.clip(mag - 0.05, 0.0, None)[..., None]
    rgb = np.stack([r, g, b], axis=-1)
    neutral = np.repeat(g[..., None], 3, axis=-1)
    rgb = rgb * (1.0 - spill) + neutral * spill

    out = np.concatenate([np.clip(rgb, 0, 1), alpha[..., None]], axis=-1)
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def place_hero(hero: Image.Image) -> Image.Image:
    """Stand the keyed figure in the room on a full-size transparent canvas.

    The room's floor is a sheet of white haze, so the figure is dissolved into
    it over her lowest fifth rather than being planted on a hard contact edge —
    the same way she read in the older render that had her baked into the scene.
    """
    hero = hero.crop(hero.split()[3].getbbox())
    # Whichever limit binds first: a bust is wider than it is tall, so scaling on
    # height alone would push the shoulders off the sides of the tile.
    scale = min(H * HERO_HEIGHT / hero.height, W * HERO_MAX_W / hero.width)
    width, height = round(hero.width * scale), round(hero.height * scale)
    hero = hero.resize((width, height), Image.LANCZOS)

    alpha = np.asarray(hero.split()[3], dtype=np.float32) / 255.0
    fade_px = max(1, round(height * HERO_FADE))
    ramp = np.ones(height, dtype=np.float32)
    ramp[-fade_px:] = np.linspace(1.0, 0.0, fade_px) ** 1.6
    alpha *= ramp[:, None]
    hero.putalpha(Image.fromarray((alpha * 255).astype(np.uint8), "L"))

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(hero, ((W - width) // 2, H - round(H * HERO_BOTTOM) - height))
    return canvas


def title_lockup(width: int) -> Image.Image:
    """The game logo in SCATTER-card paint: red face, white edge, dark keyline.

    The shipping logo is off-white, which is invisible on a white room, so the
    alpha is reused purely as a stencil and repainted.
    """
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.crop(logo.split()[3].getbbox())

    height = round(width * logo.height / logo.width)
    stencil = logo.split()[3].resize((width, height), Image.LANCZOS)

    # One text line is roughly a third of the stack; scale the paint edges off
    # that so the treatment matches the cards at any tile size. The edges are
    # much finer than the SCATTER cards use because the letters in this logo
    # nearly touch — a card-weight outline welds WHITE and ROOM into one slab
    # and the keyline then traces the slab instead of the letters.
    cap = height / 3.0
    outline = max(1.5, cap * 0.018)
    key = max(1.0, cap * 0.012)

    pad = int(round(outline + key)) + 8
    canvas = (width + pad * 2, height + pad * 2)
    solid = Image.new("L", canvas, 0)
    solid.paste(stencil, (pad, pad))

    def dilate(src: Image.Image, radius: float) -> Image.Image:
        out = src
        for _ in range(int(round(radius))):
            out = out.filter(ImageFilter.MaxFilter(3))
        return out.filter(ImageFilter.GaussianBlur(0.8))

    layer = Image.new("RGBA", canvas, (0, 0, 0, 0))
    for colour, radius in ((KEYLINE, outline + key), (WHITE, outline), (RED, 0)):
        part = Image.new("RGBA", canvas, colour[:3] + (0,))
        part.putalpha(dilate(solid, radius) if radius else solid)
        layer = Image.alpha_composite(layer, part)

    # soft shadow so the lockup lifts off a bright floor instead of sitting flat
    shadow = Image.new("RGBA", canvas, (40, 38, 36, 0))
    shadow.putalpha(dilate(solid, outline + key).filter(ImageFilter.GaussianBlur(cap * 0.09)))
    shadow = Image.fromarray(
        np.concatenate(
            [
                np.asarray(shadow)[..., :3],
                (np.asarray(shadow)[..., 3:] * 0.45).astype(np.uint8),
            ],
            axis=-1,
        )
    )
    return Image.alpha_composite(shadow, layer)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    background = lift_edges(cover(Image.open(SCENE).convert("RGB"), (W, H)))
    # JPEG for the background (the spec allows png or jpg) — as a PNG the pair
    # lands at 2.8 MB against a 3 MB ceiling with no room to breathe.
    bg_path = os.path.join(OUT_DIR, "TheWhiteRoom-BG.jpg")
    background.save(bg_path, quality=93, subsampling=0)

    foreground = place_hero(key_magenta(Image.open(HERO).convert("RGB")))
    fg_path = os.path.join(OUT_DIR, "TheWhiteRoom-FG.png")
    foreground.save(fg_path)

    lockup_w = min(round(W * LOGO_MAX_W), round(H * LOGO_MAX_H * 1806 / 1838))
    lockup = title_lockup(lockup_w)
    if lockup.height > H * LOGO_MAX_H:
        lockup = title_lockup(round(lockup_w * (H * LOGO_MAX_H) / lockup.height))

    tile = background.convert("RGBA")
    tile.alpha_composite(foreground)
    tile.alpha_composite(lockup, ((W - lockup.width) // 2, H - LOGO_BOTTOM - lockup.height))
    tile = tile.convert("RGB")
    tile_path = os.path.join(OUT_DIR, "TheWhiteRoom-Tile.png")
    tile.save(tile_path)

    total = (os.path.getsize(bg_path) + os.path.getsize(fg_path)) / 1e6
    darkest, at = darkest_border(tile)
    print(f"tile -> {tile_path}")
    print(f"        darkest border pixel {darkest:.0f}/255 at {at}")
    print(f"bg   -> {bg_path}")
    print(f"fg   -> {fg_path}")
    print(f"BG + FG = {total:.2f} MB (Stake limit 3 MB)")
