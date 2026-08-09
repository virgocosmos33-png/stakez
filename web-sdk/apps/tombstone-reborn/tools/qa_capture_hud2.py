"""Capture a funded, idle HUD (balance set) so enabled/accent buttons show.

Loads a base book story but does NOT click Action, so the game stays idle with
balance funded -> BET (accent), AUTO SPIN, TURBO, BUY BONUS all enabled.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--maxwin-showcase"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)


def shot(play, prefix: str, w: int, h: int) -> list[str]:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": w, "height": h})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(BASE + STORY, wait_until="domcontentloaded")
    # let the book story finish loading its full asset set + press-to-continue
    time.sleep(18)
    for _ in range(4):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=3000)
            break
        except Exception:  # noqa: BLE001
            page.mouse.click(w * 0.5, h * 0.5)
            time.sleep(1)
    # after the book resolves the HUD returns to a funded idle state
    time.sleep(22)
    page.mouse.move(w * 0.93, h * 0.42)
    time.sleep(0.7)
    page.screenshot(path=str(OUT / f"{prefix}-enabled.png"))
    print(f"[shot] {prefix}-enabled.png", flush=True)
    browser.close()
    return errors


def main() -> None:
    with sync_playwright() as play:
        e1 = shot(play, "land2", 1280, 720)
        e2 = shot(play, "port2", 720, 1280)
    for k, v in {"land2": e1, "port2": e2}.items():
        print(f"[{k}] {len(set(v))} unique error(s)")
        for e in sorted(set(v))[:10]:
            print("   ", e[:200])


if __name__ == "__main__":
    sys.exit(main())
