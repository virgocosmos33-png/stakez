# Game Concept — "TOMBSTONE REBORN"

> **Build status.** The **main game is built and running** (6-reel ways base
> game, math optimized locally). Everything below about Revenge Spins, the KILL
> MULTIPLIER, the escalating smile and the six win cutscenes is the **roadmap
> for the feature pass** — not in the current build. Sections 3–4 are the
> forward design; sections 1–2, 5–6 already describe shipped code where noted.

A dead-eyed western revenge slot. He died. He came back. He can't smile anymore.
Killing them brings the smile back. The whole game is one escalating story: the
protagonist gets *happier* as it gets more violent, and the player watches his
face change while the multiplier climbs.

- **Grid:** 6 reels, variable column heights **3 · 4 · 4 · 2 · 2 · 1** (a coffin/
  headstone silhouette). Ways-pays. Max ways = 3·4·4·2·2·1 = **192**.
- **Win type:** ways.
- **Volatility:** high. RTP 96.5%. **Wincap 99,999x** — the signature top award.
- **Free game:** REVENGE SPINS, driven by the KILL MULTIPLIER ladder.
- **Modes:** base, ante (2.5x), bonus1/2/3 buys (3/4/5-scatter entries).

---

## 1. The core character — The Gunslinger

No title. Just The Gunslinger. Dead for years, grave cracked and forgotten. He
wakes with one emotion: anger. He can't smile — **until he kills someone.** Then
a tiny smile. As the game gets more violent the smile grows, and the KILL
MULTIPLIER grows in lock-step. That is the entire personality of the game.

### Five facial states (the subconscious hook)

| Kills so far | `smileState` | Face | Feeling |
|---|---|---|---|
| 0 (base / just returned) | `grim` | 😐 | anger, nothing |
| 1 | `faint` | 🙂 | first blood |
| 2–3 | `smirk` | 😏 | payback |
| 4 | `grin` | 😈 | the killer — *he's enjoying it* |
| 5+ (and 99,999x) | `evil` | full evil smile | "I feel better." |

The math emits a `smileState` book event on every kill; the frontend swaps the
Gunslinger portrait beside the board and steps the KILL MULTIPLIER badge.

---

## 2. Symbols (all art to be generated — western set)

The Gunslinger is #1. The other four premiums are the people who wronged him
before his death; killing them in the win/death animations is the payoff.

| ID | Symbol | Art + death animation |
|---|---|---|
| **H1** | **The Gunslinger** | long black coat, dusty hat, revolver. Expressionless until he kills. Top pay. |
| **H2** | **The Duchess** | black Victorian dress, extravagant hat, pearls, golden pistol. *Death:* he shoots her chandelier — it falls — CRUSH — he looks at camera, tiny smile. |
| **H3** | **The Butcher** | huge outlaw, apron, cleaver, massive beard, blood. Actually killed him. *Death:* Butcher swings, Gunslinger catches the cleaver, BANG, Butcher drops. |
| **H4** | **The Card Shark** | purple suit, gold teeth, cards. Cheated him of his fortune. *Death:* draws five cards, Gunslinger shoots them out of his hand, bullets hit him, picks up the Ace of Spades, smiles. |
| **H5** | **The Preacher** | black outfit, white beard, huge silver cross. Buried him alive. *Death:* he prays, Gunslinger walks through the prayer, barrel to forehead, BANG, silence. |
| L1–L5 | bullet · whiskey · spur · horseshoe · playing card | western trinkets, low pays |
| **W** | **the revolver** (wild) | substitutes; pays on its own only as a full 6-reel wild line |
| **S** | **the tombstone** (scatter) | 3+ triggers Revenge Spins |

---

## 3. The KILL MULTIPLIER (Revenge Spins)

Free spins are the engine of the fantasy. A **kill** = any Revenge spin whose win
includes a premium (H1–H5). Each kill widens the smile and steps the multiplier
one rung up the ladder; the multiplier applies to subsequent spins' ways wins
(`multiplier_strategy="global"`).

