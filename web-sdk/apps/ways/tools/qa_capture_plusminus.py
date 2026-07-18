"""Light capture of the +/- bet buttons (portrait + landscape HUD).

Clicks Action to reach idle, then full-page screenshot with a generous timeout.
Run:  python tools/qa_capture_plusminus.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "components-game--pre-spin"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)


def shot(play, prefix: str, w: int, h: int) -> None:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": w, "height": h})
    page.goto(BASE + STORY, wait_until="domcontentloaded")
    time.sleep(16)
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=20000)
        print(f"[{prefix}] action clicked", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"[{prefix}] no action: {error}", flush=True)
    time.sleep(4)
    page.screenshot(path=str(OUT / f"{prefix}-pm.png"), timeout=60000)
    print(f"[shot] {prefix}-pm.png", flush=True)
    browser.close()


def main() -> None:
    with sync_playwright() as play:
        shot(play, "port", 720, 1280)
        shot(play, "land", 1280, 720)


if __name__ == "__main__":
    sys.exit(main())
