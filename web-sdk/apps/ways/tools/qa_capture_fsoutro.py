"""Capture the revamped 'YOU WON / TOTAL WIN' free-spins outro panel.

Plays the Seance bonus book, clicks through the veil intro + level banner,
lets the free spins run, then screenshots the outro (it waits for a press).

Run:  python tools/qa_capture_fsoutro.py [land|port]
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "mode-base-book--bonus-level-1-the-seance"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "fsoutro"
OUT.mkdir(parents=True, exist_ok=True)

MODES = {
    "land": (1280, 720),
    "port": (600, 1000),
}


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
    print(f"[{prefix}] action clicked", flush=True)

    cx = viewport[0] // 2
    cy = viewport[1] // 2
    # (time, kind, arg) - dismiss veil intro (press anywhere), then the level
    # banner CONTINUE pill (several y positions to be safe), then hands off
    timeline: list[tuple[float, str, object]] = [
        (28, "click", (cx, cy)),
        (30, "click", (cx, cy)),
        (33, "click", (cx, int(viewport[1] * 0.81))),
        (35, "click", (cx, int(viewport[1] * 0.85))),
        (37, "click", (cx, int(viewport[1] * 0.88))),
        (39, "shot", "after-banner"),
    ]
    # free spins run unattended; from t=110 alternate SHOT then CLICK so the
    # celebration scenes advance and the outro is always captured before a
    # click could dismiss it (first click on the outro only ends the count-up)
    for i, at in enumerate(range(110, 260, 9)):
        timeline.append((at, "shot", f"t{at}"))
        timeline.append((at + 3, "click", (cx, cy)))

    start = time.monotonic()
    for at, kind, arg in timeline:
        wait = at - (time.monotonic() - start)
        if wait > 0:
            time.sleep(wait)
        if kind == "click":
            x, y = arg  # type: ignore[misc]
            page.mouse.click(x, y)
            print(f"[{prefix}] click {arg} @t{at}", flush=True)
        else:
            path = OUT / f"{prefix}-{arg}.png"
            page.screenshot(path=str(path))
            print(f"[shot] {path.name}", flush=True)

    browser.close()
    uniq = sorted(set(errors))
    print(f"[{prefix}] {len(uniq)} unique console error(s)")
    for e in uniq[:10]:
        print("   ", e[:200])


def main() -> None:
    wanted = sys.argv[1:] or ["land", "port"]
    with sync_playwright() as play:
        for name in wanted:
            run(play, name, MODES[name])


if __name__ == "__main__":
    main()
