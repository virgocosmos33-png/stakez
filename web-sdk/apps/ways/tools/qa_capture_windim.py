"""Capture the post-win REST state to verify:
  1. winning symbols stay lit + STATIC (no postWin mesh morph)
  2. every non-winning cell sits under a dark overlay

Plays the deterministic mirrorBurstShowcase book (ends on a win) and shoots
several late frames; the rest state persists after the bet so the last frames
should all show winners lit / others dimmed.

Run:  python tools/qa_capture_windim.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--mirror-burst-showcase"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "windim"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)

        # first-load Vite compile + board load
        time.sleep(30)
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=30000)
            print("[windim] action clicked", flush=True)
        except Exception as error:  # noqa: BLE001
            print(f"[windim] action click failed: {error}", flush=True)

        # shoot the tail: the book resolves and the board rests in the win state
        start = time.monotonic()
        for at_seconds in (10, 14, 18, 22, 26, 30):
            wait = at_seconds - (time.monotonic() - start)
            if wait > 0:
                time.sleep(wait)
            path = OUT / f"rest-t{at_seconds:02d}.png"
            page.screenshot(path=str(path))
            print(f"[shot] {path.name}", flush=True)
        browser.close()

    print("\n=== console errors ===", flush=True)
    uniq = sorted(set(errors))
    print(f"{len(uniq)} unique error(s)")
    for e in uniq[:15]:
        print("   ", e[:220])


if __name__ == "__main__":
    sys.exit(main())
