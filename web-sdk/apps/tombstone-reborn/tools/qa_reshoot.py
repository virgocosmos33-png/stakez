"""Re-capture the three shots that raced in the full run: the mixed-affordability
buy menu (art hadn't finished loading), the pay table, and the settings tab.
Adds an explicit image-load wait and a longer, more patient modal-open loop.
Run from web-sdk/apps/ways  (Storybook :6001).
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 860
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


def open_modal(page, tries=30) -> bool:
    for _ in range(tries):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=2500)
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2.0)
        if page.locator(MODAL_SELECTORS).count() > 0:
            return True
    return False


def wait_images(page, timeout=20) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            ok = page.evaluate(
                """() => {
                const imgs = [...document.querySelectorAll('.card-art, .dialog-image, .pay-cell img')];
                if (imgs.length === 0) return true;
                return imgs.every(i => i.complete && i.naturalWidth > 0);
            }"""
            )
        except Exception:  # noqa: BLE001
            ok = False
        if ok:
            return True
        time.sleep(1)
    return False


def hide_canvas(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('canvas').forEach(c => { c.style.visibility='hidden'; })"
    )
    time.sleep(0.4)


def shoot(page, name) -> None:
    hide_canvas(page)
    wait_images(page)
    time.sleep(0.5)
    try:
        el = page.locator(MODAL_SELECTORS).first
        if el.count() > 0:
            el.screenshot(path=str(OUT / f"{name}.png"))
            print(f"[shot] {name}.png (element)", flush=True)
            return
    except Exception as e:  # noqa: BLE001
        print(f"[warn] element shot {name}: {e}", flush=True)
    page.screenshot(path=str(OUT / f"{name}.png"), clip={"x": 0, "y": 0, "width": W, "height": H})
    print(f"[shot] {name}.png (clip)", flush=True)


def cap_story(page, name, story) -> None:
    page.goto(f"{BASE}{story}", wait_until="commit", timeout=120000)
    wait_ready(page, 130)
    opened = open_modal(page)
    wait_images(page)
    shoot(page, name)
    print(f"       {name}: modal_open={opened}", flush=True)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H})
        page = ctx.new_page()
        page.goto(f"{BASE}components-game--buy-menu", wait_until="commit", timeout=120000)
        wait_ready(page, 160)

        cap_story(page, "buybonus-mixed", "components-game--buy-menu-mixed")

        # pay table (patient) + settings tab
        page.goto(f"{BASE}components-game--pay-table", wait_until="commit", timeout=120000)
        wait_ready(page, 150)
        opened = open_modal(page, tries=40)
        wait_images(page)
        shoot(page, "paytable-mono")
        print(f"       paytable: modal_open={opened}", flush=True)
        try:
            page.get_by_label("Sound settings").click(timeout=8000)
            time.sleep(1.0)
            shoot(page, "settings-mono")
            print("       settings: ok", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[warn] settings click failed: {e}", flush=True)

        ctx.close()
        browser.close()
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
