"""Capture the resized SPIN + bonus-buy coins in the bottom HUD bar.

Run: python tools/qa_buttons_shots.py

Storybook must be up on :6001. Uses the preSpin story (board + HUD visible).
The HUD renders without needing the story action, so we just wait for the app to
leave the "Initialising" state, optionally click the action button if present,
then screenshot. Prints progress so a hang is diagnosable. os._exit(0) at the end
avoids the Windows Playwright teardown hang.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
STORY = "components-game--pre-spin"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "hud"
OUT.mkdir(parents=True, exist_ok=True)

SHOTS = [
    ("buttons_portrait", 720, 1280),
]


def try_click_action(page) -> bool:
    btn = page.locator("button.action")
    for _ in range(20):
        try:
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=2000)
                return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.5)
    return False


def main() -> None:
    with sync_playwright() as p:
        for name, w, h in SHOTS:
            browser = p.chromium.launch()
            ctx = browser.new_context(
                viewport={"width": w, "height": h}, device_scale_factor=1
            )
            page = ctx.new_page()
            perr: list[str] = []
            page.on("pageerror", lambda e: perr.append(str(e)))
            page.goto(f"{BASE}{STORY}", wait_until="commit", timeout=60000)
            print(f"[goto] {name}", flush=True)
            # wait for the app to leave the blank "Initialising" frame
            for _ in range(75):
                time.sleep(1)
                try:
                    body = page.evaluate("document.body.innerText") or ""
                except Exception:  # noqa: BLE001
                    body = ""
                if "Initialising" not in body:
                    break
            clicked = try_click_action(page)
            time.sleep(6)  # settle
            out = OUT / f"{name}.png"
            try:
                page.screenshot(
                    path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h}
                )
                print(
                    f"[shot] {out} clicked={clicked} pageerrors={len(perr)}", flush=True
                )
            except Exception as e:  # noqa: BLE001
                print(f"[fail] {name}: {str(e)[:160]}", flush=True)
            for e in sorted(set(perr))[:5]:
                print("   ERR:", e[:200], flush=True)
            browser.close()
        print("[done]", flush=True)
    os._exit(0)


if __name__ == "__main__":
    main()
