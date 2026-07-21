"""Boot a Storybook story, wait for the game canvas, screenshot it, and
report console errors. Used to smoke-check a fresh pull.

Run:  python tools/qa_boot_check.py [story-id]
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

STORY = sys.argv[1] if len(sys.argv) > 1 else "mode-base-book--madams-eye-base"
URL = f"http://localhost:6001/iframe.html?viewMode=story&id={STORY}"
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "boot"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"PAGEERROR: {e}"))
        page.goto(URL, wait_until="domcontentloaded", timeout=120000)

        canvas = page.locator("canvas")
        try:
            canvas.first.wait_for(state="visible", timeout=90000)
            print("[ok] canvas visible", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] no canvas: {exc}", flush=True)

        # click the story Action button (plays the book) if present
        try:
            btn = page.locator("button.action")
            btn.wait_for(state="visible", timeout=8000)
            for _ in range(30):
                if btn.is_enabled():
                    break
                time.sleep(1)
            btn.click(timeout=5000)
            print("[ok] action clicked", flush=True)
        except Exception:  # noqa: BLE001
            print("[info] no action button (static story)", flush=True)

        start = time.monotonic()
        for at, name in [(3, "idle"), (10, "playing"), (20, "settled")]:
            wait = at - (time.monotonic() - start)
            if wait > 0:
                time.sleep(wait)
            path = OUT / f"boot-{name}.png"
            page.screenshot(path=str(path))
            print(f"[shot] {path.name}", flush=True)

        browser.close()
        uniq = sorted(set(errors))
        print(f"[done] story={STORY} {len(uniq)} unique console error(s)")
        for e in uniq[:15]:
            print("   ", e[:220])


if __name__ == "__main__":
    main()
