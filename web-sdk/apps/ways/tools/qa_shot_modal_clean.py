"""Capture the mono pay-table + bet menu cleanly.

The pixi canvas composites over the HTML portal, so we hide the canvas before
shooting. Headless WebGL cold-boot is slow, so we WARM the game once (reusing a
single page/context) and poll readiness before opening each modal.

Run: python tools/qa_shot_modal_clean.py  (Storybook on :6001)
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1280, 860
STORIES = [
    ("paytable-mono", "components-game--pay-table"),
    ("betmenu-mono", "components-game--bet-menu"),
]


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


def capture(page, name, story) -> bool:
    page.goto(f"{BASE}{story}", wait_until="commit", timeout=120000)
    wait_ready(page, 120)
    opened = False
    for _ in range(16):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=2500)
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2.5)
        if page.locator(".shell, .ui-popup-standard-content-wrap").count() > 0:
            opened = True
            break
    time.sleep(1.2)
    page.evaluate(
        "() => document.querySelectorAll('canvas').forEach(c => { c.style.visibility='hidden'; })"
    )
    time.sleep(0.5)
    page.screenshot(path=str(OUT / f"{name}.png"), clip={"x": 0, "y": 0, "width": W, "height": H})
    print(f"[shot] {name}.png (modal={opened})", flush=True)
    return opened


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H})
        page = ctx.new_page()
        # warm once so the WebGL context + assets are cached for all targets
        page.goto(f"{BASE}components-game--buy-menu", wait_until="commit", timeout=120000)
        wait_ready(page, 150)
        for name, story in STORIES:
            capture(page, name, story)
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