```
kills:  1    2    3    4     5     6     7     8+
mult:  ×1   ×2   ×3   ×5   ×10   ×25   ×50  ×100
```

Under a forced-wincap search the ladder keeps doubling past the top rung so a
premium-dense Revenge run can climb into the 99,999x cap. Source of truth:
`math-sdk/games/0_3_tombstone_reborn/game_config.py` → `kill_ladder`.

Entry: 3 / 4 / 5 scatters award 8 / 10 / 12 spins (each separately buyable as
bonus1/2/3). Ante guarantees a scatter on reel 0 for ~2x trigger rate.

---

## 4. The win animations — one escalating story

There aren't six unrelated wins; they're one story. Map each to book events:

| Beat | Trigger (book event) | Scene |
|---|---|---|
| **WIN 1 — The Return** | `freeSpinTrigger` (bonus entry) | dark, THUMP, tombstone cracks, a hand comes through, he pulls himself out, sees the town. No smile yet. Asset `cutsceneReturn`. |
| **WIN 2 — First Blood** | first `smileState` with `state:"faint"` | the Duchess sees him, "You?", BANG, 😐→🙂 tiniest smile. `cutsceneFirstBlood`. |
| **WIN 3 — Payback** | `smileState` reaching `smirk` | poker table, four aces, he shoots the Card Shark across the table, bigger smile. `cutscenePayback`. |
| **WIN 4 — The Killer** | `smileState` reaching `grin` | Butcher charges, crashes through the saloon doors, one bullet in his hat, he chuckles — *killing is making him happy.* `cutsceneKiller`. |
| **WIN 5 — The Last Rite** | `smileState` reaching `evil` | the Preacher prays, church bell DONG per step, barrel to forehead, BANG, silence, he smiles properly. `cutsceneLastRite`. |
| **WIN 6 — MAX WIN / THE SMILE** | `wincap` event (99,999x) | black screen, breathing, CLICK·CLICK·CLICK reload, camera to his face, the four dead premiums around his tombstone, he looks at camera and **smiles** — eyes stay dead. Then **99,999×** and **"I feel better."** `cutsceneMaxWin` + `voIFeelBetter`. |

No giant explosion, no multiplier tornado. The signature is the smile.

---

## 5. Book event contract (frontend ⟷ math)

Standard engine events: `reveal`, `winInfo`, `setWin`, `setTotalWin`,
`freeSpinTrigger` / `freeSpinRetrigger`, `updateFreeSpin`, `updateGlobalMult`,
`freeSpinEnd`, `finalWin`, `wincap`.

Bespoke event (this game only), emitted on each kill during Revenge Spins:

```jsonc
{ "index": 17, "type": "smileState", "kills": 2, "state": "smirk", "multiplier": 3 }
```

- `kills`      — total kills this Revenge run
- `state`      — `grim | faint | smirk | grin | evil` → portrait + caption
- `multiplier` — KILL MULTIPLIER now in force (matches the following `updateGlobalMult`)

Frontend types + maps: `web-sdk/apps/tombstone-reborn/src/game/` (`types.ts`
`SmileStateEvent`, `constants.ts` `SMILE_FACE_MAP` / `KILL_LADDER`).

---

## 6. Files

**Math** — `math-sdk/games/0_3_tombstone_reborn/`
(`game_config.py`, `gamestate.py`, `game_override.py`, `game_executables.py`,
`game_events.py`, `game_calculations.py`, `game_optimization.py`, `run.py`,
`run_local.py`, `make_storybook_books.py`, `reels/`).

**Frontend config layer** — `web-sdk/apps/tombstone-reborn/src/game/`
(`config.ts`, `board.generated.ts`, `types.ts`, `constants.ts`, `assets.ts`).

Art/animation deliverables: `ASSET_CHECKLIST_TOMBSTONE_REBORN.md`.
