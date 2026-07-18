"""Capture the idle HUD to verify the re-themed buttons / menu / tickers.

Loads the <Game> preSpin story (skipLoadingScreen) and screenshots the full
control layer in landscape and portrait, plus a menu-drawer-open shot.
Run:  python tools/qa_capture_hud.py
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


def shot(play, prefix: str, w: int, h: int) -> list[str]:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": w, "height": h})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(BASE + STORY, wait_until="domcontentloaded")
    time.sleep(12)
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=8000)
        print(f"[{prefix}] action clicked", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"[{prefix}] no action button: {error}", flush=True)
    time.sleep(3)
    page.screenshot(path=str(OUT / f"{prefix}-idle.png"))
    print(f"[shot] {prefix}-idle.png", flush=True)
    # hover the spin button area to show hover aura (landscape spin sits right/center)
    try:
        page.mouse.move(w * 0.92, h * 0.5)
        time.sleep(0.6)
        page.screenshot(path=str(OUT / f"{prefix}-hover.png"))
        print(f"[shot] {prefix}-hover.png", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"[{prefix}] hover failed: {error}", flush=True)
    browser.close()
    return errors


def main() -> None:
    with sync_playwright() as play:
        errs = {}
        errs["land"] = shot(play, "land", 1280, 720)
        errs["port"] = shot(play, "port", 720, 1280)
    print("\n=== console errors ===", flush=True)
    for k, v in errs.items():
        uniq = sorted(set(v))
        print(f"[{k}] {len(uniq)} unique error(s)")
        for e in uniq[:12]:
            print("   ", e[:220])


if __name__ == "__main__":
    sys.exit(main())
