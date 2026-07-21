"""Hover-state probe for the BET stepper +/- cells.

Run: python tools/qa_hover_betstepper.py [suffix]   (Storybook on :6001)

The mode-base-book--random story boots slowly (loading screen ~30-60s) and only
plays on manual action, so it settles to an IDLE HUD. We poll full-page shots
until the SPIN button (bottom-right white blob) AND the BET pill (bottom-left
white outline) are actually painted, then hover the +/- cells and crop the pill.

- plus:          hover works immediately (bet starts at min, canInc == true)
- minus-disabled: hover - while still at min (canDec == false) => no white wash
- minus:         click + once (raises bet => canDec == true), then hover -

Optional argv[1] is appended to the output filenames (e.g. "before" / "after").
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--random"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

SUFFIX = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 1600, 900


def name(base: str) -> str:
    return f"{base}-{SUFFIX}.png" if SUFFIX else f"{base}.png"


def white_ratio(im: Image.Image, box) -> float:
    crop = im.crop(box)
    n = crop.width * crop.height
    w = sum(1 for (r, g, b) in crop.getdata() if r > 225 and g > 225 and b > 225)
    return w / max(1, n)


def wait_for_idle_hud(page, timeout_s=160):
    """Poll full-page shots until SPIN (bottom-right) AND pill (bottom-left) are white.

    Measured white ratios:
      - blank "Initialising" page:  BR ~1.0  / BL ~1.0   (exclude via upper bound)
      - MADAM MIRROR loading screen: BR ~0.0  / BL ~0.0   (exclude via lower bound)
      - idle HUD (target):           BR ~0.094 / BL ~0.025 (middle band)
    """
    tmp = OUT / "_idle.png"
    deadline = time.time() + timeout_s
    br = bl = 0.0
    while time.time() < deadline:
        page.screenshot(path=str(tmp))
        im = Image.open(tmp).convert("RGB")
        iw, ih = im.size
        br = white_ratio(im, (iw // 2, ih // 2, iw, ih))
        bl = white_ratio(im, (0, int(ih * 0.85), int(iw * 0.25), ih))
        if 0.03 < br < 0.30 and 0.010 < bl < 0.10:
            return True, br, bl
        time.sleep(2)
    return False, br, bl


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(f"{BASE}{STORY}", wait_until="commit", timeout=120000)

        ok, br, bl = wait_for_idle_hud(page, timeout_s=160)
        print(f"[hover] idle={ok} br={br:.3f} bl={bl:.3f}", flush=True)
        time.sleep(1)

        clip = {"x": 0, "y": H - 96, "width": 210, "height": 96}
        # full-frame shot to confirm the pill is where we think it is
        page.screenshot(path=str(OUT / name("bethover-full")))

        yc = H - 48
        minus_xy = (35, yc)
        plus_xy = (162, yc)
        value_xy = (105, yc)

        # neutral baseline (mouse on the value zone, no stepper hover)
        page.mouse.move(*value_xy)
        time.sleep(0.5)
        page.screenshot(path=str(OUT / name("bethover-00-idle")), clip=clip)

        # hover PLUS (canInc == true at min bet)
        page.mouse.move(*plus_xy)
        time.sleep(0.7)
        page.screenshot(path=str(OUT / name("bethover-plus")), clip=clip)

        # hover MINUS while still at min ($1.00) => canDec == false:
        # must NOT paint the white wash, glyph stays disabled-grey
        page.mouse.move(*value_xy)
        time.sleep(0.4)
        page.mouse.move(*minus_xy)
        time.sleep(0.7)
        page.screenshot(path=str(OUT / name("bethover-minus-disabled")), clip=clip)
        page.mouse.move(*value_xy)
        time.sleep(0.4)

        # raise the bet so canDec becomes true, then hover MINUS
        page.mouse.click(*plus_xy)
        time.sleep(0.9)
        page.mouse.move(*value_xy)   # leave the plus cell
        time.sleep(0.5)
        page.mouse.move(*minus_xy)
        time.sleep(0.7)
        page.screenshot(path=str(OUT / name("bethover-minus")), clip=clip)

        print(f"[hover] wrote {name('bethover-plus')} / {name('bethover-minus')}", flush=True)
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
