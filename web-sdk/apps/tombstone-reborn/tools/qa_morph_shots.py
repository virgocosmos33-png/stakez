"""Capture the morphed action-button pod (turbo · SPIN · autoplay).

Run: python tools/qa_morph_shots.py
Writes 1280x720 shots to qa-shots/hud/:
  morph_buttons_desktop.png
  morph_buttons_portrait.png

Storybook must be up on :6001. Windows quirk: os._exit(0) at the end to avoid
Playwright teardown hangs.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

STORY = "components-game--pre-spin"

SHOTS = [
    ("gold", 1280, 720),
]


def click_action(page) -> bool:
    btn = page.locator("button.action")
    for _ in range(130):
        try:
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=2000)
                return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1)
    return False


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, w, h in SHOTS:
            ctx = browser.new_context(
                viewport={"width": w, "height": h}, device_scale_factor=1
            )
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(f"{BASE}{STORY}", wait_until="commit", timeout=120000)
            time.sleep(4)
            click_action(page)
            time.sleep(10)
            out = OUT / f"morph_buttons_{name}.png"
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h})
            print(f"[shot] {out} errors={len(errors)}", flush=True)
            for e in errors[:5]:
                print(f"  [pageerror] {e}", flush=True)
            ctx.close()
        print("[done]", flush=True)
    os._exit(0)


if __name__ == "__main__":
    main()
