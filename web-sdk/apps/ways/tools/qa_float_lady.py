"""Capture the floating Lady-Mirror scene (base + bonus) at 1280x720 to verify
the full figure (incl. head/face) floats beside the reels with clean edges.

Loads the scene stories, clicks Action, dismisses the one-shot intro, waits for
the board to settle (body text no longer "Initialising..."), then screenshots.

Run while Storybook is up on :6001.  ->  web-sdk/qa-shots/lady/
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "lady"
OUT.mkdir(parents=True, exist_ok=True)

JOBS = [
    ("float_base", "components-game--scene-base"),
    ("float_bonus", "components-game--scene-bonus"),
]


def settled(page) -> str:
    try:
        return page.evaluate("() => document.body.innerText.slice(0, 400)")
    except Exception:
        return ""


def capture(browser, label: str, story: str) -> list[str]:
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append("PAGEERROR: " + str(e)))
    page.goto(BASE + story, wait_until="commit", timeout=120000)

    try:
        page.get_by_text("Action", exact=True).first.click(timeout=180000)
    except Exception as e:  # noqa: BLE001
        print(f"  [{label}] action click failed: {str(e)[:160]}", flush=True)

    for _ in range(6):
        page.mouse.click(640, 360)
        time.sleep(0.5)

    # wait until the board is no longer initialising
    for _ in range(40):
        txt = settled(page)
        if "Initialising" not in txt and txt.strip():
            break
        time.sleep(0.5)
    time.sleep(6)

    out = OUT / f"{label}.png"
    page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1280, "height": 720})
    body = settled(page)[:60].strip().encode("ascii", "replace").decode("ascii")
    print(f"[shot] {out.name}  body='{body}'", flush=True)
    page.close()
    return errors


def main() -> None:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    with sync_playwright() as play:
        browser = play.chromium.launch()
        try:
            for label, story in JOBS:
                if only and only not in label:
                    continue
                errs = capture(browser, label, story)
                uniq = sorted(set(errs))
                print(f"[{label}] {len(uniq)} unique console error(s)", flush=True)
                for e in uniq[:10]:
                    print("    ", e[:200], flush=True)
        finally:
            browser.close()
    print("done.", flush=True)


if __name__ == "__main__":
    sys.exit(main())
