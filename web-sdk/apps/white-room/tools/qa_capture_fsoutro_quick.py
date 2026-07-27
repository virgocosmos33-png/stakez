"""Quick outro check via the MODE_BASE/bookEvent freeSpinEnd story
(plays the freeSpinEnd event directly - no full bonus run needed).

Run:  python tools/qa_capture_fsoutro_quick.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-bookevent--free-spin-end"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "fsoutro"
OUT.mkdir(parents=True, exist_ok=True)


def run(play, prefix: str, viewport: tuple[int, int]) -> None:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(BASE + STORY, wait_until="domcontentloaded")

    button = page.locator("button.action")
    button.wait_for(state="visible", timeout=60000)
    for _ in range(120):
        if button.is_enabled():
            break
        time.sleep(1)
    button.click(timeout=5000)

    start = time.monotonic()
    for at, name in [(2.5, "counting"), (5, "mid"), (9, "settled")]:
        wait = at - (time.monotonic() - start)
        if wait > 0:
            time.sleep(wait)
        path = OUT / f"quick-{prefix}-{name}.png"
        page.screenshot(path=str(path))
        print(f"[shot] {path.name}", flush=True)

    browser.close()
    uniq = sorted(set(errors))
    print(f"[{prefix}] {len(uniq)} unique console error(s)")
    for e in uniq[:10]:
        print("   ", e[:200])


def main() -> None:
    with sync_playwright() as play:
        run(play, "land", (1280, 720))
        run(play, "port", (600, 1000))


if __name__ == "__main__":
    main()
