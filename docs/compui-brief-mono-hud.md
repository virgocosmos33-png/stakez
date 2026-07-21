# CompUI Design Brief — Madam Mirror Mono HUD + Pay Table

## Context Summary
- **Stack:** SvelteKit + PixiJS (pixi-svelte) for the in-canvas HUD; Svelte + SCSS for HTML modals (`components-ui-html`). Monorepo (`web-sdk`), Storybook on :6001.
- **Scope:** The whole HUD (already mono) needs: (1) working +/- stepper, (2) removal of the redundant bet-menu button, (3) equal spacing / no overlaps across desktop/landscape/portrait/tablet, (4) the HTML pay-table + all modals restyled to the SAME shared mono system.
- **Brand keywords:** monochrome, command-center, minimalist, precision, hairline, gothic-restraint.
- **Constraints:** Pure black/white (user chose EXACT), no external font requests (Stake XSS policy — system fonts only for pixi; bundled woff2 for HTML), a11y contrast 4.5:1, 44px+ touch targets, `prefers-reduced-motion`.

---

## 1. React Bits
### Research performed
- Queries: `minimalist black and white game UI HUD monochrome bevel button system 2026`.
- Findings were mostly Unity/itch sprite kits (not React) — confirms the mono/bevel language is a recognised "clarity-first" HUD idiom (buttons, pills, panels, toggles, one unified rhythm) but offers no drop-in React code for a Pixi canvas.

### Findings
| Element | Category | Use in project | Link | Notes |
|---------|----------|----------------|------|-------|
| "Classic B&W" unified kit rhythm | Components | Validates one shared silhouette + state set so HUD doesn't look "stitched" | assetstore (Modern UI Kit) | Concept only; we draw vector in Pixi |

### Code patterns
- No deps to add. Motion stays CSS/tween only. Keep transitions ~120–180ms (matches existing HTML `.rail-btn`), respect reduced-motion.

---

## 2. Refero  ← PRIMARY token source
### Research performed
- Queries: `Refero monochrome black white minimal Linear Vercel dark UI tokens`.
- DESIGN.md systems reviewed: **Vercel**, **Linear**, **Trunk** (all near-monochrome command centers).

### Design tokens extracted (dark-canvas variants)
| Token | Value | Semantic role |
|-------|-------|---------------|
| Floor (bg) | `#08090a` (Linear) / near-black, NOT `#000` | page/stage — avoid harsh pure black |
| Surface 1 | `#0f1011` | panels, pill bodies |
| Surface 2 | `#141516` / `#18191a` | hover / lifted |
| Inverted fill | `#ffffff` | primary CTA (SPIN), value chips |
| Hairline | `#23252a → #34343a → #3e3e44` | 0.5–1px borders (depth = borders, NOT shadow) |
| Text hi | `#ffffff` (tight tracking −0.02em) | headings, values |
| Text mid | `#b8b8be`/`#8a8a90` | labels, secondary |
| Text on-white | `#0b0b0d` | text/glyphs on inverted fills |
| Radius | 6px cards/buttons · 9999px pills | sharpness is the point (never >6px on rects) |
| Spacing | **4px grid** (4/8/12/16/24…) | compact, equal rhythm |
| Weights | 400–600 (no 700+ display) | precision, not shouting |
| Numerals | `tabular-nums` | bet/balance/pays align |

### Component & usage rules (from Vercel/Linear)
- Depth through **tonal value shifts + hairline borders**, never drop-shadows.
- One accent max, functional only. Our system: the accent IS white (inverted fill) — no colour.
- Buttons: pure black-on-white or white-on-black; 6px radius or full pill.
- "Unafraid of empty space" — consistent gaps, no cramped clusters (directly answers the overlap complaint).

---

## 3. Uiverse
### Research performed
- Filters/queries: `uiverse.io stepper quantity input plus minus dark tailwind` (+ HyperUI, Material Tailwind steppers).

### Shortlist
| Element | Category | Adaptation plan | Link |
|---------|----------|-----------------|------|
| Bordered quantity stepper `[ − | n | + ]` | inputs | Full-cell `size-10` (≈44px) click targets each side; thin divider; our bevel pill instead of rounded-rect | hyperui.dev/components/application/quantity-inputs |
| Plain +/- counter | buttons | Confirms +/- must have LARGE hit targets, hover opacity shift | material-tailwind input-number |

### CSS/Tailwind patterns to reuse
- **Critical fix insight:** every stepper button is a full `size-10` box (not just the glyph). In Pixi this means each +/- zone needs an explicit hit rectangle covering the whole cell — the current bug is the hit area = thin glyph pixels only.

