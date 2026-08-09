"""Verify the 'enter the mirror' intro video plays in the loading flow.

Loads the full <Game> loadingScreen story, waits for assets, advances past the
feature carousel (Space triggers oncontinue), then samples frames while the
intro video plays and after it hands off to the game.

Usage:
  python tools/qa_capture_intro.py land
  python tools/qa_capture_intro.py port
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "components-game--component-loading-screen"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "intro" / "play"
OUT.mkdir(parents=True, exist_ok=True)


def run(which: str) -> None:
    w, h = (1280, 720) if which == "land" else (720, 1280)
    errors: list[str] = []
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        page = browser.new_page(viewport={"width": w, "height": h})
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(BASE + STORY, wait_until="domcontentloaded")

        # wait for the post-load phase to finish (intro videos load here too),
        # by which point the carousel is shown
        time.sleep(20)
        page.screenshot(path=str(OUT / f"{which}-0-carousel.png"), timeout=60000)
        print(f"[{which}] carousel captured", flush=True)

        # focus the canvas and trigger the carousel CONTINUE (Space)
        page.mouse.click(w * 0.5, h * 0.5)
        page.keyboard.press("Space")
        print(f"[{which}] pressed Space -> intro should play", flush=True)

        # sample the intro playback (~5s) then the game hand-off
        for i in range(1, 8):
            time.sleep(0.8)
            page.screenshot(path=str(OUT / f"{which}-{i}-t{i*0.8:.1f}.png"), timeout=60000)
            print(f"[{which}] frame {i}", flush=True)

        browser.close()
    uniq = sorted(set(errors))
    print(f"[{which}] {len(uniq)} console error(s)")
    for e in uniq[:10]:
        print("   ", e[:200])


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "land")
