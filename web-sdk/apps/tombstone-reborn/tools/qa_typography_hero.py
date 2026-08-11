"""Capture the display / hero surfaces and a large amount in the HUD console.

The estimator checks in qa_typography_shots.py prove the metrics; this proves the
pixels: a nine-figure win in the WIN well (does it grow instead of clipping?) and
the western display face wearing its metal fill on a real banner.

Run: python tools/qa_typography_hero.py [port] [story]
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / "qa-shots" / "typography"
OUT.mkdir(parents=True, exist_ok=True)

# seconds after the story action fires
FRAMES = [1, 3, 5, 8, 12, 16, 20, 25, 30, 36]


def main() -> None:
    port = sys.argv[1] if len(sys.argv) > 1 else "6013"
    story = sys.argv[2] if len(sys.argv) > 2 else "mode-bonus-book--max-win"
    tag = story.split("--")[-1]
    url = f"http://localhost:{port}/iframe.html?viewMode=story&id={story}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(url, wait_until="commit", timeout=120000)
        page.wait_for_selector("canvas", timeout=600000)
        time.sleep(4)
        btn = page.locator("button.action")
        for _ in range(60):
            try:
                if btn.count() and btn.first.is_enabled():
                    btn.first.click(timeout=2000)
                    break
            except Exception:  # noqa: BLE001
                pass
            time.sleep(1)
        start = time.time()
        for at in FRAMES:
            wait = at - (time.time() - start)
            if wait > 0:
                time.sleep(wait)
            out = OUT / f"hero-{tag}-{at:02d}s.png"
            page.screenshot(path=str(out))
            print(f"[shot] {out}", flush=True)
    os._exit(0)


if __name__ == "__main__":
    main()
