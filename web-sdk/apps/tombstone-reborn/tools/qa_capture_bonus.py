"""Capture the Seance bonus story end-to-end, pressing through every gate:
fsIntro panel -> LEVEL banner CONTINUE -> free spins -> outro.

Run:  python tools/qa_capture_bonus.py
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "final"
OUT.mkdir(parents=True, exist_ok=True)

# (time, kind, arg): shot = screenshot, click = mouse click at (x, y)
TIMELINE: list[tuple[float, str, object]] = [
    (5, "shot", "spin"),
    (7, "shot", "antic1"),
    (8.5, "shot", "antic2"),
    (10, "shot", "antic3"),
    (13, "shot", "win"),
    (20, "shot", "fsintro"),
    (21, "click", (640, 400)),  # press anywhere on the fsIntro panel
    (23, "shot", "banner"),
    (24.5, "shot", "banner2"),
    (26, "click", (640, 610)),  # banner CONTINUE (center-lower)
    (27, "click", (640, 585)),
    (28, "click", (640, 635)),
    (29, "shot", "after-banner"),
    (36, "shot", "fs1"),
    (44, "shot", "fs2"),
    (52, "shot", "fs3"),
    (60, "shot", "fs4"),
    (70, "shot", "fs5"),
    (80, "shot", "fs6"),
    (90, "shot", "fs7"),
    (100, "shot", "fs8"),
    (110, "shot", "fs9"),
    (120, "shot", "fs10"),
    (130, "shot", "outro1"),
    (138, "shot", "outro2"),
    (140, "click", (640, 400)),
    (146, "shot", "outro3"),
    (152, "shot", "end"),
]


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + "mode-base-book--bonus-level-1-the-seance", wait_until="domcontentloaded")

        # wait until preload finishes and the story's Action button becomes enabled
        button = page.locator("button.action")
        try:
            button.wait_for(state="visible", timeout=30000)
            for _ in range(120):
                if button.is_enabled():
                    break
                time.sleep(1)
            button.click(timeout=5000)
            print("[seance] action clicked", flush=True)
        except Exception as error:  # noqa: BLE001
            print(f"[seance] action click failed: {error}", flush=True)

        start = time.monotonic()
        for at, kind, arg in TIMELINE:
            wait = at - (time.monotonic() - start)
            if wait > 0:
                time.sleep(wait)
            if kind == "click":
                x, y = arg  # type: ignore[misc]
                page.mouse.click(x, y)
                print(f"[click] {arg} @t{at}", flush=True)
            else:
                path = OUT / f"seance2-{arg}.png"
                page.screenshot(path=str(path))
                print(f"[shot] {path.name}", flush=True)
        browser.close()

    uniq = sorted(set(errors))
    print(f"[seance] {len(uniq)} unique console error(s)")
    for e in uniq[:10]:
        print("   ", e[:220])


if __name__ == "__main__":
    main()
