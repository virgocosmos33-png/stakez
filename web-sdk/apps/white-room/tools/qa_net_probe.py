"""Log the exact URLs of any failed network requests on a Storybook story,
so we can see what is 403/404ing rather than guessing.

Run:  python tools/qa_net_probe.py [story-id]
"""

from __future__ import annotations

import sys
import time

from playwright.sync_api import sync_playwright

STORY = sys.argv[1] if len(sys.argv) > 1 else "mode-base-book--madams-eye-base"
URL = f"http://localhost:6001/iframe.html?viewMode=story&id={STORY}"


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        failed: list[str] = []

        def on_response(resp):
            if resp.status >= 400:
                failed.append(f"{resp.status}  {resp.url}")

        page.on("response", on_response)
        page.on("requestfailed", lambda r: failed.append(f"FAIL  {r.url}  ({r.failure})"))
        page.goto(URL, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(18000)
        browser.close()

        uniq = sorted(set(failed))
        print(f"[done] {len(uniq)} failed request(s):")
        for f in uniq:
            print("   ", f[:300])


if __name__ == "__main__":
    main()
