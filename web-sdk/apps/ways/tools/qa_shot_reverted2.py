"""Capture the remaining reverted Bonus Buy shots — a FRESH browser per shot to
avoid the headless crash seen when reusing one context across many WebGL reloads.
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
    ("buybonus-reverted-mixed-portrait", "components-game--buy-menu-mixed", 480, 900),
    ("buybonus-reverted-greyed-desktop", "components-game--buy-menu-greyed", 1280, 860),
    ("buybonus-reverted-greyed-portrait", "components-game--buy-menu-greyed", 480, 900),
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


def wait_images(page, timeout=25):
    end = time.time() + timeout
    while time.time() < end:
        try:
            ok = page.evaluate(
                """() => { const a=[...document.querySelectorAll('.card-art')];
                    return a.length>0 && a.every(i=>i.complete && i.naturalWidth>0); }"""
            )
        except Exception:  # noqa: BLE001
            ok = False
        if ok:
            return True
        time.sleep(1)
    return False


def capture(name, story, w, h) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        try:
            page.goto(f"{BASE}{story}", wait_until="commit", timeout=90000)
            wait_ready(page, 150)
            opened = open_modal(page)
            imgs_ok = wait_images(page)
            broken = page.evaluate(
                """() => [...document.querySelectorAll('.card-art')]
                    .filter(i => !(i.complete && i.naturalWidth>0)).length"""
            )
            page.evaluate(
                "() => document.querySelectorAll('canvas').forEach(c=>{c.style.visibility='hidden';})"
            )
            time.sleep(0.6)
            try:
                page.locator(MODAL).first.screenshot(path=str(OUT / f"{name}.png"))
                where = "element"
            except Exception:
                page.screenshot(path=str(OUT / f"{name}.png"))
                where = "fullpage"
            print(f"[shot] {name}.png ({where}) open={opened} imgs_ok={imgs_ok} broken={broken}", flush=True)
        finally:
            ctx.close()
            browser.close()


def main() -> None:
    for name, story, w, h in SHOTS:
        for attempt in range(2):
            try:
                capture(name, story, w, h)
                break
            except Exception as e:  # noqa: BLE001
                print(f"[warn] {name} attempt {attempt+1} failed: {e}", flush=True)
                time.sleep(3)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
