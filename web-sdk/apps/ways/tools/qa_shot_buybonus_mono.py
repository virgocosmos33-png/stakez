"""Capture the MONO Bonus Buy modal across layouts + the confirm dialog, plus
Pay Table / Settings for a regression check.

The pixi canvas composites over the HTML portal, so we hide the canvas before
shooting. Headless WebGL cold-boot is slow, so we warm the game once and reuse a
single page, re-sizing the viewport to drive the responsive layoutType:
  - desktop  : ratio >= 1.3 and min(w,h) > 480
  - portrait : ratio <= 0.8
  - landscape: ratio >= 1.3 and min(w,h) <= 480

Run from web-sdk/apps/ways:  python tools/qa_shot_buybonus_mono.py   (Storybook :6001)
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

BUY = "components-game--buy-menu"
PAY = "components-game--pay-table"

# (name, viewport) — viewport chosen to force the desired layoutType
LAYOUTS = [
    ("buybonus-desktop", {"width": 1280, "height": 860}),
    ("buybonus-portrait", {"width": 480, "height": 900}),
    ("buybonus-landscape", {"width": 960, "height": 440}),
]

# affordability states (desktop) — different story funds different cards
AFFORD = [
    ("buybonus-greyed", "components-game--buy-menu-greyed"),
    ("buybonus-mixed", "components-game--buy-menu-mixed"),
]

MODAL_SELECTORS = ".sheet, .ui-popup-standard-content-wrap, .shell"


def wait_ready(page, timeout=150) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            txt = page.evaluate("() => (document.body && document.body.innerText) || ''")
        except Exception:  # noqa: BLE001
            txt = ""
        if txt and "nitialis" not in txt:
            return True
        time.sleep(2)
    return False


def open_modal(page) -> bool:
    for _ in range(16):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=2500)
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2.0)
        if page.locator(MODAL_SELECTORS).count() > 0:
            return True
    return False


def hide_canvas(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('canvas').forEach(c => { c.style.visibility='hidden'; })"
    )
    time.sleep(0.4)


def shoot(page, name) -> None:
    """Screenshot the modal element if we can find it, else the full viewport."""
    hide_canvas(page)
    try:
        el = page.locator(MODAL_SELECTORS).first
        if el.count() > 0:
            el.screenshot(path=str(OUT / f"{name}.png"))
            print(f"[shot] {name}.png (element)", flush=True)
            return
    except Exception as e:  # noqa: BLE001
        print(f"[warn] element shot failed for {name}: {e}", flush=True)
    page.screenshot(path=str(OUT / f"{name}.png"))
    print(f"[shot] {name}.png (fullpage)", flush=True)


def capture_buybonus_layouts(page) -> None:
    for name, vp in LAYOUTS:
        page.set_viewport_size(vp)
        page.goto(f"{BASE}{BUY}", wait_until="commit", timeout=120000)
        wait_ready(page, 120)
        opened = open_modal(page)
        shoot(page, name)
        print(f"       {name}: modal_open={opened} vp={vp}", flush=True)


def capture_affordability(page) -> None:
    page.set_viewport_size({"width": 1280, "height": 860})
    for name, story in AFFORD:
        page.goto(f"{BASE}{story}", wait_until="commit", timeout=120000)
        wait_ready(page, 120)
        opened = open_modal(page)
        shoot(page, name)
        print(f"       {name}: modal_open={opened}", flush=True)


def capture_confirm(page) -> None:
    page.set_viewport_size({"width": 1280, "height": 860})
    page.goto(f"{BASE}{BUY}", wait_until="commit", timeout=120000)
    wait_ready(page, 120)
    open_modal(page)
    hide_canvas(page)
    # click a card action to open the confirm dialog (prefer a BUY)
    clicked = False
    for getter in (
        lambda: page.get_by_role("button", name="BUY").first,
        lambda: page.locator(".bonus-card-wrap button").first,
    ):
        try:
            getter().click(timeout=3000)
            clicked = True
            break
        except Exception:  # noqa: BLE001
            continue
    time.sleep(1.5)
    hide_canvas(page)
    shoot(page, "buybonus-confirm")
    print(f"       confirm: clicked={clicked}", flush=True)


def capture_paytable_and_settings(page) -> None:
    page.set_viewport_size({"width": 1280, "height": 860})
    page.goto(f"{BASE}{PAY}", wait_until="commit", timeout=120000)
    wait_ready(page, 120)
    opened = open_modal(page)
    shoot(page, "paytable-mono")
    print(f"       paytable: modal_open={opened}", flush=True)
    # switch to the sound settings tab (gear rail button) and shoot again
    try:
        page.get_by_label("Sound settings").click(timeout=3000)
        time.sleep(0.8)
        shoot(page, "settings-mono")
        print("       settings: ok", flush=True)
    except Exception as e:  # noqa: BLE001
        print(f"[warn] settings tab click failed: {e}", flush=True)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 860})
        page = ctx.new_page()
        # warm once so WebGL + assets are cached for every later target
        page.goto(f"{BASE}{BUY}", wait_until="commit", timeout=120000)
        wait_ready(page, 150)

        capture_buybonus_layouts(page)
        capture_affordability(page)
        capture_confirm(page)
        capture_paytable_and_settings(page)

        ctx.close()
        browser.close()
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
