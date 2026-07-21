"""Capture the base-game desktop HUD to verify the balance/bet panel is HUD gold.

Run: python tools/qa_palette_shot.py
Writes web-sdk/qa-shots/hud/palette_desktop.png (1280x720) and reports any
console/page errors. Storybook must be up on :6001.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
SID = "components-game--pre-spin"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1280, 720


def click_action(page) -> bool:
    btn = page.locator("button.action")
    for _ in range(130):
        try:
            if btn.count() and btn.first.is_enabled():
                label = (btn.first.inner_text() or "").strip()
                # skip the blank "Initialising..." state
                if label and "Init" not in label:
                    btn.first.click(timeout=2000)
                    return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1)
    return False


def main() -> None:
    errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(f"{BASE}{SID}", wait_until="commit", timeout=120000)
        time.sleep(5)
        clicked = click_action(page)
        time.sleep(9)
        full = OUT / "palette_gold_outlines.png"
        page.screenshot(path=str(full), clip={"x": 0, "y": 0, "width": W, "height": H})
        print(f"[shot] {full} (action_clicked={clicked})", flush=True)
        print(f"[errors] {len(errors)}", flush=True)
        for e in errors:
            print(f"  {e}", flush=True)
        ctx.close()
    os._exit(0)


if __name__ == "__main__":
    main()
