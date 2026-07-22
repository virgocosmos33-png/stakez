"""Capture the full game at mobile/tablet viewports to sanity-check responsive
fit: HUD row spans the frame, nothing clips/overflows, and the floating Lady
only shows where there's side room.

Run while Storybook is up on :6001.  ->  web-sdk/qa-shots/mobile/
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "mobile"
OUT.mkdir(parents=True, exist_ok=True)

STORY = "components-game--scene-base"

# (label, width, height)
VIEWPORTS = [
    ("portrait_390x844", 390, 844),
    ("portrait_360x780", 360, 780),
    ("landscape_844x390", 844, 390),
    ("tablet_820x1180", 820, 1180),
    ("tablet_land_1180x820", 1180, 820),
]


def settled(page) -> str:
    try:
        return page.evaluate("() => document.body.innerText.slice(0, 400)")
    except Exception:
        return ""


def capture(browser, label: str, w: int, h: int) -> list[str]:
    page = browser.new_page(viewport={"width": w, "height": h})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append("PAGEERROR: " + str(e)))
    page.goto(BASE + STORY, wait_until="commit", timeout=120000)

    try:
        page.get_by_text("Action", exact=True).first.click(timeout=180000)
    except Exception as e:  # noqa: BLE001
        print(f"  [{label}] action click failed: {str(e)[:160]}", flush=True)

    for _ in range(6):
        page.mouse.click(w // 2, h // 2)
        time.sleep(0.4)

    for _ in range(40):
        txt = settled(page)
        if "Initialising" not in txt and txt.strip():
            break
        time.sleep(0.5)
    time.sleep(5)

    out = OUT / f"{label}.png"
    page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h})
    print(f"[shot] {out.name}", flush=True)
    page.close()
    return errors


def main() -> None:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    with sync_playwright() as play:
        browser = play.chromium.launch()
        try:
            for label, w, h in VIEWPORTS:
                if only and only not in label:
                    continue
                errs = capture(browser, label, w, h)
                uniq = sorted(set(errs))
                print(f"[{label}] {len(uniq)} unique console error(s)", flush=True)
                for e in uniq[:6]:
                    print("    ", e[:160], flush=True)
        finally:
            browser.close()
    print("done.", flush=True)


if __name__ == "__main__":
    sys.exit(main())
