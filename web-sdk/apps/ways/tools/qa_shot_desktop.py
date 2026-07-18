"""Capture a single clean desktop HUD frame (waits for the story to resolve).

Run: python tools/qa_shot_desktop.py  (Storybook must be up on :6001)
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--random"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 900


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(f"{BASE}{STORY}", wait_until="commit", timeout=120000)
        time.sleep(20)
        # start the story action if the button is present
        for _ in range(6):
            try:
                page.get_by_text("Action", exact=True).first.click(timeout=3000)
                break
            except Exception:  # noqa: BLE001
                page.mouse.click(W * 0.5, H * 0.5)
                time.sleep(1)
        # wait for the play function to resolve (game fully loaded + spun)
        for _ in range(40):
            try:
                if page.get_by_text("resolved").count() > 0:
                    break
            except Exception:  # noqa: BLE001
                pass
            time.sleep(1)
        time.sleep(6)
        out = OUT / "hud-desktop.png"
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": W, "height": H})
        print(f"[shot] {out.name} ({W}x{H})", flush=True)
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
