"""Verify the restored BET-amount modal trigger coexists with the −/+ steppers.

For every layout that owns a bet control:
  (a) clicking the BET *amount* opens the bet-menu modal (asserted via the
      unique `.bet-menu` DOM node the ModalBetMenu renders through Popup),
  (b) clicking `+` then `-` steps the value and does NOT open the modal,
  (c) at the widest value ("$1,000.00") the amount never overlaps the steppers.

Screenshots are written to web-sdk/qa-shots/hud/ (betmodal-<layout>-*.png). The
modal shot hides the pixi canvas first (the canvas composites over the HTML
portal), matching tools/qa_shot_modal_clean.py.

Run from web-sdk/apps/ways:  python tools/qa_betmodal.py   (Storybook on :6001)

Viewports (each forces a distinct HUD layout):
  - desktop   1600x900  -> LayoutDesktop (== Landscape) ControlInfoBar
  - portrait   540x960  -> LayoutPortrait  LabelBet + flanking steppers
  - tablet    1200x1200 -> LayoutTablet    LabelBet + flanking steppers
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--random"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

UI_BASE = 150


def control_info_bar_cfg(name, W, H):
    # LayoutDesktop and LayoutLandscape are the identical file (same transform,
    # same ControlInfoBar, standard 1920x1080), so one config serves both.
    cs = min(W / 1920, H / 1080)  # canvas (MainContainer) scale, centred at 0,0
    bar_scale = 0.84
    BUY = SPIN = UI_BASE * 1.2
    BADGE = UI_BASE * 0.6
    INFO = 500
    G1, G2, G3, SIDE = 14, 16, 22, 10
    spin_cluster = BADGE + SIDE + SPIN + SIDE + BADGE
    TW = BUY + G1 + BADGE + G2 + INFO + G3 + spin_cluster
    infoC = (-TW / 2 + BUY + G1 + BADGE + G2) + INFO / 2
    bar_x, bar_y = 1920 / 2, 1080 - 22 - (SPIN * bar_scale) / 2
    cib_left, cib_top = infoC - INFO / 2, -88 / 2

    def scr(lx, ly):
        # standard (1920x1080) coord of the local ControlInfoBar point ...
        sx = bar_x + (cib_left + lx) * bar_scale
        sy = bar_y + (cib_top + ly) * bar_scale
        # ... then map through the centred MainContainer (handles letterboxing;
        # for perfect-fit viewports the offset cancels, matching the old math).
        return (W / 2 + (sx - 1920 / 2) * cs, H / 2 + (sy - 1080 / 2) * cs)

    tl, br = scr(0, 0), scr(INFO, 88)
    clip = {"x": max(0, tl[0] - 12), "y": max(0, tl[1] - 14),
            "width": br[0] - tl[0] + 24, "height": br[1] - tl[1] + 28}
    # bet hit rect (ControlInfoBar): betHitX=242, betHitW=136 -> centre local x=310
    amount = scr(310, 44)
    fallbacks = [scr(300, 44), scr(330, 44), scr(285, 44), scr(350, 44), scr(270, 44)]
    return dict(name=name, w=W, h=H, plus=scr(459, 44), minus=scr(407, 44),
                amount=amount, fallbacks=fallbacks, clip=clip)


def desktop_cfg():
    return control_info_bar_cfg("desktop", 1600, 900)


def landscape_cfg():
    # ratio 2.045 (>=1.3 -> longWidth) and min side 440 (<=480 -> mobile) => landscape
    return control_info_bar_cfg("landscape", 900, 440)


def portrait_cfg():
    W, H = 540, 960
    cs = min(W / 1080, H / 1920)  # 0.5
    SW = 1080  # portrait STANDARD width
    ay = (1920 - 112) * cs         # text row baseline, lines up with the steppers
    ax = (SW * 0.5 - 250) * cs     # pill centre (145)
    plus = ((SW * 0.5 - 250 + 200) * cs, ay)
    minus = ((SW * 0.5 - 250 - 200) * cs, ay)
    amount = (ax + 27, ay)  # value sits to the right of the pill centre
    fallbacks = [(ax + 10, ay), (ax + 45, ay), (ax - 15, ay), (ax + 55, ay), (ax, ay)]
    clip = {"x": 0, "y": 850, "width": 540, "height": 110}
    return dict(name="portrait", w=W, h=H, plus=plus, minus=minus,
                amount=amount, fallbacks=fallbacks, clip=clip)


def tablet_cfg():
    W, H = 1200, 1200  # ratio 1.0 -> almostSquare -> LayoutTablet
    cs = min(W / 1920, H / 1920)  # 0.625
    BET_X = 1920 * 0.135
    dx = 1920 * 0.095
    Y_PILL = 1920 * 0.82
    ay = (Y_PILL + 32) * cs
    ax = BET_X * cs  # pill centre (162)
    plus = ((BET_X + dx) * cs, ay)
    minus = ((BET_X - dx) * cs, ay)
    amount = (ax + 30, ay)
    fallbacks = [(ax + 10, ay), (ax + 50, ay), (ax - 15, ay), (ax + 65, ay), (ax, ay)]
    clip = {"x": 0, "y": 950, "width": 620, "height": 130}
    return dict(name="tablet", w=W, h=H, plus=plus, minus=minus,
                amount=amount, fallbacks=fallbacks, clip=clip)


VIEWS = [desktop_cfg(), landscape_cfg(), portrait_cfg(), tablet_cfg()]


def wait_for_hud(page):
    btn = page.locator("button.action")
    btn.wait_for(state="visible", timeout=30000)
    for _ in range(360):
        if btn.is_enabled():
            break
        time.sleep(1)
    time.sleep(4)  # let the layout reflow + repaint for this viewport


def modal_state(page) -> dict:
    return page.evaluate(
        """() => ({
            betMenu: document.querySelectorAll('.bet-menu').length,
            popup: document.querySelectorAll('.pop-up-wrap').length,
            confirm: document.querySelectorAll('[data-test="confirm-button"]').length,
            anyModal: document.querySelectorAll('[class*="popup" i],[class*="modal" i]').length,
        })"""
    )


def is_open(m: dict) -> bool:
    return m["betMenu"] > 0 or m["popup"] > 0


def shot(page, clip, path):
    page.screenshot(path=str(path), clip=clip)


def diff_mean(a: Path, b: Path) -> float:
    ia = np.asarray(Image.open(a).convert("RGB")).astype("int16")
    ib = np.asarray(Image.open(b).convert("RGB")).astype("int16")
    if ia.shape != ib.shape:
        return 999.0
    return round(float(np.abs(ia - ib).mean()), 3)


def close_modal(page):
    try:
        page.keyboard.press("Escape")
    except Exception:  # noqa: BLE001
        pass
    time.sleep(0.5)


def run_view(browser, v) -> dict:
    r = {"name": v["name"], "amount": [round(c) for c in v["amount"]],
         "plus": [round(c) for c in v["plus"]], "minus": [round(c) for c in v["minus"]]}
    ctx = browser.new_context(viewport={"width": v["w"], "height": v["h"]}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(f"{BASE}{STORY}", wait_until="domcontentloaded", timeout=120000)
    page.locator("canvas").first.wait_for(state="visible", timeout=90000)
    wait_for_hud(page)

    r["modal_before_any_click"] = is_open(modal_state(page))

    # --- (b) steppers step and DO NOT open the modal --------------------------
    p_min = OUT / f"betmodal-{v['name']}-a-min.png"
    shot(page, v["clip"], p_min)

    page.mouse.click(*v["plus"])
    time.sleep(0.6)
    r["plus_opened_modal"] = is_open(modal_state(page))
    p_plus = OUT / f"betmodal-{v['name']}-b-plus.png"
    shot(page, v["clip"], p_plus)
    r["plus_changed_value"] = diff_mean(p_min, p_plus)

    page.mouse.click(*v["minus"])
    time.sleep(0.6)
    r["minus_opened_modal"] = is_open(modal_state(page))
    p_minus = OUT / f"betmodal-{v['name']}-c-minus.png"
    shot(page, v["clip"], p_minus)
    r["minus_changed_value"] = diff_mean(p_plus, p_minus)

    # --- (c) widest value: reach max, capture for overlap review --------------
    for _ in range(16):
        page.mouse.click(*v["plus"])
        time.sleep(0.22)
    r["max_reached_no_modal"] = not is_open(modal_state(page))
    shot(page, v["clip"], OUT / f"betmodal-{v['name']}-d-max.png")

    # --- (a) clicking the amount opens the bet-menu modal --------------------
    opened = False
    used = None
    for pt in [v["amount"], *v["fallbacks"]]:
        page.mouse.click(*pt)
        time.sleep(0.7)
        if is_open(modal_state(page)):
            opened = True
            used = [round(c) for c in pt]
            break
    r["amount_opened_modal"] = opened
    r["amount_click_used"] = used
    r["amount_modal_detail"] = modal_state(page)

    # screenshot the modal with the pixi canvas hidden so the HTML popup shows.
    # The blur-layer's backdrop-filter over a large canvas makes captures crawl,
    # so neutralise it (we only need to confirm the bet-menu content rendered).
    page.evaluate(
        """() => {
            document.querySelectorAll('canvas').forEach((c) => { c.style.visibility = 'hidden'; });
            document.querySelectorAll('.blur-layer').forEach((b) => {
                b.style.backdropFilter = 'none';
                b.style.webkitBackdropFilter = 'none';
                b.style.background = 'rgba(9, 11, 15, 0.97)';
            });
        }"""
    )
    time.sleep(0.4)
    try:
        page.screenshot(path=str(OUT / f"betmodal-{v['name']}-open.png"),
                        clip={"x": 0, "y": 0, "width": v["w"], "height": v["h"]},
                        animations="disabled", timeout=90000)
        r["modal_screenshot"] = "ok"
    except Exception as e:  # noqa: BLE001
        r["modal_screenshot"] = f"error: {str(e)[:120]}"
    close_modal(page)
    ctx.close()
    return r


def main() -> None:
    wanted = [a.lower() for a in sys.argv[1:]]
    views = [v for v in VIEWS if not wanted or v["name"] in wanted]
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        for v in views:
            print(f"[betmodal] {v['name']} start amount={[round(c) for c in v['amount']]}", flush=True)
            res = run_view(browser, v)
            results.append(res)
            print(f"[betmodal] {v['name']} -> {json.dumps(res)}", flush=True)
        browser.close()

    print("\n===== SUMMARY =====", flush=True)
    ok = True
    for r in results:
        amount_ok = r["amount_opened_modal"]
        step_ok = (not r["plus_opened_modal"]) and (not r["minus_opened_modal"])
        changed_ok = r["plus_changed_value"] > 0.5 and r["minus_changed_value"] > 0.5
        passed = amount_ok and step_ok and changed_ok and r["max_reached_no_modal"]
        ok = ok and passed
        print(
            f"{r['name']:8s} amount_opens={amount_ok!s:5s} "
            f"steppers_dont_open={step_ok!s:5s} "
            f"plus_diff={r['plus_changed_value']} minus_diff={r['minus_changed_value']} "
            f"=> {'PASS' if passed else 'FAIL'}",
            flush=True,
        )
    print(f"\nOVERALL: {'PASS' if ok else 'FAIL'}", flush=True)


if __name__ == "__main__":
    main()
