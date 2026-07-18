"""CDP screencast of the mirror-burst story: streams frames as the page
renders them (fast enough to catch the cut-blade sweep).

Run:  python tools/qa_screencast.py
"""

from __future__ import annotations

import asyncio
import base64
import time
from pathlib import Path

from playwright.async_api import async_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "frame3" / "cast"
OUT.mkdir(parents=True, exist_ok=True)


async def main() -> None:
    async with async_playwright() as play:
        browser = await play.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        await page.goto(
            BASE + "mode-bonus-book--random", wait_until="domcontentloaded"
        )
        await asyncio.sleep(16)

        client = await page.context.new_cdp_session(page)
        t0 = time.monotonic()
        saved = 0

        def on_frame(params):
            nonlocal saved
            ms = int((time.monotonic() - t0) * 1000)
            (OUT / f"c{saved:04d}_{ms}.jpg").write_bytes(base64.b64decode(params["data"]))
            saved += 1
            asyncio.get_event_loop().create_task(
                client.send("Page.screencastFrameAck", {"sessionId": params["sessionId"]})
            )

        client.on("Page.screencastFrame", on_frame)

        await page.get_by_text("Action", exact=True).first.click(timeout=30000)
        t0 = time.monotonic()
        print("action clicked", flush=True)

        await client.send(
            "Page.startScreencast",
            {
                "format": "jpeg",
                "quality": 65,
                "maxWidth": 1280,
                "maxHeight": 720,
                "everyNthFrame": 1,
            },
        )
        await asyncio.sleep(24)
        await client.send("Page.stopScreencast")
        await browser.close()
        print(f"{saved} frames", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
