"""Probe the BET stepper in every layout that owns one: click "+" until the bet
reaches its widest string ("$1,000.00") and confirm the +/- buttons never
overlap the amount.

Run: python tools/qa_probe_betstepper.py  (Storybook on :6001)

Loads mode-base-book--random (funds balance to 10000, bet starts at 1) at three
viewports chosen so each distinct HUD layout actually renders:
  - desktop      1600x900  -> LayoutDesktop  (== LayoutLandscape) ControlInfoBar
  - portrait      540x960  -> LayoutPortrait  LabelBet + flanking steppers
  - tablet       1200x1200 -> LayoutTablet    (almost-square) LabelBet + steppers
The "+"/"-" screen positions are derived from each layout's transforms. The
action book only runs on an Action click (which we never do), so the HUD stays
idle and the stepper is live.
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--random"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

UI_BASE = 150


def desktop_cfg():
    W, H = 1600, 900
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
        return ((bar_x + (cib_left + lx) * bar_scale) * cs,
                (bar_y + (cib_top + ly) * bar_scale) * cs)

    tl, br = scr(0, 0), scr(INFO, 88)
    clip = {"x": max(0, tl[0] - 12), "y": max(0, tl[1] - 14),
            "width": br[0] - tl[0] + 24, "height": br[1] - tl[1] + 28}
    return dict(name="desktop", w=W, h=H, plus=scr(459, 44), minus=scr(407, 44), clip=clip)


def portrait_cfg():
    W, H = 540, 960
    cs = min(W / 1080, H / 1920)  # 0.5, MainContainer bottom-aligned == centred here
    SW = 1080  # portrait STANDARD width (the layout's W, not the viewport)
    plus = ((SW * 0.5 - 250 + 200) * cs, (1920 - 112) * cs)
    minus = ((SW * 0.5 - 250 - 200) * cs, (1920 - 112) * cs)
    clip = {"x": 0, "y": 850, "width": 540, "height": 110}
    return dict(name="portrait", w=W, h=H, plus=plus, minus=minus, clip=clip)


def tablet_cfg():
    W, H = 1200, 1200  # ratio 1.0 -> almostSquare -> LayoutTablet
    cs = min(W / 1920, H / 1920)  # 0.625, centred at 0,0
    BET_X = 1920 * 0.135
    dx = 1920 * 0.095
    Y_PILL = 1920 * 0.82
    plus = ((BET_X + dx) * cs, (Y_PILL + 32) * cs)
    minus = ((BET_X - dx) * cs, (Y_PILL + 32) * cs)
    clip = {"x": 0, "y": 950, "width": 620, "height": 130}
    return dict(name="tablet", w=W, h=H, plus=plus, minus=minus, clip=clip)


VIEWS = [desktop_cfg(), portrait_cfg(), tablet_cfg()]


def wait_for_hud(page):
    """Wait for full asset load: the Action button flips enabled once painted."""
    btn = page.locator("button.action")
    btn.wait_for(state="visible", timeout=30000)
    for _ in range(360):
        if btn.is_enabled():
            break
        time.sleep(1)
    time.sleep(4)  # let the layout reflow + repaint for this viewport


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        for v in VIEWS:
            print(f"[probe] {v['name']} plus={v['plus']} minus={v['minus']}", flush=True)
            ctx = browser.new_context(
                viewport={"width": v["w"], "height": v["h"]}, device_scale_factor=2
            )
            page = ctx.new_page()
            page.goto(f"{BASE}{STORY}", wait_until="domcontentloaded", timeout=120000)
            page.locator("canvas").first.wait_for(state="visible", timeout=90000)
            wait_for_hud(page)

            page.screenshot(path=str(OUT / f"bet-{v['name']}-00-min.png"), clip=v["clip"])
            for _ in range(10):
                page.mouse.click(*v["plus"])
                time.sleep(0.45)
            page.screenshot(path=str(OUT / f"bet-{v['name']}-01-max.png"), clip=v["clip"])
            page.screenshot(path=str(OUT / f"bet-{v['name']}-01-full.png"))
            ctx.close()
            print(f"[probe] {v['name']} done", flush=True)

        browser.close()
        print("[done]", flush=True)


if __name__ == "__main__":
    main()
