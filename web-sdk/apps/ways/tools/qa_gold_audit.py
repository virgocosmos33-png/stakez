"""Authoritative gold audit for the restyled HTML modals.

Opens each modal *patiently* (WebGL cold-boot is very slow headless) and scans the
whole modal subtree's computed styles for any lingering gold — both an explicit
list of the legacy gothic hexes and a yellow-ish heuristic to catch anything we
didn't enumerate. Prints gold_hits per modal; 0 across the board == pass.

Run from web-sdk/apps/ways  (Storybook :6001).
"""

from __future__ import annotations

import json
import sys
import time

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="

GOLD_RGBS = [
    "255, 193, 46",   # #ffc12e accent
    "201, 162, 39",   # #c9a227 ds-gold
    "233, 200, 119",  # #e9c877
    "255, 233, 168",  # #ffe9a8
    "201, 154, 63",   # #c99a3f bevel
    "233, 220, 192",  # #e9dcc0
    "244, 236, 216",  # #f4ecd8 bone
    "255, 237, 184",  # #ffedb8
    "243, 230, 200",  # #f3e6c8 ds-bone
    "184, 168, 136",  # #b8a888 ds-bone-dim
]

# story id -> modal root selectors present for that modal
TARGETS = [
    ("BUY BONUS", "components-game--buy-menu", ".ui-popup-standard-content-wrap, .sheet"),
    ("BUY BONUS (greyed)", "components-game--buy-menu-greyed", ".ui-popup-standard-content-wrap, .sheet"),
    ("PAY TABLE", "components-game--pay-table", ".shell"),
]


def wait_ready(page, timeout=160) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            txt = page.evaluate("() => (document.body && document.body.innerText) || ''")
        except Exception:  # noqa: BLE001
            txt = ""
        if txt and "nitialis" not in txt:
            return True
        time.sleep(2)
    return False


def open_modal(page, selector, tries=40) -> bool:
    for _ in range(tries):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=2500)
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2.0)
        if page.locator(selector).count() > 0:
            return True
    return False


def probe(page, selector, gold_rgbs) -> dict:
    return page.evaluate(
        """([selector, goldRgbs]) => {
        const root = document.documentElement;
        const cs = getComputedStyle(root);
        const out = {
            token_bg: cs.getPropertyValue('--mono-bg').trim(),
            token_hairline: cs.getPropertyValue('--mono-hairline').trim(),
            token_line: cs.getPropertyValue('--mono-line').trim(),
            token_fill: cs.getPropertyValue('--mono-fill').trim(),
            token_fg_dim: cs.getPropertyValue('--mono-fg-dim').trim(),
        };
        const wrap = document.querySelector(selector);
        out.present = !!wrap;
        if (!wrap) return out;

        const isGold = (v) => goldRgbs.some((g) => v && v.includes(g));
        const goldish = (v) => {
            const m = v && v.match(/rgba?\\((\\d+), (\\d+), (\\d+)/);
            if (!m) return false;
            const r = +m[1], g = +m[2], b = +m[3];
            return r > 175 && g > 130 && b < 120 && (r - b) > 80 && (g - b) > 35;
        };
        const props = ['color', 'backgroundColor', 'borderTopColor', 'borderRightColor',
            'borderBottomColor', 'borderLeftColor', 'outlineColor'];
        const nodes = [wrap, ...wrap.querySelectorAll('*')];
        const hits = [], goldishHits = [];
        for (const el of nodes) {
            const s = getComputedStyle(el);
            for (const p of props) {
                const v = s[p];
                if (isGold(v)) hits.push({cls: (el.className||'').toString().slice(0,30), prop: p, val: v});
                else if (goldish(v)) goldishHits.push({cls: (el.className||'').toString().slice(0,30), prop: p, val: v});
            }
        }
        out.node_count = nodes.length;
        out.gold_hits = hits.length;
        out.gold_samples = hits.slice(0, 10);
        out.goldish_hits = goldishHits.length;
        out.goldish_samples = goldishHits.slice(0, 10);
        return out;
    }""",
        [selector, gold_rgbs],
    )


def main() -> None:
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 860})
        page = ctx.new_page()
        page.goto(f"{BASE}components-game--buy-menu", wait_until="commit", timeout=120000)
        wait_ready(page, 160)
        for name, story, sel in TARGETS:
            page.goto(f"{BASE}{story}", wait_until="commit", timeout=120000)
            wait_ready(page, 150)
            opened = open_modal(page, sel)
            time.sleep(1.0)
            r = probe(page, sel, GOLD_RGBS)
            r["_opened"] = opened
            results[name] = r
        ctx.close()
        browser.close()

    ok = True
    for name, r in results.items():
        print(f"\n===== {name} =====")
        print(json.dumps(r, indent=2))
        if not r.get("present"):
            print(f"[FAIL] {name}: modal not present")
            ok = False
            continue
        if r.get("gold_hits", 1) != 0:
            print(f"[FAIL] {name}: gold_hits = {r['gold_hits']}")
            ok = False
        else:
            print(f"[PASS] {name}: gold_hits === 0 (scanned {r.get('node_count')} nodes)")
        if r.get("goldish_hits", 0) != 0:
            print(f"[WARN] {name}: goldish_hits = {r['goldish_hits']}")

    print("\n==================")
    print("ALL PASS" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
