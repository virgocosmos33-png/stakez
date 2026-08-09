"""Capture the Bonus Buy menu at 1280x720 to verify the cards now render with the
outer black removed (transparent) on the menu background.

Run from web-sdk/apps/ways:  python tools/qa_shot_buybonus_transparent.py  (Storybook :6001)
"""
from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

STORY = "components-game--buy-menu"
BASE = f"http://localhost:6001/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)
MODAL_SELECTORS = ".sheet, .ui-popup-standard-content-wrap, .shell"


def wait_ready(page, timeout=150) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            txt = page.evaluate("() => (document.body && document.body.innerText) || ''")
        except Exception:
            txt = ""
        if txt and "nitialis" not in txt:
            return True
        time.sleep(1.5)
    return False


def open_modal(page) -> bool:
    for _ in range(16):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=2500)
        except Exception:
            pass
        time.sleep(1.5)
        if page.locator(MODAL_SELECTORS).count() > 0:
            return True
    return False


def main() -> None:
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 720},
                                  device_scale_factor=1)
        page = ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)

        page.goto(BASE, wait_until="commit", timeout=120000)
        ready = wait_ready(page, 150)
        opened = open_modal(page)
        time.sleep(1.0)
        # hide the pixi canvas so it doesn't composite over the HTML modal
        page.evaluate(
            "() => document.querySelectorAll('canvas').forEach(c => c.style.visibility='hidden')"
        )
        time.sleep(0.5)
        out = OUT / "buybonus_transparent.png"
        page.screenshot(path=str(out))
        print(f"ready={ready} modal_open={opened} shot={out}")
        print(f"page_errors={len(errors)}")
        for e in errors[:20]:
            print("  ERR:", e[:200])
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
