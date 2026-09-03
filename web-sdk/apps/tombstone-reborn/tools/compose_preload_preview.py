"""Compose the preload layout at desktop canvas size for visual check."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

APP = Path(__file__).resolve().parents[1]
PRE = APP / "assets" / "sprites" / "preload"
MIRROR = APP / "assets" / "sprites" / "mirror"
BG = PRE / "bg.png"
LOGO = MIRROR / "tr_logo.png"
OUT = APP / "assets-raw" / "preload" / "preview_desktop.png"

W, H = 1422, 800
BG_W, BG_H = 1536, 1024
ACTIVE_RATIO = 823 / 479
SIDE_RATIO = 572 / 298
ARROW_RATIO = 305 / 180
CONTINUE_RATIO = 165 / 784
CARD_ART_TOP = 0.22
CARD_ART_BOT = 0.62
CARD_TITLE_Y = 0.925
CARD_BODY_MAX_BOTTOM = 0.86
CARD_ART_W = 0.66
LOGO_ASPECT = 717 / 1514

ART = {
    -1: MIRROR / "tr_scatter_super.png",
    0: MIRROR / "tr_scatter.png",
    1: MIRROR / "tr_sp.png",
}
TITLES = {-1: "THE RECKONING", 0: "THE WAKE", 1: "SPLIT"}
BODIES = {
    -1: "A SUPER SCATTER OPENS\nTHE LAST-REEL LANE",
    0: "3 BONUS TOMBSTONES\nUNLOCK 10 BONUS SPINS",
    1: "ONE SYMBOL GAINS EXTRA WAYS\nTHEN TURNS WILD",
}


def fit(src: Image.Image, box: tuple[int, int]) -> Image.Image:
    src = src.convert("RGBA")
    scale = min(box[0] / src.width, box[1] / src.height)
    nw = max(1, round(src.width * scale))
    nh = max(1, round(src.height * scale))
    return src.resize((nw, nh), Image.LANCZOS)


def paste_c(dst: Image.Image, src: Image.Image, cx: float, cy: float) -> None:
    x = int(cx - src.width / 2)
    y = int(cy - src.height / 2)
    dst.alpha_composite(src, (x, y))


def box(cx: float, cy: float, w: float, h: float) -> tuple[float, float, float, float]:
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return a[0] < b[2] - 0.5 and b[0] < a[2] - 0.5 and a[1] < b[3] - 0.5 and b[1] < a[3] - 0.5


def main() -> None:
    scale = max(W / BG_W, H / BG_H)
    drawn_w, drawn_h = BG_W * scale, BG_H * scale
    bg = Image.open(BG).convert("RGBA").resize((int(drawn_w), int(drawn_h)), Image.LANCZOS)
    canvas = Image.new("RGBA", (W, H), (5, 3, 8, 255))
    origin = (int(W / 2 - drawn_w / 2), int(H / 2 - drawn_h / 2))
    canvas.alpha_composite(bg, origin)

    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
        body_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
    except OSError:
        title_font = body_font = ImageFont.load_default()

    stage_w = max(160, W * 0.86)
    logo_w = min(stage_w * 0.36, H * 0.16 / LOGO_ASPECT, 340)
    logo_h = logo_w * LOGO_ASPECT
    logo_y = max(logo_h * 0.52 + 10, H * 0.08)
    continue_w = min(stage_w * 0.48, W * 0.36)
    continue_h = continue_w * CONTINUE_RATIO
    continue_y = H - continue_h * 0.5 - max(10, H * 0.02)
    card_top = logo_y + logo_h * 0.5 + max(10, H * 0.02)
    card_bot = continue_y - continue_h * 0.5 - max(36, H * 0.07)
    budget = max(120, card_bot - card_top)
    card_y = (card_top + card_bot) * 0.5
    card_gap = max(8, stage_w * 0.016)
    arrow_pad = max(10, stage_w * 0.014)
    raw_center_h = budget
    raw_center_w = raw_center_h / ACTIVE_RATIO
    raw_side_h = raw_center_h * 0.84
    raw_side_w = raw_side_h / SIDE_RATIO
    raw_arrow_h = raw_center_h * 0.22
    raw_arrow_w = raw_arrow_h / ARROW_RATIO
    raw_row = raw_center_w + (raw_side_w + card_gap) * 2 + (raw_arrow_w + arrow_pad) * 2
    scale_c = min(1, (stage_w * 0.96) / raw_row)
    a_w, a_h = raw_center_w * scale_c, raw_center_h * scale_c
    s_w, s_h = raw_side_w * scale_c, raw_side_h * scale_c
    arrow_h, arrow_w = raw_arrow_h * scale_c, raw_arrow_w * scale_c
    side_span = s_w + card_gap * scale_c
    arrow_x = a_w * 0.5 + side_span + arrow_pad * scale_c + arrow_w * 0.5
    card_bottom = card_y + a_h * 0.5
    dot_size = min(stage_w * 0.038, 28)
    dots_y = min(
        continue_y - continue_h * 0.5 - dot_size * 0.7,
        card_bottom + max(10, a_h * 0.035) + dot_size * 0.5,
    )
    paste_c(canvas, fit(Image.open(LOGO), (int(logo_w), int(logo_h))), W / 2, logo_y)

    def art_box(cw: float, ch: float) -> tuple[float, float]:
        well_h = (CARD_ART_BOT - CARD_ART_TOP) * ch
        well_w = cw * CARD_ART_W
        size = min(well_w, well_h * 0.88)
        y = ((CARD_ART_TOP + CARD_ART_BOT) * 0.5 - 0.5) * ch
        return y, size

    def card(key: str, art_i: int, cx: float, cw: float, ch: float, alpha: int) -> dict[str, tuple[float, float, float, float]]:
        frame = Image.open(PRE / key).convert("RGBA").resize((int(cw), int(ch)), Image.LANCZOS)
        if alpha < 255:
            r, g, b, a = frame.split()
            frame = Image.merge("RGBA", (r, g, b, a.point(lambda v: int(v * alpha / 255))))
        paste_c(canvas, frame, cx, card_y)
        art = Image.open(ART[art_i]).convert("RGBA")
        ay, size = art_box(cw, ch)
        art = fit(art, (int(size), int(size)))
        paste_c(canvas, art, cx, card_y + ay)
        d = ImageDraw.Draw(canvas)
        body_size = max(11, min(cw * 0.08, ch * 0.04))
        line_h = body_size * 1.16
        block_h = line_h * 2
        center_from_top = min(ch * 0.74, ch * CARD_BODY_MAX_BOTTOM - block_h * 0.5)
        by = card_y + center_from_top - ch * 0.5
        ty = card_y + (CARD_TITLE_Y - 0.5) * ch
        d.multiline_text((cx, by), BODIES[art_i], fill=(240, 230, 208, 255), font=body_font, anchor="mm", align="center")
        d.text((cx, ty), TITLES[art_i], fill=(18, 12, 8, 255), font=title_font, anchor="mm")
        return {
            "frame": box(cx, card_y, cw, ch),
            "art": box(cx, card_y + ay, size, size),
            "body": box(cx, by, cw * 0.82, block_h),
            "title": box(cx, ty, cw * 0.8, max(12, cw * 0.082) * 1.2),
        }

    left_x = W / 2 - (a_w * 0.5 + card_gap * scale_c + s_w * 0.5)
    right_x = W / 2 + (a_w * 0.5 + card_gap * scale_c + s_w * 0.5)
    left = card("card_side_l.png", -1, left_x, s_w, s_h, 200)
    mid = card("card_active.png", 0, W / 2, a_w, a_h, 255)
    right = card("card_side_r.png", 1, right_x, s_w, s_h, 200)

    paste_c(canvas, fit(Image.open(PRE / "arrow_left.png"), (int(arrow_w), int(arrow_h))), W / 2 - arrow_x, card_y)
    paste_c(canvas, fit(Image.open(PRE / "arrow_right.png"), (int(arrow_w), int(arrow_h))), W / 2 + arrow_x, card_y)

    for i in range(6):
        name = "dot_on.png" if i == 0 else "dot_off.png"
        sz = dot_size * (1.15 if i == 0 else 0.72)
        paste_c(canvas, fit(Image.open(PRE / name), (sz, sz)), W / 2 + (i - 2.5) * dot_size * 1.45, dots_y)

    paste_c(
        canvas,
        fit(Image.open(PRE / "continue.png"), (int(continue_w), int(continue_h))),
        W / 2,
        continue_y,
    )

    boxes = {
        "left": left["frame"],
        "mid": mid["frame"],
        "right": right["frame"],
        "arrowL": box(W / 2 - arrow_x, card_y, arrow_w, arrow_h),
        "arrowR": box(W / 2 + arrow_x, card_y, arrow_w, arrow_h),
        "dots": box(W / 2, dots_y, 6 * dot_size * 1.45, dot_size * 1.15),
        "continue": box(W / 2, continue_y, continue_w, continue_h),
        "logo": box(W / 2, logo_y, logo_w, logo_h),
    }
    hits = []
    pairs = (
        ("arrowL", "left"),
        ("arrowR", "right"),
        ("left", "mid"),
        ("mid", "right"),
        ("mid", "dots"),
        ("dots", "continue"),
        ("left", "dots"),
        ("right", "dots"),
        ("mid", "logo"),
        ("left", "logo"),
        ("right", "logo"),
    )
    for a, b in pairs:
        if overlap(boxes[a], boxes[b]):
            hits.append(f"{a} x {b}")
    inner = []
    for name, pack in (("L", left), ("M", mid), ("R", right)):
        if overlap(pack["art"], pack["body"]):
            inner.append(f"{name} art x body")
        if overlap(pack["body"], pack["title"]):
            inner.append(f"{name} body x title")
        if overlap(pack["art"], pack["title"]):
            inner.append(f"{name} art x title")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT)
    print(f"wrote {OUT} {canvas.size} cards {a_w:.0f}x{a_h:.0f} sides {s_w:.0f}x{s_h:.0f} scale {scale_c:.3f}")
    print(f"cardBottom {card_bottom:.1f} dots {dots_y:.1f} continue {continue_y:.1f}")
    print("overlap_row", hits or "none")
    print("overlap_card", inner or "none")


if __name__ == "__main__":
    main()
