# MADAM MIRROR — Asset Preparation Checklist

Everything the game needs, in the exact formats the web-sdk loads. Split by **who prepares it**:

- **[YOU]** — things you must source/decide (mostly audio and any pro animation).
- **[ME]** — I generate with the image pipeline we already built (AI image → background keying → atlas packing).
- **[CODE]** — no asset needed; faked with tweens/tints/particles in code.
- **[REUSE]** — keep the SDK's existing asset initially, replace later if wanted.

Priority: **P1** = needed for the Storybook-playable prototype. **P2** = needed before demo/publish. **P3** = polish.

---

## 1. Symbol art (the reels) — P1

13 icons, each: **1024×1024 PNG, one centered object, thick dark painterly outline, plain background** (my keying script removes it). They get packed into 200×200 atlas cells by `repack_symbols.py`.

| # | Symbol | Notes |
|---|---|---|
| 1 | H1 Madam Mirror (veiled medium, glowing eyes) | [ME] |
| 2 | H2 The Twins (porcelain-faced girls) | [ME] |
| 3 | H3 The Client (dead aristocrat, top hat) | [ME] |
| 4 | H4 The Familiar (black cat, human iris) | [ME] |
| 5 | L1 burning Tower tarot card | [ME] |
| 6 | L2 melted candelabra | [ME] |
| 7 | L3 crystal ball with a face inside | [ME] |
| 8 | L4 scratched-out mourning locket | [ME] |
| 9 | L5 absinthe glass | [ME] |
| 10 | W The Entity + "WILD" banner | [ME] |
| 11 | S ouija planchette + "SCATTER" banner | [ME] |
| 12 | HM Haunted Mirror — **intact** state | [ME] |
| 13 | HM Haunted Mirror — **cracked** state (same framing as #12; shown after the burst) | [ME] |

Extra per-symbol states (win/land/explode) are **[CODE]** for the prototype: scale-pulse + glow tint on the static sprite (we verified `SymbolSprite` resolves win states safely). Spine-animated symbols are P3 (see §6).

**[YOU]:** approve the art style from 1–2 test icons before I batch all 13 (same as we did with ninja).

## 2. Board & environment — P1/P2

| Asset | Spec | Who |
|---|---|---|
| Base-game background (séance parlor, dark, candle-lit) | 2039×1000 **and** 1242×2208 portrait, JPG/WebP, symbol area must stay dark/low-contrast in the middle | [ME] P1 |
| Free-spin background (THE OTHER SIDE — same parlor, absinthe-green, mirrored/decayed) | same sizes | [ME] P2 |
| Reels frame (ornate Victorian mirror frame around the 5×4 board) | ~1400×1200 PNG, transparent center window with 5:4-ish proportions | [ME] P1 |
| Board mask/backdrop tint | flat dark panel behind symbols | [CODE] |
| Background ambience (dust, candle flicker) | SDK uses a Spine here; we substitute a static image + code-driven flicker (alpha sine) and drifting dust particles | [CODE] P2 |
| Loading screen art (title + Madam portrait) | 1920×1080 JPG + game logo PNG ~1000×400 transparent | [ME] P2 |
| Favicon | 64×64 | [ME] P3 |

## 3. Feature/UI graphics — P1/P2

| Asset | Spec | Who |
|---|---|---|
| Ways counter panel (brass séance counter above board) | ~800×200 PNG transparent | [ME] P1 |
| Apparition count badge (2/3/4 on haunted cells) | [CODE] — BitmapText over a small dark disc, like the nudge badge | [CODE] P1 |
| Free-spin intro panels — **one per bonus level** (THE SÉANCE / THE OTHER SIDE / BLOOD MOON) | 3 PNG frames ~1200×900; text is BitmapText | [ME] P2 |
| Free-spin counter panel | ~824×622 PNG (same slot as `Frame_FSCounter.png`) | [ME] P2 |
| Win level panels (BIG WIN / EPIC / MAX — blood-red stamps) | can start as BitmapText only; art panels later | [CODE] P1 → [ME] P3 |
| Buy-bonus buttons — **3 tiers** (Séance 100x / Other Side 400x / Blood Moon 1000x) | 3 PNGs ~500×300, escalating menace | [ME] P2 |
| Bonus-level background tints (L2 green bleed, L3 blood moon) | code tint over the free-spin background, optional L3 art variant | [CODE] P2 → [ME] P3 |
| "Press anywhere to continue" | [REUSE] existing sprite | — |
| Paytable/info screens | generated from symbol icons + text at runtime | [CODE] P2 |
| Coin/ember particle for win celebrations | [REUSE] coin spritesheet, or 1 ember PNG re-colored | [REUSE] P1, [ME] P3 |

## 4. Animations — P1/P2

**No GIFs needed anywhere** — PixiJS uses either sprite-sheet flipbooks (PNG strip + JSON, like the coin) or Spine. If you ever hand me a GIF/video reference, I convert it to a sprite sheet.

| Animation | How | Who |
|---|---|---|
| Mirror crack burst | swap intact→cracked sprite + white flash + shards: **8–12 frame flipbook**, 400×400/frame — I can generate frames or fake with code shake+flash first | [CODE] P1 → [ME] P2 |
| Apparition split (copies slide out of a cell) | tween clones out with alpha/scale — no asset | [CODE] P1 |
| Haunt deepen pulse (green shockwave on cell) | code tint pulse + 1 radial-glow PNG | [ME]+[CODE] P1 |
| Ways counter tick-up | BitmapText count-up tween | [CODE] P1 |
| Win × ways slam | reuse NudgeWinBoost pattern, horror styling | [CODE] P1 |
| Anticipation (reel about to land scatter) | [REUSE] SDK anticipation spine, or code glow overlay | [REUSE] P1 |
| Transition to free spins (veil tear wipe) | [REUSE] SDK transition spine first; custom flipbook later | [REUSE] P1 → [ME] P3 |
| Big win sequence | [REUSE] SDK bigwin spine initially | [REUSE] P2 → P3 custom |
| Symbol win animations (Spine) | only if we hire a Spine animator — optional | [YOU] decide, P3 |

## 5. Audio — P2 — **this is the main thing only YOU can prepare**

The engine loads **one audio-sprite file** (`sounds.mp3/.ogg/.m4a/.ac3` + `sounds.json` with named offsets). You collect the individual files; I concatenate and generate the JSON with an audiosprite tool.

Deliver as individual **WAV or MP3** files, named as below:

**Music (loops, seamless):**
| Cue | Length | Direction |
|---|---|---|
| `bgm_main` | 1.5–2.5 min loop | detuned music box + low strings, sparse |
| `bgm_freespin` | ~1 min loop | same motif, absinthe-green tension, whispers (levels 1–2) |
| `bgm_freespin_blood` | ~1 min loop | Blood Moon (level 3) variant — heavier percussion, choir | 
| `bgm_winlevel_big/mega/epic/max` | 8 s loops (4 files) | dread-swells, not fanfares |

**SFX (short, dry):**
| Cue | Direction |
|---|---|
| `sfx_btn_general` | soft brass click |
| `sfx_reel_stop_1` | heavy wooden thunk |
| `sfx_anticipation` + `sfx_anticipation_start` | heartbeat build ~7 s + single thump |
| `sfx_scatter_stop_1..5` (5 files, rising pitch) | planchette scrape, each higher/tenser |
| `sfx_scatter_win_v2` | ouija board rattle + gasp |
| `sfx_mirror_crack` | glass fracture + whisper burst (our custom cue) |
| `sfx_apparition` | breathy wisp (clone slide-out) |
| `sfx_haunt_deepen` | low reversed piano hit (charge upgrade) |
| `sfx_winlevel_small` | short string sting |
| `sfx_youwon_panel` | church bell, single |
| `sfx_bigwin_coinloop` | shimmer loop (embers, not coins) |
| `jng_intro_fs` | 2 s veil-tear jingle |
| `sfx_superfreespin` | choir hit |

Sources: any royalty-free library (Freesound, Pixabay Audio, Epidemic if you have it). **License must allow commercial redistribution** — keep receipts/links per file.

## 6. Fonts — P2

Bitmap fonts (BMFont: `.xml/.fnt` + PNG page). We [REUSE] the `gold` font for the prototype. For theme polish, pick 1–2 horror display fonts (check license!) and I convert them to BMFont with charset `A–Z 0–9 $ . , × %`:

- **[YOU]:** choose the font(s) — e.g. something like "IM Fell", "Cinzel Decorative", or a grungier display face.
- **[ME]:** conversion + drop-in.

## 7. What YOU personally need to prepare — short list

1. **Approve the visual style** — I'll make 2 test symbols first; you say go/no-go. (P1, 5 min)
2. **Audio pack** — the ~20 cues in §5, royalty-free, named as listed. (P2, the only genuinely manual task)
3. **Font choice** — 1–2 licensed horror display fonts. (P2, 15 min)
4. **Decide on Spine budget** — none needed to ship a demo; hiring a Spine animator later upgrades symbol wins, transition, and big-win to NLC production level. (P3)
5. **Original-IP check** — theme is original, but when we later reskin the *ninja* game, its icons need de-Naruto-ing before any store submission.

Everything else on this page is [ME]/[CODE]/[REUSE].
