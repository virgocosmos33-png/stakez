"""Verify the Lady Mirror character renders WITH HEAD after the anchor fix.

Waits until the story body reads "Click action to start" (Vite recompiled and
the game booted; the intermediate "Initialising..." frame is blank), then
screenshots. Collects pageerror / console.error and any spine "key ... not
found". Also crops the right-side region where she stands for a close-up.

Run:  python tools/qa_verify_lady.py [story] [outname]
  default story  = mode-base-book--random
  default outname = fixed
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = sys.argv[1] if len(sys.argv) > 1 else "mode-base-book--random"
OUTNAME = sys.argv[2] if len(sys.argv) > 2 else "fixed"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "lady"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> int:
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page_errors: list[str] = []
        console_msgs: list[str] = []
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("console", lambda m: console_msgs.append(f"{m.type}: {m.text}"))
        page.goto(BASE + STORY, wait_until="commit", timeout=120000)

        ready = False
        deadline = time.time() + 90
        while time.time() < deadline:
            time.sleep(3)
            body = page.evaluate("document.body.innerText")
            if "Click action to start" in body:
                ready = True
                break
        # settle a couple idle cycles so the pose is mid-animation
        time.sleep(2.5)
        elapsed = int(90 - (deadline - time.time()))
        print(f"ready={ready} after ~{elapsed}s", flush=True)

        shot = OUT / f"{OUTNAME}.png"
        page.screenshot(path=str(shot))
        # right-side close-up (where she stands): x 560..1000, full height
        page.screenshot(path=str(OUT / f"{OUTNAME}_rightcrop.png"),
                        clip={"x": 560, "y": 0, "width": 440, "height": 720})
        print(f"[shot] {shot.name} + {OUTNAME}_rightcrop.png", flush=True)
        browser.close()

    spine_key_errs = [m for m in console_msgs if "not found" in m.lower() and "spine" in m.lower()]
    key_errs = [m for m in console_msgs if "is not found in loadedAssets" in m]
    console_errs = [m for m in console_msgs if m.startswith("error:")]

    print("\n=== pageerror ({}): ===".format(len(page_errors)), flush=True)
    for e in sorted(set(page_errors))[:15]:
        print("  ", e[:300])
    print("=== console.error ({}): ===".format(len(console_errs)), flush=True)
    for e in sorted(set(console_errs))[:15]:
        print("  ", e[:300])
    print("=== spine key-not-found ({}): ===".format(len(key_errs) + len(spine_key_errs)), flush=True)
    for e in sorted(set(key_errs + spine_key_errs))[:15]:
        print("  ", e[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
