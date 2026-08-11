"""Live verification of the western type system (src/game/typography.ts).

Storybook must already be serving this app (default :6009).

Run: python tools/qa_typography_shots.py [port] [story]

Three checks, all against the real browser that renders the game:

1. FACE LOADED — document.fonts.check() for every role at its shipped weight.
2. NO SILENT FALLBACK — the killer failure mode. Pixi rasterizes text to a
   texture and never re-rasterizes, so a face that arrives late (or 404s) leaves
   Arial baked into the HUD with no error anywhere. Detected by measuring a
   probe string twice, once against the role's family and once against the
   fallback tail of that same stack: identical advance widths mean the vendored
   face never won.
3. ESTIMATOR AGREEMENT — the HUD sizes its wells from estimateTextWidth() before
   any Text node exists. That estimate is summed from advances baked out of the
   woff2 files, so it must agree with what the browser will actually lay out.
   Compared here against canvas measureText, which is the same measurement Pixi's
   CanvasTextMetrics performs. Stress strings cover the cases that clip in
   production: nine-digit ways counts and long currency amounts.

Then screenshots at four canvas sizes, plus any console error the page logged.

GOTCHA: a `storybook dev` server treats packages/pixi-svelte/dist as an immutable
dependency and caches its transform for the life of the process, so after
rebuilding that package (`pnpm --filter pixi-svelte build`) check 2 will keep
failing against a server that predates the rebuild. Restart Storybook first.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


# The stress set prints currency symbols; a default Windows console is cp1252 and
# would raise mid-report rather than fail the check it was running.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

APP = Path(__file__).resolve().parents[1]
OUT = APP / "qa-shots" / "typography"
OUT.mkdir(parents=True, exist_ok=True)

METRICS_TS = APP / "src" / "game" / "typographyMetrics.generated.ts"

# role -> (full stack as shipped, fallback-only tail, weight)
ROLES = {
    "display": ('"Rye", "Bookman Old Style", Georgia, serif', '"Bookman Old Style", Georgia, serif', "400"),
    "label": ('"Oswald", "Arial Narrow", "Segoe UI", Arial, sans-serif', '"Arial Narrow", "Segoe UI", Arial, sans-serif', "600"),
    "value": ('"Archivo Narrow", "Arial Narrow", "Segoe UI", Arial, sans-serif', '"Arial Narrow", "Segoe UI", Arial, sans-serif', "700"),
    "accent": ('"Special Elite", "Courier New", monospace', '"Courier New", monospace', "400"),
}

# The strings that actually break layouts: a nine-digit ways count, a long
# currency amount, and the widest HUD captions.
STRESS = {
    "label": ["WAYS", "WIN", "FREE SPINS", "BALANCE", "BET", "TOTAL BET"],
    "value": ["123456789", "1,234,567,890", "$1,234,567.89", "₩1,234,567,890", "888,888,888", "x90", "0.00"],
    "display": ["MEGA WIN", "TOMBSTONE"],
    "accent": ["HER SIDE SPINS"],
}

VIEWPORTS = [
    ("desktop", 1600, 900),
    ("landscape", 900, 440),
    ("portrait", 560, 980),
    ("tablet", 860, 820),
]

PROBE = "AVAILABLE BALANCE 1234567890"

# --- the estimator, mirrored from typography.ts -----------------------------


ROLE_HEADER = re.compile(r"^\t(display|label|value|accent): \{$", re.MULTILINE)
# keys are quoted with whichever quote character the glyph itself is not
PAIR = re.compile(r"""(?:'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)")\s*:\s*([\d.]+)""")
FALLBACK = re.compile(r"fallback:\s*([\d.]+)")


def load_metrics() -> dict:
    """Parse the generated advance table straight out of the TS module.

    Read rather than reimplemented so this check can never drift from what the
    app ships: if the table is regenerated, this picks the new numbers up. Hand
    parsed rather than via json because the generated literal uses TS quoting.
    """
    src = METRICS_TS.read_text(encoding="utf-8")
    bounds = [(m.group(1), m.end()) for m in ROLE_HEADER.finditer(src)]
    if len(bounds) != 4:
        raise SystemExit(f"expected 4 roles in {METRICS_TS.name}, found {len(bounds)}")
    out: dict = {}
    for i, (role, start) in enumerate(bounds):
        end = bounds[i + 1][1] if i + 1 < len(bounds) else len(src)
        block = src[start:end]
        advance = {}
        for m in PAIR.finditer(block):
            key = m.group(1) if m.group(1) is not None else m.group(2)
            advance[key.encode().decode("unicode_escape")] = float(m.group(3))
        out[role] = {"fallback": float(FALLBACK.search(block).group(1)), "advance": advance}
    return out


def estimate(metrics: dict, role: str, text: str, size: float, tracking: float = 0.0) -> float:
    m = metrics[role]
    ratio = sum(m["advance"].get(ch, m["fallback"]) for ch in text)
    return ratio * size + tracking * len(text)


# --- browser-side measurement ----------------------------------------------

MEASURE_JS = """
async (args) => {
  await document.fonts.ready;
  const c = document.createElement('canvas').getContext('2d');
  const out = {};
  for (const [role, spec] of Object.entries(args.roles)) {
    const [stack, fallback, weight] = spec;
    c.font = `${weight} 100px ${stack}`;
    const real = c.measureText(args.probe).width;
    c.font = `${weight} 100px ${fallback}`;
    const fb = c.measureText(args.probe).width;
    const widths = {};
    for (const s of (args.stress[role] || [])) {
      c.font = `${weight} 100px ${stack}`;
      widths[s] = c.measureText(s).width;
    }
    out[role] = {
      loaded: document.fonts.check(`${weight} 16px ${stack.split(',')[0]}`),
      probeReal: real,
      probeFallback: fb,
      widths,
    };
  }
  out._families = [...document.fonts].map((f) => `${f.family} ${f.weight} ${f.status}`);
  // Did the app's own preload pull in the latin-ext subset? Checked, never
  // forced: if this is false the exotic currency symbols will rasterize once
  // with a fallback glyph and PIXI will cache that forever.
  out._extLoaded = document.fonts.check('700 16px "Archivo Narrow"', '\\u20a9');
  return out;
}
"""


def main() -> None:
    port = sys.argv[1] if len(sys.argv) > 1 else "6009"
    story = sys.argv[2] if len(sys.argv) > 2 else "mode-base-book--dead-spin"
    base = f"http://localhost:{port}/iframe.html?viewMode=story&id={story}"

    metrics = load_metrics()
    failures: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        measured = None
        for vname, w, h in VIEWPORTS:
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
            page = ctx.new_page()
            errors: list[str] = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
            page.goto(base, wait_until="commit", timeout=120000)
            # Cold Vite transforms of this app can take minutes, and several
            # Storybook instances usually share the machine; wait on the canvas
            # rather than a fixed sleep or the shots come back empty.
            page.wait_for_selector("canvas", timeout=600000)
            time.sleep(4)
            # fund + run the story action so the HUD shows real amounts
            try:
                btn = page.locator("button.action")
                for _ in range(40):
                    if btn.count() and btn.first.is_enabled():
                        btn.first.click(timeout=2000)
                        break
                    time.sleep(1)
            except Exception:  # noqa: BLE001
                pass
            time.sleep(6)

            if measured is None:
                measured = page.evaluate(MEASURE_JS, {"roles": ROLES, "stress": STRESS, "probe": PROBE})
                if not measured.pop("_extLoaded"):
                    failures.append(
                        "latin-ext subset of the value face was not preloaded: "
                        "amounts in rupee / ruble / peso / won currencies would "
                        "rasterize with a fallback glyph"
                    )

            out = OUT / f"type-{vname}.png"
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h})
            print(f"[shot] {out}", flush=True)
            for e in errors:
                low = e.lower()
                if "font" in low or "woff" in low or "404" in low:
                    failures.append(f"{vname} console: {e}")
                    print(f"[console] {vname}: {e}", flush=True)
            ctx.close()

    print("\n=== loaded font faces ===", flush=True)
    for f in measured.pop("_families"):
        print(f"  {f}", flush=True)

    print("\n=== role checks ===", flush=True)
    for role, data in measured.items():
        same = abs(data["probeReal"] - data["probeFallback"]) < 0.5
        status = "OK  " if data["loaded"] and not same else "FAIL"
        if not data["loaded"]:
            failures.append(f"{role}: document.fonts.check() false")
        if same:
            failures.append(f"{role}: renders identically to its fallback -> face never loaded")
        print(
            f"  [{status}] {role:8s} loaded={data['loaded']} "
            f"probe={data['probeReal']:.1f}px fallback={data['probeFallback']:.1f}px",
            flush=True,
        )

    print("\n=== estimator vs browser layout (100px) ===", flush=True)
    for role, strings in STRESS.items():
        for s in strings:
            actual = measured[role]["widths"].get(s)
            if actual is None:
                continue
            est = estimate(metrics, role, s, 100.0)
            drift = (est - actual) / actual * 100 if actual else 0.0
            # A wide estimate only costs a little empty space; a short one clips.
            bad = drift < -1.0 or drift > 12.0
            if bad:
                failures.append(f"{role} '{s}': estimate off by {drift:+.1f}%")
            print(
                f"  [{'FAIL' if bad else 'OK  '}] {role:8s} {s!r:24s} "
                f"est={est:8.1f} actual={actual:8.1f} ({drift:+.1f}%)",
                flush=True,
            )

    print("\n=== result ===", flush=True)
    if failures:
        for f in failures:
            print(f"  FAIL {f}", flush=True)
    else:
        print("  all typography checks passed", flush=True)
    os._exit(1 if failures else 0)


if __name__ == "__main__":
    main()
