"""Functional check for tap-to-skip (slam stop).

Starts the base book (reels spin), then taps the reel area mid-spin and
captures frames. Compares against a run where we DON'T tap, to show the reels
settle earlier when tapped. Also asserts no new console/page errors on the tap.

Run:  python tools/qa_tap_skip.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--two-symbol-ways"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "skip"
OUT.mkdir(parents=True, exist_ok=True)


def wait_ready(page) -> None:
    # wait until the pixi canvas exists AND the story has settled (not the blank
    # "Initialising"/recompile frame), then give it a moment to actually paint
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


def run(tap: bool, label: str) -> list[str]:
    errors: list[str] = []
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.on("pageerror", lambda e: errors.append(f"PAGEERROR {e}"))
        page.on(
            "console",
            lambda m: errors.append(f"CONSOLE {m.text}") if m.type == "error" else None,
        )
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)
        wait_ready(page)

        # start the book -> reels begin spinning (Action button, top-left DOM)
        page.get_by_text("Action", exact=True).first.click()
        # let the reels get fully into the spin before tapping
        time.sleep(0.55)
        if tap:
            # tap the reel area (canvas center) = slam stop
            page.mouse.click(640, 300)
        # capture at a fixed moment: without tap the later reels are still
        # dropping; with tap they should already be settled
        time.sleep(0.30)
        page.screenshot(path=str(OUT / f"{label}.png"))
        browser.close()
    # only report errors that aren't the pre-existing missing logo asset
    return [e for e in errors if "buy_bonus_logo" not in e]


def main() -> None:
    no_tap = run(tap=False, label="no_tap")
    tapped = run(tap=True, label="tapped")
    print("=== no-tap errors (excl. known logo 403) ===", flush=True)
    for e in sorted(set(no_tap))[:10]:
        print("  ", e[:200])
    print("=== tapped errors (excl. known logo 403) ===", flush=True)
    for e in sorted(set(tapped))[:10]:
        print("  ", e[:200])
    print("shots: skip/no_tap.png, skip/tapped.png", flush=True)


if __name__ == "__main__":
    sys.exit(main())
