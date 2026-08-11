"""Verify the vendored western webfonts under static/assets/fonts/webfont/.

The typography system (src/game/typography.ts + typography.css) renders HUD
labels, currency values and hero titles through PIXI.Text, which needs the real
browser face. This checks each woff2 actually carries the glyphs those surfaces
demand, and that the value face's digits are equal-width so a win count-up does
not jitter (PIXI.TextStyle has no font-feature-settings, so tabular figures have
to be the font's default).

Run:  python tools/qa_verify_webfonts.py
Exit code 1 if any required glyph is missing or the value face is proportional.
"""

from __future__ import annotations

import os
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
FONT_DIR = os.path.join(APP, "static", "assets", "fonts", "webfont")

DIGITS = "0123456789"
CAPS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PUNCT = ",.:/+-\u00d7x%"
# currency symbols the amount surfaces can emit, matching the set the bitmap
# face already ships (tools/make_tombstone_font.py)
CURRENCY_CORE = "$\u00a3\u00a5\u20ac"
CURRENCY_EXT = "\u20b9\u20bd\u20b1\u20a9"

# Only the VALUE role ever renders a currency amount or a count-up, so only it
# owes full currency coverage and equal-width digits. The display and accent
# roles are latin-only hero faces; typography.ts documents that amounts must
# never be handed to them.
#
# file -> (required glyphs, must have equal-width digits, render weight)
CHECKS = {
	"rye-400-latin.woff2": (CAPS + DIGITS + "$" + PUNCT, False, None),
	"oswald-var-latin.woff2": (CAPS + DIGITS + CURRENCY_CORE + PUNCT, False, 600),
	"oswald-var-latin-ext.woff2": (CURRENCY_EXT, False, 600),
	"archivo-narrow-var-latin.woff2": (CAPS + DIGITS + CURRENCY_CORE + PUNCT, True, 700),
	"archivo-narrow-var-latin-ext.woff2": (CURRENCY_EXT, False, 700),
	"special-elite-400-latin.woff2": (CAPS + DIGITS + PUNCT, False, None),
}


def codepoints(font: TTFont) -> set[int]:
	out: set[int] = set()
	for table in font["cmap"].tables:
		out |= set(table.cmap.keys())
	return out


def best_cmap(font: TTFont) -> dict[int, str]:
	out: dict[int, str] = {}
	for table in font["cmap"].tables:
		out.update(table.cmap)
	return out


def main() -> int:
	failures: list[str] = []
	for name, (required, tabular, weight) in CHECKS.items():
		path = os.path.join(FONT_DIR, name)
		if not os.path.isfile(path):
			failures.append(f"{name}: MISSING FILE")
			continue
		font = TTFont(path)
		# a variable face can change digit widths per weight, so check the
		# instance the role actually renders at
		if weight is not None and "fvar" in font:
			font = instantiateVariableFont(font, {"wght": weight}, inplace=False)
		covered = codepoints(font)
		missing = [c for c in required if ord(c) not in covered]
		status = "ok" if not missing else "MISSING " + " ".join(f"U+{ord(c):04X}" for c in missing)
		if missing:
			failures.append(f"{name}: {status}")

		note = ""
		if tabular:
			cmap = best_cmap(font)
			widths = {font["hmtx"][cmap[ord(d)]][0] for d in DIGITS if ord(d) in cmap}
			if len(widths) == 1:
				note = f" digits tabular @ {widths.pop()}/{font['head'].unitsPerEm}"
			else:
				note = f" digits PROPORTIONAL {sorted(widths)}"
				failures.append(f"{name}: value face digits are not equal-width")
		print(f"{name:34s} {len(font.getGlyphOrder()):4d} glyphs  {status}{note}")

	if failures:
		print("\nFAILED:")
		for line in failures:
			print("  " + line)
		return 1
	print("\nall vendored webfonts cover the required glyph set")
	return 0


if __name__ == "__main__":
	sys.exit(main())
