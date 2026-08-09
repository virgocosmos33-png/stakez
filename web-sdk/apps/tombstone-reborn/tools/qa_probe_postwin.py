"""Probe whether the looping symbol states actually animate (esp. postWin ripple).

Loads the Components/<Symbol> "symbols" contact sheet (every symbol x every
state, loop=true) and takes a burst of full screenshots ~1.2s apart, then diffs
consecutive frames so we can see which state columns move.

Run:  python tools/qa_probe_postwin.py
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
OUT = Path(__file__).resolve().parents[3] / "qa-shots" / "postwin"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as play:
    browser = play.chromium.launch()
    try:
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(BASE + "components-symbol--symbols", wait_until="commit", timeout=120000)
        time.sleep(25)
        paths = []
        for i in range(4):
            p = OUT / f"sheet_{i}.png"
            page.screenshot(path=str(p), timeout=60000)
            paths.append(p)
            print(f"shot {i}", flush=True)
            time.sleep(1.2)
    finally:
        browser.close()

    for i in range(len(paths) - 1):
        a = Image.open(paths[i]).convert("RGB")
        b = Image.open(paths[i + 1]).convert("RGB")
        d = np.asarray(ImageChops.difference(a, b))
        mask = d.max(axis=2) > 12
        print(f"frame {i}->{i+1}: max={d.max()} mean={d.mean():.4f} changed_px={int(mask.sum())}", flush=True)
        # column-band of change: report x ranges with movement
        cols = np.where(mask.any(axis=0))[0]
        if cols.size:
            print(f"  x-range of motion: {cols.min()}..{cols.max()}", flush=True)
    print("done", flush=True)
