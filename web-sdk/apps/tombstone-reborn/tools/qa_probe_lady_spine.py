"""Verify the Lady Mirror SPINE rig loads + animates on the base game.

Loads the base story (desktop), waits for assets, then:
  - reports any console errors (esp. 'Spine: key ... not found')
  - shoots two frames ~1s apart and reports the mean diff over HER column with
    the animated room bg subtracted out (diff of consecutive frames minus a
    left-board reference strip) so we can tell she actually moves.

Run:  python tools/qa_probe_lady_spine.py
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


def mean_diff(a: Image.Image, b: Image.Image) -> float:
    diff = ImageChops.difference(a.convert("RGB"), b.convert("RGB"))
    hist = diff.histogram()
    total = sum((i % 256) * c for i, c in enumerate(hist))
    return total / (diff.width * diff.height * 3)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)
        time.sleep(34)  # fully settle first (avoid a pre-paint blank baseline)

        frames = []
        for i in range(6):
            p = OUT / f"spine_{i}.png"
            page.screenshot(path=str(p))
            frames.append(Image.open(p))
            time.sleep(0.4)
        browser.close()

    her = (int(1280 * 0.70), 40, 1280, 700)   # her column (right room)
    ref = (int(1280 * 0.05), 40, int(1280 * 0.12), 700)  # empty bg strip, far left
    print("=== motion (consecutive settled frames) ===", flush=True)
    for i in range(1, len(frames)):
        her_d = mean_diff(frames[i - 1].crop(her), frames[i].crop(her))
        ref_d = mean_diff(frames[i - 1].crop(ref), frames[i].crop(ref))
        print(f"  f{i-1}->f{i}: her={her_d:.3f}  bg_ref={ref_d:.3f}", flush=True)

    spine_errs = [e for e in errors if "Spine" in e or "spine" in e]
    print(f"\nconsole errors: {len(set(errors))} unique; spine-related: {len(spine_errs)}", flush=True)
    for e in sorted(set(errors))[:12]:
        print("   ", e[:200])


if __name__ == "__main__":
    sys.exit(main())
