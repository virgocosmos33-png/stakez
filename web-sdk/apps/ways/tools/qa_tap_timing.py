"""Measure reel settle-time with vs without tap-to-skip, on the SAME book.

After starting the book, poll a crop of the last-settling reels and detect when
motion stops. For the tapped run, tap the reels as soon as motion is first seen.
If slam-stop works, the tapped run settles noticeably sooner.

Run:  python tools/qa_tap_timing.py
"""

from __future__ import annotations

import io
import sys
import time
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--two-symbol-ways"
# crop of the right-hand reels (they settle last) in the 1280x720 viewport
CROP = (700, 70, 970, 600)
MOTION = 6.0  # mean-abs-diff above this = the reels are moving


def wait_ready(page) -> None:
    for _ in range(60):
        try:
            has_canvas = page.evaluate("!!document.querySelector('canvas')")
            txt = page.evaluate("document.body.innerText")
        except Exception:
            time.sleep(1)
            continue
        if has_canvas and ("Click action to start" in txt or "resolved" in txt):
            time.sleep(2.0)
            return
        time.sleep(1)


def crop_diff(page, prev: Image.Image | None):
    raw = page.screenshot()
    img = Image.open(io.BytesIO(raw)).convert("RGB").crop(CROP)
    if prev is None:
        return img, 0.0
    diff = ImageChops.difference(img, prev)
    hist = diff.histogram()
    # mean abs diff across all channels
    total = sum(i % 256 * count for i, count in enumerate(hist))
    mean = total / (diff.width * diff.height * 3)
    return img, mean


def run(tap: bool) -> float:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)
        wait_ready(page)

        page.get_by_text("Action", exact=True).first.click()
        t0 = time.time()
        prev = None
        seen_motion = False
        tapped = False
        settle_t = None
        still_count = 0
        while time.time() - t0 < 6.0:
            prev, mean = crop_diff(page, prev)
            now = time.time() - t0
            moving = mean > MOTION
            if moving:
                seen_motion = True
                still_count = 0
                if tap and not tapped:
                    page.mouse.click(640, 300)
                    tapped = True
            elif seen_motion:
                still_count += 1
                if still_count >= 2:  # stable for 2 polls after motion
                    settle_t = now
                    break
            time.sleep(0.08)
        browser.close()
    return settle_t if settle_t is not None else float("nan")


def main() -> None:
    no_tap = run(tap=False)
    tapped = run(tap=True)
    print(f"settle WITHOUT tap: {no_tap:.2f}s", flush=True)
    print(f"settle WITH tap:    {tapped:.2f}s", flush=True)
    if no_tap == no_tap and tapped == tapped:
        print(f"delta (saved): {no_tap - tapped:.2f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main())
