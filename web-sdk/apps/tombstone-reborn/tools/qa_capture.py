"""Headless Storybook capture for final Madam Mirror QA.

Captures:
  1. COMPONENTS/<Game> component (loadingScreen) -> intro carousel cards
  2. MODE_BASE/book maxwinShowcase -> coin shower / win celebration frames
  3. MODE_BASE/book mirrorBurstShowcase -> mirror burst + win frames

Writes PNGs into qa-shots/final/ and prints console errors per story.
Run:  python tools/qa_capture.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "final"
OUT.mkdir(parents=True, exist_ok=True)


def snap(page, name: str) -> None:
    path = OUT / f"{name}.png"
    page.screenshot(path=str(path))
    print(f"[shot] {path.name}", flush=True)


def capture(play, story_id: str, prefix: str, plan: list[tuple[float, str]]) -> list[str]:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(BASE + story_id, wait_until="domcontentloaded")

    # wait for the board to load, then press the story's Action button
    time.sleep(10)
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
        snap(page, f"{prefix}-{name}")
    browser.close()
    return errors


def main() -> None:
    with sync_playwright() as play:
        all_errors: dict[str, list[str]] = {}

        # max win showcase: coin shower + win level celebration (long tail)
        all_errors["maxwin"] = capture(
            play,
            "mode-base-book--maxwin-showcase",
            "maxwin",
            [(6, "t06"), (12, "t12"), (18, "t18"), (24, "t24"),
             (30, "t30"), (36, "t36"), (44, "t44"), (52, "t52"), (60, "t60")],
        )

        # mirror burst showcase
        all_errors["burst"] = capture(
            play,
            "mode-base-book--mirror-burst-showcase",
            "burst",
            [(4, "t04"), (8, "t08"), (12, "t12"), (16, "t16"), (22, "t22")],
        )

    print("\n=== console errors ===", flush=True)
    for story, errs in all_errors.items():
        uniq = sorted(set(errs))
        print(f"[{story}] {len(uniq)} unique error(s)")
        for e in uniq[:10]:
            print("   ", e[:220])


if __name__ == "__main__":
    sys.exit(main())
