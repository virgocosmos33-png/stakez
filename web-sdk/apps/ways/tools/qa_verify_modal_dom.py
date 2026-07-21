"""Verify the pay-table modal renders and uses the mono tokens (DOM-based).

Reads computed styles from the live modal so we don't depend on the modal being
composited above the pixi canvas in a screenshot.

Run: python tools/qa_verify_modal_dom.py  (Storybook on :6001)
"""

from __future__ import annotations

import json
import time

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="


def probe(page) -> dict:
    return page.evaluate(
        """() => {
        const out = {};
        const root = document.documentElement;
        const cs = getComputedStyle(root);
        out.token_bg = cs.getPropertyValue('--mono-bg').trim();
        out.token_line = cs.getPropertyValue('--mono-line').trim();
        out.token_hairline = cs.getPropertyValue('--mono-hairline').trim();
        out.shell = !!document.querySelector('.shell');
        out.popupWrap = !!document.querySelector('.ui-popup-standard-content-wrap');
        out.railBtns = document.querySelectorAll('.rail-btn').length;
        out.payCells = document.querySelectorAll('.pay-cell').length;
        out.anyPopup = document.querySelectorAll('[class*="popup" i], [class*="modal" i]').length;
        const dlg = document.querySelector('[role="dialog"]');
        out.dialog_present = !!dlg;
        if (dlg) {
            const d = getComputedStyle(dlg);
            out.dialog_color = d.color;
            out.dialog_font = d.fontFamily;
        }
        const h1 = document.querySelector('.head h1');
        if (h1) out.h1_color = getComputedStyle(h1).color;
        const railActive = document.querySelector('.rail-btn.active');
        if (railActive) {
            const r = getComputedStyle(railActive);
            out.rail_active_bg = r.backgroundColor;
            out.rail_active_color = r.color;
        }
        const cell = document.querySelector('.pay-cell');
        if (cell) {
            const c = getComputedStyle(cell);
            out.paycell_bg = c.backgroundColor;
            out.paycell_border = c.borderColor;
        }
        // any lingering gold?
        out.gold_hits = [...document.querySelectorAll('*')].filter((el) => {
            const s = getComputedStyle(el);
            return [s.color, s.backgroundColor, s.borderColor].some((v) =>
                v.includes('255, 193, 46') || v.includes('201, 154, 63'));
        }).length;
        return out;
    }"""
    )


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 860})
        page = ctx.new_page()
        page.goto(f"{BASE}components-game--pay-table", wait_until="commit", timeout=120000)
        time.sleep(22)
        print("before action:", json.dumps(probe(page)), flush=True)
        for _ in range(3):
            try:
                page.get_by_text("Action", exact=True).first.click(timeout=2500)
            except Exception:  # noqa: BLE001
                pass
            time.sleep(2)
            r = probe(page)
            if r.get("shell") or r.get("railBtns"):
                break
        time.sleep(2)
        print("after action:", json.dumps(probe(page), indent=2), flush=True)
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
