# Tombstone Reborn western webfonts

Browser faces for every `PIXI.Text` surface in the game. Vendored here because the
Stake Engine XSS policy requires the build to be fully static with no external
requests, so nothing may be fetched from `fonts.googleapis.com` at runtime.

Wiring: `src/game/typography.css` declares the `@font-face` blocks and
`src/game/typography.ts` maps them to the four roles and registers them with
`preloadFont()` so they are rasterized before the canvas draws.

The baked BITMAP face used for celebration amounts lives in `../tombstoneFont/`
and is **baked from Rye in this folder** by `tools/make_tombstone_font.py`, with
Archivo Narrow covering the four currency signs Rye does not ship. It used to be
baked from `C:\Windows\Fonts\georgiab.ttf`, which put proprietary Microsoft
outlines into a shipped atlas and made the output depend on the build machine.
That script also now pads the digits into one shared advance cell, because it
crops every glyph to its ink and would otherwise hand PIXI proportional figures
and make win count-ups jitter.

## Faces

| Role | Family | Files | Licence | Designer |
|------|--------|-------|---------|----------|
| display | Rye | `rye-400-latin*.woff2` | SIL Open Font License 1.1 | Nicole Fally / Sorkin Type Co |
| label | Oswald (variable 400–700) | `oswald-var-latin*.woff2` | SIL Open Font License 1.1 | Vernon Adams, Kalapi Gajjar, Cyreal |
| value | Archivo Narrow (variable 400–700) | `archivo-narrow-var-latin*.woff2` | SIL Open Font License 1.1 | Omnibus-Type |
| accent | Special Elite | `special-elite-400-latin*.woff2` | Apache License 2.0 | Astigmatic |

Full licence texts ship alongside the fonts as `LICENSE-*.txt`, as the OFL
requires. Total payload is ~200 KB across all eight files.

Each family is split into Google's stock `latin` and `latin-ext` subsets. The
`latin-ext` half is not optional for the **value** face: the exotic currency
symbols (₹ U+20B9, ₽ U+20BD, ₱ U+20B1, ₩ U+20A9) sit in `U+20A0-20AB` /
`U+20AD-20C0`, so dropping it would silently lose glyphs from long-currency
amounts.

## Verifying

```powershell
python tools/qa_verify_webfonts.py        # glyph coverage + tabular figures
python tools/make_typography_metrics.py   # re-bake the advance-width table
python tools/make_tombstone_font.py       # re-bake the bitmap amount atlas
python tools/qa_typography_shots.py 6009  # LIVE: faces render, estimates hold
```

`qa_typography_shots.py` is the one that catches the failure mode this system
exists to prevent. PIXI rasterizes text to a texture and never re-rasterizes, so
a face that loads late leaves a system fallback baked into the HUD with no error
logged anywhere. It measures each role against the fallback tail of its own stack
(identical widths mean the vendored face never won), checks the `latin-ext` subset
was preloaded rather than left for first use, and compares `estimateTextWidth`
against the browser's own layout on the strings that clip in production.

`qa_verify_webfonts.py` is what proves the value face is safe for count-ups:
`PIXI.TextStyle` has no `font-feature-settings`, so `tnum` cannot be enabled at
runtime and the face's default figures must already be equal width. Archivo
Narrow is (456/1000 upem at weight 700); Oswald, Bitter, Barlow Condensed, Saira
Condensed, Fira Sans Condensed and Encode Sans Condensed all are not, which is
why they were rejected for that role.
