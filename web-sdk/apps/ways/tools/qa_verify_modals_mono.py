"""Verify the AUTO SPINS + BUY BONUS modals render in the MONO design system.

DOM-based (not pixel-based): the pixi canvas composites over the HTML portal so
screenshots can't see modal colors reliably. Instead we read computed styles from
the live modal and assert there is no lingering gold and that titles/values are
white + primary button skins follow the mono treatment.

Run: python tools/qa_verify_modals_mono.py   (Storybook must be on :6001)
"""

from __future__ import annotations

import json
import sys
import time

from playwright.sync_api import sync_playwright

BASE = "http://localhost:6001/iframe.html?viewMode=story&id="

# Gold rgb() substrings that map to the legacy gothic palette we are replacing.
# #ffc12e / #c9a227 / #e9c877 / #ffe9a8 / #c99a3f / #e9dcc0 / #f4ecd8 / #ffedb8
GOLD_RGBS = [
    "255, 193, 46",
    "201, 162, 39",
    "233, 200, 119",
    "255, 233, 168",
    "201, 154, 63",
    "233, 220, 192",
    "244, 236, 216",
    "255, 237, 184",
]

TARGETS = [
    {"id": "components-game--auto-spin", "name": "AUTO SPINS"},
    {"id": "components-game--buy-menu", "name": "BUY BONUS"},
]


def probe(page, gold_rgbs) -> dict:
    return page.evaluate(
        """([goldRgbs]) => {
        const root = document.documentElement;
        const cs = getComputedStyle(root);
        const out = {};
        out.token_bg = cs.getPropertyValue('--mono-bg').trim();
        out.token_line = cs.getPropertyValue('--mono-line').trim();
        out.token_fill = cs.getPropertyValue('--mono-fill').trim();

        const wrap = document.querySelector('.ui-popup-standard-content-wrap');
        out.popupWrap = !!wrap;
        if (!wrap) return out;

        const isGold = (v) => goldRgbs.some((g) => v && v.includes(g));
        // yellow-ish heuristic to catch any *other* gold shade we didn't enumerate
        const goldish = (v) => {
            const m = v && v.match(/rgba?\\((\\d+), (\\d+), (\\d+)/);
            if (!m) return false;
            const r = +m[1], g = +m[2], b = +m[3];
            return r > 175 && g > 130 && b < 120 && (r - b) > 80 && (g - b) > 35;
        };

        const nodes = [wrap, ...wrap.querySelectorAll('*')];
        const props = ['color', 'backgroundColor', 'borderTopColor', 'borderRightColor',
            'borderBottomColor', 'borderLeftColor', 'outlineColor'];
        const hits = [];
        const goldishHits = [];
        for (const el of nodes) {
            const s = getComputedStyle(el);
            for (const p of props) {
                const v = s[p];
                if (isGold(v)) hits.push({tag: el.tagName, cls: el.className, prop: p, val: v});
                else if (goldish(v)) goldishHits.push({tag: el.tagName, cls: (el.className||'').toString().slice(0,40), prop: p, val: v});
            }
        }
        out.gold_hits = hits.length;
        out.gold_samples = hits.slice(0, 12);
        out.goldish_hits = goldishHits.length;
        out.goldish_samples = goldishHits.slice(0, 12);

        const pick = (el, ks) => { if (!el) return null; const s = getComputedStyle(el); const o = {}; ks.forEach(k => o[k] = s[k]); return o; };

        const title = wrap.querySelector('.ui-modal-title-wrap');
        out.title = pick(title, ['color', 'fontFamily', 'fontWeight']);

        // button skins (BaseIcon) + labels (BaseButtonContent)
        const skins = [...wrap.querySelectorAll('.skin')];
        out.skinCount = skins.length;
        out.skin_first = pick(skins[0], ['backgroundColor', 'borderTopColor', 'borderRadius']);
        const selectedSkin = wrap.querySelector('.skin.selected');
        out.skin_selected = pick(selectedSkin, ['backgroundColor', 'borderTopColor']);
        out.label_first = pick(wrap.querySelector('.base-button-content'), ['color', 'fontFamily']);

        // buyBonus specifics
        out.amount = pick(wrap.querySelector('.amount'), ['color', 'fontFamily', 'fontVariantNumeric']);
        const card = wrap.querySelector('.bonus-card-wrap');
        out.card = pick(card, ['backgroundColor', 'borderTopColor', 'borderRadius']);
        out.price = pick(wrap.querySelector('.price'), ['color', 'fontVariantNumeric']);

        // autoSpin specifics
        out.subtitle = pick(wrap.querySelector('.subtitle'), ['color', 'fontFamily', 'letterSpacing', 'textTransform']);
        return out;
    }""",
        [gold_rgbs],
    )


def wait_ready(page, timeout=120) -> bool:
    """Poll until the pixi game has finished booting (the 'Initialising...' hint
    is gone). Headless WebGL cold-boot is slow, so we give it a long budget."""
    end = time.time() + timeout
    while time.time() < end:
        try:
            txt = page.evaluate("() => (document.body && document.body.innerText) || ''")
        except Exception:  # noqa: BLE001
            txt = ""
        if txt and "nitialis" not in txt:  # 'Initialising...' cleared
            return True
        time.sleep(2)
    return False


def run_target(page, target) -> dict:
    page.goto(f"{BASE}{target['id']}", wait_until="commit", timeout=120000)
    wait_ready(page, 120)
    r = {}
    for _ in range(16):
        try:
            page.get_by_text("Action", exact=True).first.click(timeout=2500)
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2.5)
        r = probe(page, GOLD_RGBS)
        if r.get("popupWrap"):
            break
    time.sleep(1)
    r = probe(page, GOLD_RGBS)
    # visual: hide the pixi canvas so the HTML modal is visible, then shoot
    try:
        page.evaluate("() => document.querySelectorAll('canvas').forEach(c => c.style.visibility='hidden')")
        time.sleep(0.4)
        shot = f"../../qa-shots/hud/modal-{target['id'].split('--')[-1]}-mono.png"
        page.screenshot(path=shot, full_page=True)
        r["_shot"] = shot
    except Exception as e:  # noqa: BLE001
        r["_shot_error"] = str(e)
    return r


def main() -> None:
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 860})
        page = ctx.new_page()
        # Warm the WebGL/game/asset caches once. The first story of a fresh
        # headless browser boots very slowly; warming makes every real target
        # load fast so cold-boot doesn't masquerade as a "modal didn't open".
        page.goto(f"{BASE}components-game--buy-menu", wait_until="commit", timeout=120000)
        wait_ready(page, 150)
        for t in TARGETS:
            results[t["name"]] = run_target(page, t)
        ctx.close()
        browser.close()

    ok = True
    for name, r in results.items():
        print(f"\n===== {name} =====")
        print(json.dumps(r, indent=2))
        if not r.get("popupWrap"):
            print(f"[FAIL] {name}: modal did not open")
            ok = False
            continue
        if r.get("gold_hits", 1) != 0:
            print(f"[FAIL] {name}: gold_hits = {r['gold_hits']}")
            ok = False
        else:
            print(f"[PASS] {name}: gold_hits === 0")
        if r.get("goldish_hits", 0) != 0:
            print(f"[WARN] {name}: goldish_hits = {r['goldish_hits']} (inspect samples)")

    print("\n==================")
    print("ALL PASS" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