---

## 4. shadcn/ui  ← component/token MODEL source
### Scaffold choices
- Style preset: new-york density; Base color: **zinc/neutral** (pure grayscale, hue 0); Radius: `6px`; Font: system sans (Geist-like) — we use a system sans stack.

### Components to add/use (mapping, not installing shadcn into Pixi)
| Concept | Status | Customization |
|-----------|--------|---------------|
| Semantic token layer | new (shared) | mirror `--background/--foreground/--card/--muted/--border/--ring` in BOTH pixi `hudTheme.ts` and an HTML `mono.scss` so the pay table matches the HUD |
| Card / Dialog / Tabs | restyle existing HTML modals | flat surface + hairline border + 6px radius |
| Stepper / Button | Pixi vector | inverted primary, outlined secondary |

### Theme variable map (HTML `:root`, dark)
```
--mono-bg:#08090a  --mono-surface:#101012  --mono-surface-2:#17181a
--mono-line:#ffffff  --mono-hairline:#2a2b2f  --mono-fill:#ffffff
--mono-fg:#ffffff  --mono-fg-dim:#9a9aa0  --mono-on-fill:#0a0a0c
--mono-radius:6px  --mono-radius-pill:9999px
```
(Replaces the gold `--ds-gold*` tokens for the mono look; keep old vars aliased so nothing breaks.)

---

## 5. AntV Infographic
### Research performed
- Queries: `AntV infographic paytable comparison stats grid declarative JSX dark theme`.
- Reviewed: declarative syntax (`list-grid-*`, `compare-*`, `chart-*`), dark theme block, `@antv/infographic-jsx`.

### Infographic patterns
| Type | Use in project | Link | Integration |
|------|----------------|------|-------------|
| `list-grid-*` | Pay table PAYOUT grid (symbol → 5/4/3 pays) | infographic.antv.vision | Concept — we hand-build the grid in SCSS (no runtime dep) |
| `compare-*` / rows | RTP / free-spins / feature-buy rows | same | Two-column `label · value` rows, hairline separated |
| `theme dark` block | palette discipline | learn/infographic-syntax | Map palette to mono tokens |

### Data viz layer notes
- Pay table is fundamentally a **stats/comparison infographic**: symbol tiles + tabular pays + label/value rows. Apply mono tokens: hairline row separators, tabular-nums values, no gold. No new dependency — AntV informs the LAYOUT (alignment, hierarchy, data-ink ratio), implemented in existing SCSS.

---

## Cross-source notes
- Conflicts resolved: Vercel uses light canvas, Linear/Trunk use dark — we take the **dark variants** (our stage is black) but keep Vercel's border/typography discipline.
- Accent: sources use one functional colour; user wants NONE — so "accent" = the white inverted fill. Replace all gold (`#ffc12e`, `#c9a227`) in HTML modals with mono tokens.
- Gap (no source match): the "folder-tab" on the BET pill is bespoke — keep, but align its stroke/gap to the hairline system.

---

## Unified CompUI System (synthesis)

### Tokens (single source, mirrored pixi ↔ html)
- Colors: black floor `#08090a`, surfaces `#101012/#17181a`, white line/fill `#ffffff`, on-fill `#0a0a0c`, dim text `#9a9aa0`, disabled `#4a4a4e`.
- Type: system sans; weights 400–600; tight tracking on caps labels; **tabular-nums** on all numbers.
- Spacing: 4px grid. HUD uses ONE `GAP` unit between every neighbour (equal spacing mandate).
- Radius/bevel: octagon chamfer for HUD controls; 6px for HTML cards; full-pill for value chips.
- Motion: 120–180ms opacity/scale, reduced-motion safe.

### Component map
| UI need | Base (shadcn model) | Motion (React Bits) | Micro (Uiverse) | Data (AntV) |
|---------|--------------------|---------------------|-----------------|-------------|
| SPIN | inverted primary | press scale | — | — |
| BONUS/AUTO/TURBO | outlined medallion | hover fill | — | — |
| BET stepper | outlined pill | — | full-cell +/- targets | — |
| BALANCE/WIN | split pill | count tween | — | value chip |
| Pay table | card + hairline rows | — | — | list-grid + compare rows |

### Implementation order
1. Fix +/- hit areas (bug) — highest priority.
2. Remove bet-menu button; rebalance layouts to equal GAP; kill overlaps.
3. Shared mono token layer for HTML (`mono.scss`) mirroring `hudTheme.ts`.
4. Restyle ModalPayTable (+ shared modal chrome) to mono.
5. QA all four layouts + pay table.
```
