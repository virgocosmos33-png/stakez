"""Confirm the Lady Mirror idle actually MOVES (not static).

Loads the base story (desktop), waits for load, then grabs several frames a
beat apart and reports the mean per-pixel diff over her right-side region.
A static sprite -> ~0 diff; a breathing/swaying idle -> clearly > 0.

Run:  python tools/qa_probe_lady_idle.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--random"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "lady"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)
        time.sleep(28)  # first-load compile + board settle (she shows at idle)

        shots = []
        for i in range(4):
            p = OUT / f"idle_{i}.png"
            page.screenshot(path=str(p))
            shots.append(p)
            print(f"[shot] {p.name}", flush=True)
            time.sleep(0.6)
        browser.close()

    # her region: right ~30% of the 1280-wide frame
    box = (int(1280 * 0.68), 40, 1280, 700)
    base = Image.open(shots[0]).convert("RGB").crop(box)
    print("\n=== idle motion (mean abs diff vs frame 0, her region) ===", flush=True)
    for p in shots[1:]:
        img = Image.open(p).convert("RGB").crop(box)
        diff = ImageChops.difference(base, img)
        hist = diff.histogram()
        # mean over all channels
        total = sum(i % 256 * c for i, c in enumerate(hist))
        pixels = diff.width * diff.height * 3
        print(f"  {p.name}: mean abs diff = {total / pixels:.3f}", flush=True)

    print(f"\nconsole errors: {len(set(errors))}", flush=True)
    for e in sorted(set(errors))[:10]:
        print("   ", e[:200])


if __name__ == "__main__":
    sys.exit(main())
