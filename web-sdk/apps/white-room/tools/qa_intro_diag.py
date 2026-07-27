"""Screenshot-free diagnostic for the intro video wiring.

Confirms the intro mp4 is actually fetched by the loader, drives the carousel,
and reports any missing-asset errors or 'not found in loadedAssets' spam and
which key is missing - without screenshotting the (headless-unstable) video.
Run:  python tools/qa_intro_diag.py
"""

from __future__ import annotations

import time
from collections import Counter
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "components-game--component-loading-screen"


def main() -> None:
    console_msgs: list[str] = []
    net: list[str] = []
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.on("console", lambda m: console_msgs.append(m.text))
        page.on("request", lambda r: net.append(r.url) if ".mp4" in r.url else None)
        page.goto(BASE + STORY, wait_until="domcontentloaded")
        time.sleep(20)

        intro_loaded = [u for u in net if "intro_mirror" in u]
        print("intro mp4 requests:", len(intro_loaded))
        for u in intro_loaded:
            print("   ", u.split("?")[0].split("/")[-1])

        # find any 'not found in loadedAssets' key spam
        not_found = [m for m in console_msgs if "not found in the loadedAssets" in m or "not found in loadedAssets" in m]
        keys = Counter()
        for m in not_found:
            # message like: Sprite: key "X" is not found ...
            if 'key "' in m:
                keys[m.split('key "')[1].split('"')[0]] += 1
        print(f"\nmissing-key errors: {len(not_found)} total")
        for k, c in keys.most_common():
            print(f'   "{k}": {c}x')

        # drive the carousel CONTINUE
        before = len(console_msgs)
        page.mouse.click(640, 360)
        page.keyboard.press("Space")
        time.sleep(7)
        after_msgs = console_msgs[before:]
        intro_errs = [m for m in after_msgs if "introMirror" in m or "IntroVideo" in m]
        print(f"\nafter Space: {len(after_msgs)} new console msgs")
        print("introMirror/IntroVideo mentions:", len(intro_errs))
        for m in intro_errs[:5]:
            print("   ", m[:200])

        # error-type only summary (dedup)
        errs = sorted({m[:160] for m in console_msgs if "not found" not in m and "state_snapshot" not in m})
        print(f"\nother unique console lines: {len(errs)}")
        for e in errs[:20]:
            print("   ", e)
        browser.close()


if __name__ == "__main__":
    main()
