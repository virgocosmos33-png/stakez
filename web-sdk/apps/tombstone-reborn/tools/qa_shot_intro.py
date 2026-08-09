"""Grab in-app screenshots of the intro video mid-dive (bounded, can't hang).

Waits for the loader to FINISH (asset responses plateau) so the carousel is
actually up before pressing Space, then samples the dive. Every Playwright call
has an explicit timeout.
Run:  python tools/qa_shot_intro.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "components-game--component-loading-screen"
OUT = Path(__file__).resolve().parents[4] / "qa-shots" / "intro" / "play"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    count = {"n": 0}
    intro_seen = {"ok": False}

    def on_response(r):
        u = r.url
        if any(u.endswith(ext) or ext in u for ext in (".mp4", ".webp", ".png", ".json", ".atlas")):
            count["n"] += 1
        if "intro_mirror" in u:
            intro_seen["ok"] = True

    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.on("response", on_response)
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)

        # wait until asset responses plateau (loading finished -> carousel shown)
        last, stable = -1, 0
        for _ in range(45):  # up to ~90s
            time.sleep(2)
            if count["n"] == last and intro_seen["ok"] and count["n"] > 0:
                stable += 1
                if stable >= 4:  # ~8s with no new asset -> done loading
                    break
            else:
                stable = 0
            last = count["n"]
        print(f"asset responses={count['n']} intro_seen={intro_seen['ok']}", flush=True)
        time.sleep(2)
        page.screenshot(path=str(OUT / "carousel.png"), timeout=25000)
        print("carousel shot done", flush=True)

        page.mouse.click(640, 360)
        page.keyboard.press("Space")  # carousel oncontinue -> intro plays
        for i, dt in enumerate([0.7, 0.9, 1.1, 1.1, 1.2]):
            time.sleep(dt)
            try:
                page.screenshot(path=str(OUT / f"intro_{i}.png"), timeout=20000)
                print(f"intro shot {i} done", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"intro shot {i} failed: {str(e)[:120]}", flush=True)
        browser.close()


if __name__ == "__main__":
    main()
