"""Quick single-shot probe of the twoSymbolWays story:
plays the book, waits for the end-of-spin glint, shoots one frame, reports
console errors. Short + non-looping so it finishes fast.

Run:  python tools/qa_probe_twoways.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--two-symbol-ways"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "twoways"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)
        time.sleep(28)
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=30000)
            print("[twoways] action clicked", flush=True)
        except Exception as error:  # noqa: BLE001
            print(f"[twoways] action click failed: {error}", flush=True)

        # let the win present + count up, then the glint sweep begins
        time.sleep(9)
        path = OUT / "rest.png"
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
