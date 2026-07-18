"""Capture the three new systems: bg video, symbol spines, cut-split blades.

  1. mirror-burst showcase, dense 0.4s cadence over the burst/split window
     (blade sweep is ~300ms so only a dense strip can catch it)
  2. maxwin showcase early frames: symbol win spines + ambient bg video

Writes PNGs into qa-shots/round3/ and prints console errors per story.
Run:  python tools/qa_capture_round3.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "round3"
OUT.mkdir(parents=True, exist_ok=True)


def capture(play, story_id: str, prefix: str, plan: list[tuple[float, str]]) -> list[str]:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(BASE + story_id, wait_until="domcontentloaded")

    time.sleep(12)
    try:
        page.get_by_text("Action", exact=True).first.click(timeout=5000)
        print(f"[{prefix}] action clicked", flush=True)
    except Exception as error:  # noqa: BLE001
        print(f"[{prefix}] action click failed: {error}", flush=True)

    start = time.monotonic()
    for at_seconds, name in plan:
        wait = at_seconds - (time.monotonic() - start)
        if wait > 0:
            time.sleep(wait)
        page.screenshot(path=str(OUT / f"{prefix}-{name}.png"))
        print(f"[shot] {prefix}-{name}.png", flush=True)
    browser.close()
    return errors


def main() -> None:
    with sync_playwright() as play:
        all_errors: dict[str, list[str]] = {}

        # dense strip over the burst -> reveal -> split window
        burst_plan = [(0.0, "t000")]
        t = 3.0
        while t <= 14.0:
            burst_plan.append((t, f"t{int(t * 10):03d}"))
            t += 0.4
        all_errors["burst"] = capture(
            play, "mode-base-book--mirror-burst-showcase", "burst", burst_plan
        )

        # early win frames: symbol spines + background video behind the board
        all_errors["maxwin"] = capture(
            play,
            "mode-base-book--maxwin-showcase",
            "maxwin",
            [(2.0, "t02"), (3.0, "t03"), (3.5, "t035"), (4.0, "t04"),
             (4.5, "t045"), (5.0, "t05"), (6.0, "t06"), (8.0, "t08")],
        )

    print("\n=== console errors ===", flush=True)
    for story, errs in all_errors.items():
        uniq = sorted(set(errs))
        print(f"[{story}] {len(uniq)} unique error(s)")
        for e in uniq[:10]:
            print("   ", e[:220])


if __name__ == "__main__":
    sys.exit(main())
