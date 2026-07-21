"""Full-page screenshot of the story to locate the HUD/BET pill.

Run: python tools/qa_full_shot.py [suffix]
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)
STORY = sys.argv[1] if len(sys.argv) > 1 else "mode-base-book--random"
WAIT = int(sys.argv[2]) if len(sys.argv) > 2 else 12
W, H = 1600, 900


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(f"{BASE}{STORY}", wait_until="commit", timeout=120000)
        time.sleep(WAIT)
        nm = f"full-{STORY}.png"
        page.screenshot(path=str(OUT / nm))
        print(f"[full] wrote {nm}", flush=True)
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
