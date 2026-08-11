"""Measure how long the board shows ZERO symbols during a spin (the "empty
outlined cells" window). Drives COMPONENTS/Game/spinCycle, which runs a real
preSpin -> reveal fall-in and stashes the measured empty duration (ms) on
window.__reelEmptyMs.

Run: python tools/qa_reel_empty_window.py [label]
"""
from __future__ import annotations
import sys
import time
from playwright.sync_api import sync_playwright

LABEL = sys.argv[1] if len(sys.argv) > 1 else "run"
STORY = "components-game--spin-cycle"
PORT = sys.argv[2] if len(sys.argv) > 2 else "6009"
BASE = f"http://localhost:{PORT}/iframe.html?viewMode=story&id={STORY}"


def one_run(page) -> int:
    page.evaluate("window.__reelEmptyMs = undefined")
    btn = page.locator("button.action")
    btn.wait_for(state="visible", timeout=30000)
    for _ in range(360):
        if btn.is_enabled():
            break
        time.sleep(1)
    btn.click(timeout=5000)
    # poll for the probe result
    for _ in range(240):
        val = page.evaluate("window.__reelEmptyMs")
        if val is not None:
            return int(val)
        time.sleep(0.1)
    return -999


def main() -> None:
    with sync_playwright() as play:
        browser = play.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader"])
        ctx = browser.new_context(viewport={"width": 1600, "height": 1000}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.locator("canvas").first.wait_for(state="visible", timeout=90000)
        results = []
        for i in range(3):
            ms = one_run(page)
            print(f"[{LABEL}] run {i + 1}: empty window = {ms} ms", flush=True)
            results.append(ms)
            time.sleep(1.5)
        good = [r for r in results if r >= 0]
        if good:
            print(f"[{LABEL}] median empty window = {sorted(good)[len(good) // 2]} ms", flush=True)
        browser.close()
        print("[done]", flush=True)


if __name__ == "__main__":
    main()
