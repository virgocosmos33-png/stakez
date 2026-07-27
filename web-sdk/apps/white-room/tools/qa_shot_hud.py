"""Capture the dark-matte + gold HUD chrome at desktop + portrait + landscape.

Run: python tools/qa_shot_hud.py  (Storybook must be up on :6001)
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--random"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

VIEWPORTS = [
    ("desktop", 1600, 900),
    ("portrait", 560, 980),
    ("landscape", 900, 440),
    ("tablet", 860, 820),
]


def click_action(page, w: int, h: int) -> None:
    for _ in range(6):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=3000)
            return
        except Exception:  # noqa: BLE001
            page.mouse.click(w * 0.5, h * 0.5)
            time.sleep(1)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        first = True
        for name, w, h in VIEWPORTS:
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
            page = ctx.new_page()
            page.goto(f"{BASE}{STORY}", wait_until="commit", timeout=120000)
            time.sleep(30 if first else 26)
            click_action(page, w, h)
            time.sleep(9)
            out = OUT / f"hud-{name}.png"
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h})
            print(f"[shot] {out.name} ({w}x{h})", flush=True)
            ctx.close()
            first = False
        browser.close()


if __name__ == "__main__":
    main()
