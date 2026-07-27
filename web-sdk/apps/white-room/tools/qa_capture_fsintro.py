"""Capture the 'THE VEIL PARTS' free-spins intro for all three bonus levels
(landscape) plus a portrait run of level 1.

The intro waits for CONTINUE, so late screenshots always land on the panel.

Run:  python tools/qa_capture_fsintro.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "fsintro"
OUT.mkdir(parents=True, exist_ok=True)

RUNS = [
    ("mode-base-book--bonus-level-1-the-seance", (1280, 720), "l1-land"),
    ("mode-base-book--bonus-level-2-the-other-side", (1280, 720), "l2-land"),
    ("mode-base-book--bonus-level-3-blood-moon", (1280, 720), "l3-land"),
    ("mode-base-book--bonus-level-1-the-seance", (600, 1000), "l1-port"),
]
SHOT_TIMES = [26, 34, 44, 56]


def capture(play, story: str, viewport: tuple[int, int], prefix: str) -> list[str]:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(BASE + story, wait_until="domcontentloaded")

    button = page.locator("button.action")
    button.wait_for(state="visible", timeout=60000)
    for _ in range(120):
        if button.is_enabled():
            break
        time.sleep(1)
    button.click(timeout=5000)
    print(f"[{prefix}] action clicked", flush=True)

    start = time.monotonic()
    for at in SHOT_TIMES:
        wait = at - (time.monotonic() - start)
        if wait > 0:
            time.sleep(wait)
        path = OUT / f"{prefix}-t{at}.png"
        page.screenshot(path=str(path))
        print(f"[shot] {path.name}", flush=True)

    browser.close()
    return errors


def main() -> None:
    import sys

    only = set(sys.argv[1:])  # optional prefixes, e.g. l2-land l3-land
    with sync_playwright() as play:
        for story, viewport, prefix in RUNS:
            if only and prefix not in only:
                continue
            errors = capture(play, story, viewport, prefix)
            uniq = sorted(set(errors))
            print(f"[{prefix}] {len(uniq)} unique console error(s)")
            for e in uniq[:8]:
                print("   ", e[:200])


if __name__ == "__main__":
    main()
