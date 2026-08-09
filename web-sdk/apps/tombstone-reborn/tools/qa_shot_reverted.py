"""Capture the Bonus Buy modal after reverting the transparent-icon swap.
Desktop + portrait, in mixed-affordability and $0-greyed states, so we can
confirm the ORIGINAL plaques render (no white boxes / broken images), the mono
theme is intact, and affordability greying still works.
Run from web-sdk/apps/ways  (Storybook :6001).
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)
MODAL = ".sheet, .ui-popup-standard-content-wrap"

SHOTS = [
    ("buybonus-reverted-mixed-portrait", "components-game--buy-menu-mixed", {"width": 480, "height": 900}),
    ("buybonus-reverted-greyed-desktop", "components-game--buy-menu-greyed", {"width": 1280, "height": 860}),
    ("buybonus-reverted-greyed-portrait", "components-game--buy-menu-greyed", {"width": 480, "height": 900}),
]


def goto_retry(page, url, tries=3):
    for i in range(tries):
        try:
            page.goto(url, wait_until="commit", timeout=90000)
            return True
        except Exception as e:  # noqa: BLE001
            print(f"[retry {i+1}] goto failed: {e}", flush=True)
            time.sleep(3)
    return False


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


def open_modal(page, tries=30) -> bool:
    for _ in range(tries):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=2500)
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2.0)
        if page.locator(MODAL).count() > 0:
            return True
    return False


def wait_images(page, timeout=25) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            ok = page.evaluate(
                """() => {
                const imgs = [...document.querySelectorAll('.card-art')];
                if (imgs.length === 0) return false;
                return imgs.every(i => i.complete && i.naturalWidth > 0);
            }"""
            )
        except Exception:  # noqa: BLE001
            ok = False
        if ok:
            return True
        time.sleep(1)
    return False


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 860})
        page = ctx.new_page()
        goto_retry(page, f"{BASE}components-game--buy-menu")
        wait_ready(page, 160)
        for name, story, vp in SHOTS:
            page.set_viewport_size(vp)
            goto_retry(page, f"{BASE}{story}")
            wait_ready(page, 130)
            opened = open_modal(page)
            imgs_ok = wait_images(page)
            # report broken images explicitly
            broken = page.evaluate(
                """() => [...document.querySelectorAll('.card-art')]
                    .filter(i => !(i.complete && i.naturalWidth > 0))
                    .map(i => i.getAttribute('src')).length"""
            )
            page.evaluate(
                "() => document.querySelectorAll('canvas').forEach(c => { c.style.visibility='hidden'; })"
            )
            time.sleep(0.6)
            try:
                el = page.locator(MODAL).first
                el.screenshot(path=str(OUT / f"{name}.png"))
                where = "element"
            except Exception:
                page.screenshot(path=str(OUT / f"{name}.png"))
                where = "fullpage"
            print(f"[shot] {name}.png ({where}) open={opened} imgs_ok={imgs_ok} broken={broken}", flush=True)
        ctx.close()
        browser.close()
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
