"""Diagnose why a story's asset loader stalls: poll loadingProgress / loaded and
dump console errors + any Vite error overlay text.

Usage: python tools/probe_scene_load.py <story-id>
"""
from __future__ import annotations

import sys
import time
from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="
story = sys.argv[1] if len(sys.argv) > 1 else "components-game--pre-spin"

with sync_playwright() as play:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": 1422, "height": 800})
    errs: list[str] = []
    page.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: errs.append(f"PAGEERROR: {e}"))
    page.goto(BASE + story, wait_until="commit", timeout=120000)

    for i in range(12):
        time.sleep(10)
        info = page.evaluate(
            """() => {
                const ov = document.querySelector('vite-error-overlay');
                const btn = document.querySelector('button.action');
                return {
                    overlay: ov ? (ov.shadowRoot?.textContent||'').slice(0,300) : null,
                    actionDisabled: btn ? btn.disabled : 'no-button',
                    bodyLen: document.body.innerText.length,
                };
            }"""
        )
        print(f"[{(i+1)*10}s] action_disabled={info['actionDisabled']} overlay={bool(info['overlay'])}", flush=True)
        if info["overlay"]:
            print("  OVERLAY:", info["overlay"], flush=True)
            break
        if info["actionDisabled"] is False:
            print("  -> Action ENABLED (assets loaded)", flush=True)
            break

    print("--- console (errors/warnings) ---", flush=True)
    for e in sorted(set(errs))[:20]:
        print("  ", e[:220], flush=True)
    browser.close()
    print("done.", flush=True)
