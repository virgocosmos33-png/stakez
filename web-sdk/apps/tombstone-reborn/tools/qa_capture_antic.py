"""Dense early capture of the Seance story: anticipation columns + banner.

Run:  python tools/qa_capture_antic.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "final"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + "mode-base-book--bonus-level-1-the-seance", wait_until="domcontentloaded")

        button = page.locator("button.action")
        button.wait_for(state="visible", timeout=30000)
        for _ in range(120):
            if button.is_enabled():
                break
            time.sleep(1)
        button.click(timeout=5000)
        print("[antic] action clicked", flush=True)

        start = time.monotonic()
        # dense shots over the spin/anticipation window
        index = 0
        for tenths in range(30, 125, 7):  # 3.0s .. 12.5s, every 0.7s
            at = tenths / 10
            wait = at - (time.monotonic() - start)
            if wait > 0:
                time.sleep(wait)
            index += 1
            path = OUT / f"antic-{index:02d}-t{tenths:03d}.png"
            page.screenshot(path=str(path))
        print("[antic] dense window done", flush=True)

        # fsIntro press at ~20s, then banner shots (brightened art)
        wait = 20 - (time.monotonic() - start)
        if wait > 0:
            time.sleep(wait)
        page.mouse.click(640, 400)
        time.sleep(2.5)
        page.screenshot(path=str(OUT / "antic-banner.png"))
        time.sleep(1.5)
        page.screenshot(path=str(OUT / "antic-banner2.png"))
        browser.close()

    uniq = sorted(set(errors))
    print(f"[antic] {len(uniq)} unique console error(s)")
    for e in uniq[:10]:
        print("   ", e[:220])


if __name__ == "__main__":
    main()
