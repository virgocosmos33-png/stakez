# Game Concept — "MADAM MIRROR" (working title)

Gothic horror re-theme of the dynamic-ways concept. Same mechanics core (they're solid), completely new skin, tone and fiction — **Nolimit City-style gritty horror with a shady-lady lead**. Think MENTAL's grime + a Victorian séance parlor: a fraudulent medium who tore the veil for real, and the mirror that keeps her.

---

## 1. Pitch

> 1897. Madam Mirror runs séances for London's rich — every one of them a con. Until the night she used the wrong mirror. Now every reflection in her parlor is alive, and none of them are hers.
>
> Symbols that land beside a **Haunted Mirror** are *reflected* — one cell becomes 2, 3 or 4 apparitions, multiplying the ways count. Tear the veil completely and enter **THE OTHER SIDE**, where reflections never fade: haunted cells persist spin after spin until the parlor holds over a million ways.

- **Grid:** 5 reels × 4 rows (our solved layout).
- **Win type:** ways-pays with per-cell apparition counts (1–4). Max 16⁵ = **1,048,576 ways**.
- **Mechanic branding:** **xMirror** (NLC-style naming).
- **Volatility:** NLC-grade extreme. RTP 96.5%. **Wincap 30,000x.**
- **Three bonus levels** (3/4/5 scatters), each separately buyable.

## 2. Fiction → mechanics mapping

| Mechanic (unchanged) | Horror skin |
|---|---|
| Clone Seal splits neighbors into 2–4 copies | **Haunted Mirror** lands, cracks, and *reflects* adjacent cells into 2–4 apparitions; ghostly duplicates slide out of the cell |
| Seal transforms into best adjacent symbol | the mirror "shows what it wants you to see" — resolves into the highest-paying neighbor |
| Ways counter | brass séance counter / candle tally above the board, flickers up with each reflection |
| Free spins with persistent charged cells | **THE OTHER SIDE** — the veil is torn; haunted cells stay haunted for the whole bonus, wins deepen the haunting (+1 apparition, max 4) |
| Super buy with pre-charged cells | **BLOOD MOON séance** — starts with 4 already-haunted cells |
| Win × ways slam presentation | NLC-style: win amount in bone-white, "× ways" stamps over it in blood red, total slams with a scream sting |

## 3. Symbols (all art to be generated — horror set, no ninja assets reused)

Five character high symbols and five playing-card low ranks (A K Q J 10),
all painted as haunted daguerreotype cards in a shared ornate filigree frame.

| ID | Symbol | Art direction |
|---|---|---|
| H1 | **Lady Mirror** | veiled Victorian medium in black lace, faintly glowing white eyes behind the veil, a cracked hand mirror at her chest — the shady-lady lead, top regular pay |
| H2 | **The Wife** | mournful widow in a high-collared black mourning gown, wedding ring on a chain, thin tears of dark ichor |
| H3 | **The Man** | stern gentleman in a top hat and frock coat, séance rope burn around his neck, cold hollow eyes |
| H4 | **The Little Girl** | pale child in a lace dress holding a cracked porcelain doll, blank black eyes, unsettling smile |
| H5 | **The Dog** | gaunt spectral black hound, glowing absinthe-green eyes, bared teeth, antique Victorian collar — the lowest character |
| L1 | **Ace (A)** | large gothic silver serif "A" over a carved spade, engraved filigree |
| L2 | **King (K)** | large gothic silver serif "K" under a tarnished crown |
| L3 | **Queen (Q)** | large gothic silver serif "Q" with a mourning-veil / tiara motif |
| L4 | **Jack (J)** | large gothic silver serif "J" over crossed daggers |
| L5 | **Ten (10)** | large gothic silver serif "10", engraved filigree |
| W | **The Entity** — tall shadow silhouette filling the frame, "WILD" carved into it | substitutes all but S/HM; reflected wilds multiply ways through |
| S | **Ouija planchette** on "SCATTER" letters | 3+ triggers The Other Side |
| HM | **Haunted Mirror** — ornate cracked Victorian mirror, something moving in it | the xMirror trigger; doesn't pay, reflects neighbors, then resolves |

Palette: desaturated sepia/charcoal parlor, accents only in blood red (wins, multiplier stamps) and absinthe green (haunted cells). Film-grain vignette. Symbols get thick painterly outlines so they read at 120px — same production pipeline as the ninja set (`GenerateImage` → flood-fill keying → `repack_symbols.py`).

Sound direction: detuned music box loop; dry whispers on mirror cracks; single heartbeat thump per anticipation reel; all wins scored with low strings instead of fanfares (NLC does "dread over celebration").

## 4. Mechanics (identical math to the previous draft, renamed)

### 4.1 Base spin
1. Normal reveal (padded 6-row arrays).
2. 0–2 **Haunted Mirrors** may land (reels 2–4, weighted, never on scatter reels, suppressed on forced-zero-win sims).
3. Each mirror cracks: adjacent cells (orthogonal) roll apparitions from `{2: 60, 3: 30, 4: 10}`; the mirror resolves into the highest-paying adjacent symbol.
4. Ways evaluation: per reel, `count_r = Σ apparitions(cell)` over matching+wild cells; ways = product across the run; win = `paytable[(kind, sym)] × ways`.

### 4.2 Three bonus levels (NLC-style tiered free spins)

Scatter count picks the level; each level is a strictly nastier version of the last:

| Level | Trigger | Name | Spins | Rules |
|---|---|---|---|---|
| 1 | 3 scatters | **THE SÉANCE** | 8 | Haunted cells persist across spins. Mirrors at base frequency. |
| 2 | 4 scatters | **THE OTHER SIDE** | 10 | Persistence + **deepening**: every win through a haunted cell adds +1 apparition (max 4). |
| 3 | 5 scatters | **BLOOD MOON** | 12 | Everything in level 2 + starts with **4 pre-haunted cells** (2 apparitions each) + **guaranteed ≥1 mirror per spin**. |

- Retrigger: 2 scatters = +3 spins (same level).
- The board visually decays with the level: cracked frame at L1, green light bleed at L2, blood-red moonlight at L3.
- Wincap **30,000x** ends any bonus instantly (standard `wincap` criteria).
- `freeSpinTrigger` book event gains a `level: 1|2|3` field so the frontend picks intro panel, background tint, and music stem.

### 4.3 Bet modes (5 total — base + 3 buys + wincap distribution inside each)
| Mode | Cost | Content |
|---|---|---|
| base | 1.0x | everything above, all 3 levels reachable naturally |
| **Séance buy** | 100x | guaranteed 3-scatter trigger (level 1) |
| **Other Side buy** | 400x | guaranteed 4-scatter trigger (level 2) |
| **Blood Moon buy** | 1,000x | guaranteed 5-scatter trigger (level 3) |

Each buy mode is its own `BetMode` with its own books, lookup table, and 96.5% RTP — the level differences live in the *distribution conditions* (forced scatter counts) plus level-aware free-spin logic in `run_freespin`.

### 4.4 Paytable (per way, ×bet — optimizer tunes frequency)
| Symbol | 3 | 4 | 5 |
|---|---|---|---|
| H1 Lady Mirror | 1.0 | 3.0 | 10.0 |
| H2 The Wife | 0.6 | 1.5 | 5.0 |
| H3 The Man | 0.5 | 1.2 | 4.0 |
| H4 The Little Girl | 0.4 | 1.0 | 3.0 |
| H5 The Dog | 0.3 | 0.8 | 2.5 |
| L1 Ace / L2 King | 0.2 | 0.4 | 1.2 |
| L3 Queen / L4 Jack / L5 Ten | 0.1 | 0.3 | 0.8 |

## 5. Book event contract

Same three new events, renamed to the fiction:

```json
{ "type": "mirrorBurst",
  "mirrors": [ { "mirror": {"reel": 2, "row": 1},
                 "reflected": [ {"reel": 2, "row": 0, "apparitions": 3},
                                {"reel": 1, "row": 1, "apparitions": 2} ],
                 "mirrorBecomes": {"name": "H1"} } ],
  "totalWays": 4608 }

{ "type": "hauntDeepen", "cells": [ {"reel": 2, "row": 0, "apparitions": 4} ] }

{ "type": "winInfo", "wins": [ { "symbol": "H1", "kind": 4, "ways": 96, "win": 5400,
    "positions": [...], "meta": { "hauntedCells": [...] } } ] }
```

`reveal` / `setWin` / `setTotalWin` / `freeSpinTrigger` / `finalWin` unchanged from the lines game.

## 6. Implementation plan (unchanged structure, renamed)

**Math — `games/0_1_madam_mirror/`** (skeleton: copy `0_0_ways`)
- `game_config.py`: 5×4, paytable, `mirror_config = {probability, allowed_reels, apparition_weights, max_mirrors}`, 3 bet modes.
- `game_calculations.py`: new `MirrorWays.get_ways()` — Σ/product evaluation (§4.1.4). **Build and unit-test this first.**
- `game_override.py`: `draw_board` override placing mirrors post-draw (the `apply_wild_nudge` pattern); `self.haunted_cells` dict persisted across free spins, reset in `reset_book`.
- `game_events.py`: `mirror_burst_event`, `haunt_deepen_event`.
- `game_optimization.py`: wincap 0.1% / freegame ~38% / basegame ~58% / zero-win, as before.

**Web — `apps/mirror/`** (skeleton: copy `apps/ways`)
- `typesBookEvent.ts` + handlers: `mirrorBurst` (crack sfx → reflection slide-out per cell → ways counter tick-up), `hauntDeepen` (green pulse + badge upgrade).
- `ApparitionCell.svelte`: renders 2/3/4 ghost-copies of the symbol sprite in-cell + corner count badge (composition of existing `Symbol`).
- `WaysCounter.svelte`: séance counter above the board (positioning math from `WildNudgeMultiplier`).
- Win × ways slam: reuse the `NudgeWinBoost` pattern with the horror styling.
- New atlas via `repack_symbols.py` once the 13 horror icons are generated.

**Build order:** math eval → mirrorBurst events + showcase book → Storybook frontend → free-spin persistence → buy modes + optimizer → art/sound polish.

## 7. Numbers (NLC-style extreme volatility)

- RTP 96.5% on all 4 modes; wincap **30,000x** (target hit probability ~1 in 5–10 million spins; the optimizer's `wincap` criteria quota controls this).
- Base game deliberately starved: hit rate ~1 in 4, ~70–75% of spins pay nothing, base RTP share ~55% — the rest lives in the bonuses (NLC profile).
- Bonus targets: L1 avg ~60x, L2 avg ~120x, L3 avg ~350x, all fat-tailed (top 1% of L3 > 3,000x).
- This will fail Stake's 3-star volatility check by design — we accept the higher volatility rating (5-star), same decision NLC games make. If a cap is ever required, the lever is the apparition max (4 → 3) and L3's guaranteed-mirror rule.
- Reel strips: scatter-rich reels 1/3/5, scatter-scarce reels 2/4 in base (3-scatter triggers are common, 4/5 rare — but all levels stay naturally reachable), mirrors never on reels 1/5.

---

## Re-themed alternates

**A. "TEN BELOW" — morgue cluster game.** The Cursed Vault infection mechanic in a 1920s morgue: 7×7 cluster-pays with tumbles; **frostbite** spreads from tagged tiles each tumble; frozen tiles are wilds that *steal 10% of each win into a body drawer*; clear a full row/column of frost to crack the drawer open for the stash × tumble count.

**B. "LAST RITES" — the tower-climb, re-themed as an exorcism.** Each bet pushes a possessed girl's exorcism one rite deeper: 20 rites, predetermined survive/fail per book, rising multiplier ladder, cash-out-or-continue tension. Fastest to ship (~⅓ of a slot), pure NLC dread pacing.

**C. "DEAD RINGER" — dual-board doppelgänger slot.** Two mirrored 3×5 boards ("the parlor" and "the reflection"); wilds landing on one spawn a shadow twin at the mirrored cell of the other; simultaneous wins on both boards multiply each other. 70% reuse of the 4x5 lines math.
