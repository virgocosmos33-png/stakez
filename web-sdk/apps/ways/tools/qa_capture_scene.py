"""Capture the idle Lady-Mirror scene (single cover-scaled background + right-side
character) across several DISTINCT aspect ratios to verify:

  1) the ambient background scales as one unit (no drifting/misaligned FX),
  2) the reels stay centered + unobstructed,
  3) Lady Mirror sits on the right without covering symbols (hidden where too tight).

Loads COMPONENTS/<Game> preSpin (skips loading screen, shows the resting board),
clicks Action, dismisses the one-shot intro, then screenshots the full viewport.
Run while Storybook is up on :6001.  ->  web-sdk/qa-shots/scene/
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "components-game--pre-spin"
WIN_STORY = "components-game--win-ways-layer"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "scene"
OUT.mkdir(parents=True, exist_ok=True)

# distinct aspect ratios: wide landscape, ultra-wide, narrow portrait, tall
# portrait, near-square (the exact set the task asks to verify)
VIEWPORTS = [
    ("land-1600x900", 1600, 900),
    ("wide-1920x800", 1920, 800),
    ("port-540x960", 540, 960),
    ("port-800x1400", 800, 1400),
    ("square-1200x1200", 1200, 1200),
]


def capture(browser, label: str, w: int, h: int, do_action: bool = True,
            story: str = STORY) -> list[str]:
    page = browser.new_page(viewport={"width": w, "height": h})
    errors: list[str] = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(BASE + story, wait_until="commit", timeout=120000)

    if do_action:
        # .click() auto-waits until the Action button is ENABLED (assets loaded),
        # then preSpin() empties the board (shows the frame window, not symbols)
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=180000)
        except Exception as e:  # noqa: BLE001
            print(f"  [{label}] action click failed: {str(e)[:160]}", flush=True)
    else:
        # no action: the board rests on INITIAL_BOARD so SYMBOLS are visible,
        # proving the scene/character never cover them. Assets still auto-load.
        time.sleep(30)

    # dismiss the one-shot "enter the mirror" intro (advances on tap)
    for _ in range(5):
        page.mouse.click(w * 0.5, h * 0.5)
        time.sleep(0.5)

    time.sleep(5)  # let the scene + character settle
    out = OUT / f"{label}.png"
    page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h}, timeout=90000)
    print(f"[shot] {out.name}", flush=True)
    page.close()
    return errors


def main() -> None:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    with sync_playwright() as play:
        browser = play.chromium.launch()
        try:
            if only == "fix":
                # WIN plaque (normal win) + press-to-continue, big-win takeover,
                # and persistent WAYS in the base game — desktop + portrait
                jobs = [
                    ("winplaque-desktop", 1422, 800, WIN_STORY, True),
                    ("winplaque-portrait", 800, 1400, WIN_STORY, True),
                    ("bigwin-desktop", 1422, 800, "components-game--big-win", True),
                    ("bigwin-portrait", 800, 1400, "components-game--big-win", True),
                    ("ways-base-desktop", 1422, 800, "components-game--pre-spin", False),
                    ("ways-base-portrait", 800, 1400, "components-game--pre-spin", False),
                ]
                for label, w, h, st, act in jobs:
                    errs = capture(browser, label, w, h, do_action=act, story=st)
                    print(f"[{label}] {len(sorted(set(errs)))} unique console error(s)", flush=True)
            elif only == "char":
                # base-idle vs bonus-activated character, desktop + portrait
                jobs = [
                    ("char-base-desktop", 1422, 800, "components-game--scene-base"),
                    ("char-bonus-desktop", 1422, 800, "components-game--scene-bonus"),
                    ("char-base-portrait", 800, 1400, "components-game--scene-base"),
                    ("char-bonus-portrait", 800, 1400, "components-game--scene-bonus"),
                ]
                for label, w, h, st in jobs:
                    errs = capture(browser, label, w, h, do_action=True, story=st)
                    print(f"[{label}] {len(sorted(set(errs)))} unique console error(s)", flush=True)
            elif only == "win":
                # WIN + WAYS plaques on the left rail, on top of all ambient FX
                for label, w, h in [("winways-left-desktop", 1422, 800),
                                    ("winways-left-landscape", 1600, 900),
                                    ("winways-left-portrait", 540, 960),
                                    ("winways-left-tall", 800, 1400),
                                    ("winways-left-square", 1200, 1200)]:
                    errs = capture(browser, label, w, h, do_action=True, story=WIN_STORY)
                    uniq = sorted(set(errs))
                    print(f"[{label}] {len(uniq)} unique console error(s)", flush=True)
                    for e in uniq[:6]:
                        print("    ", e[:200], flush=True)
            elif only == "rest":
                # resting boards (symbols visible) to prove they are unobstructed
                for label, w, h in [("land-1600x900-rest", 1600, 900),
                                    ("square-1200x1200-rest", 1200, 1200)]:
                    errs = capture(browser, label, w, h, do_action=False)
                    print(f"[{label}] {len(sorted(set(errs)))} unique console error(s)", flush=True)
            else:
                for label, w, h in VIEWPORTS:
                    if only and only not in label:
                        continue
                    errs = capture(browser, label, w, h)
                    uniq = sorted(set(errs))
                    print(f"[{label}] {len(uniq)} unique console error(s)", flush=True)
                    for e in uniq[:6]:
                        print("    ", e[:200], flush=True)
        finally:
            browser.close()
    print("done.", flush=True)


if __name__ == "__main__":
    sys.exit(main())
