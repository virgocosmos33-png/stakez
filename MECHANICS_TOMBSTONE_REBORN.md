# Tombstone Reborn — Mechanics Design (extreme-volatility build)

The base game is bait. ~**92% of base spins pay nothing**; the money lives in
rare special-symbol chain-reactions and the two buys. **Max win 99,999× is
reachable in every mode** (base, small bonus, super bonus).

Almost all of this reuses **White Room**'s proven math (`unlocked_slots`,
`wild_reel` board-growth, `split`, `clone`, per-cell event ordering,
`force_special_count` acceptance). New code is only the tombstone-specific
cards, the WIN-multiplier layer and the horizontal nudge.

---

## 1. Three board states (progressive unlock)

The board is the coffin: 6 reels, heights **3·4·4·2·2·1**. A reserved **special
bar sits on top** (the "top row" cards) and the **last reel (1×)** is the coffin
lid. What's unlocked defines the mode:

| Mode | Cost | Top bar | Last reel (1×) | Feel |
|---|---|---|---|---|
| **BASE** | 1× | LOCKED — a card drops **very rarely** per cell | locked (unless a Dig-Up card opens it) | extreme; ~92% dead |
| **SMALL BONUS** | 80× | **UNLOCKED**, specials drop often | locked | 40% return exactly 0; max win very rare |
| **SUPER BONUS** | 1000× (max buy) | UNLOCKED | **UNLOCKED** → nudge + supersplit + last-reel premium | 70% return < cost; max win less rare |

Reuse: this is White Room's `unlock_by_level` (bottom / right / left) re-cast as
(top-bar / last-reel). Base-game rare drops = WR `content_weights_base`.

---

## 2. The special symbols (cards that drop into the top bar)

These land in the top-bar cells (rare in base, frequent in bonus) and fire in a
fixed order, each with its own book event (WR `apply_features_in_order`).

| Card | Effect | Interconnect | Built from |
|---|---|---|---|
| **SPLIT — GANG** (premiums) | +ways to **every premium type** on the board | more premium ways → bigger base for a WIN-mult | WR `split` (target = all premiums, not one) |
| **SPLIT — OUTLAWS** (lows) | +ways to **every low type** on the board | fills ways cheaply; feeds combos | WR `split` (target = all lows) |
| **GUNSMOKE** (wildify) | converts one **symbol type → WILD** | wilds then substitute everywhere; stacks with splits on the wild column | WR `clone` but target = wild |
| **DIG UP** (open last cell) | unlocks the **last reel (1×)** for this spin, even in BASE | turns a 5-wide board into 6-wide → 6-of-a-kind possible; can then drop a premium | WR side-column unlock, gated to reel 5 |
| **TOMBSTONE OPEN** (coffin) | **reels grow taller** (2,2,1 rise toward 4,4,4…), revealing extra symbols | max ways balloons 192 → thousands; every later split/gunsmoke acts on a bigger board | WR `wild_reel` rise, generalized to grow real symbols |
| **SUPERSPLIT** *(super bonus only, last reel)* | converts the last reel to **WILD** *and* **splits ALL symbols** on the board | the single biggest tail-maker; only in super bonus | WR `split` over all types + wildify combined |

---

## 3. The last reel (coffin lid) — super bonus

Normally 1 cell. When unlocked (super bonus, or a Dig-Up in base) it becomes a
feature lane holding **only special symbols**:

- **Bounty drop** — a random **PREMIUM lands carrying a WIN MULTIPLIER** (×, on
  the final win — *not* ways).
- **HORIZONTAL NUDGE** — the last reel **slides left across the board**; for
  **every premium it passes over while sliding**, its WIN MULTIPLIER **increases**.
  So a board full of premiums (after a Split-Gang) makes the nudge pay enormously.
- **SUPERSPLIT** lives here too.

This is the one genuinely new subsystem (no WR analogue): a sliding reel that
accumulates a win multiplier from what it crosses.

---

## 4. WAYS multiplier vs WIN multiplier (they stack)

Two independent multiplier layers — this is the core of the interconnection:

- **WAYS multipliers** (Split, Gunsmoke wild-mults, Tombstone Open) grow the
  **ways count**. Engine handles this natively (`multiplier_strategy="symbol"`,
  the ways product).
- **WIN multiplier** (last-reel bounty premium, nudge) multiplies the **final win
  amount** (`apply_mult`, global). Applied *after* ways are evaluated.

```
total = (ways_win from paytable × ways)  ×  win_multiplier
```

A monster spin: Tombstone Open grows the board → Split-Gang fans every premium →
ways explode → Dig-Up opens the lid → Bounty premium lands with ×10 → nudge
slides left over 8 premiums, climbing to ×50 → the already-huge ways win is
multiplied ×50. That chain is the path to 99,999× — reachable, but rare.

---

## 5. Order of operations (fixed, per spin)

1. Reveal the reelstrip board.
2. **DIG UP** cells resolve → last reel unlocks (if any).
3. **TOMBSTONE OPEN** → reels grow taller (new symbols slide in).
4. **Bounty drop** on the (now open) last reel → premium + WIN mult.
5. **HORIZONTAL NUDGE** → slides left, accumulating WIN mult over premiums.
6. Evaluate WAYS.
7. **SPLIT / GUNSMOKE / SUPERSPLIT** modify ways → re-evaluate.
8. Apply the accumulated **WIN multiplier** → final total, clamp to 99,999×.

Each step emits its own event so the frontend animates them one-by-one (WR
already streams features this way).

---

## 6. Volatility / math targets

| Mode | Cost | Hard targets |
|---|---|---|
| base | 1× | ~**92% dead spins**, RTP ~96.4%, max win reachable (~1e-7) |
| small bonus | **80×** | **40% return exactly 0**, RTP 96.x×cost, max win very rare |
| super bonus | **1000×** | **70% return < cost**, RTP 96.x×cost, max win rare-but-real |
| all modes | — | **99,999× achievable** |

Extreme volatility comes from: rare base drops + multiplicative ways + a
separate WIN-multiplier layer + the nudge's premium-counting climb. The
optimizer shapes each mode's fence RTPs and the zero-quotas to hit the exact
dead-spin / zero-return numbers above.

---

## 7. Build order (staged — each stage is testable)

1. **Foundation**: adapt White Room math → 6-reel `3,4,4,2,2,1` board, retheme;
   top bar + SPLIT-GANG / SPLIT-OUTLAWS / GUNSMOKE / DIG-UP / TOMBSTONE-OPEN;
   BASE-mode rare drops → hit ~92% dead + extreme tail.
2. **Small bonus** buy (80×, top bar frequent, 40% exact-zero).
3. **Last-reel subsystem**: Bounty premium + WIN-multiplier layer + horizontal
   nudge + SUPERSPLIT.
4. **Super bonus** buy (1000×, 70% < cost).
5. **Tune**: lock every volatility target; verify 99,999× in all modes; full
   `run.py` optimize + RGS verification.

Frontend follows the same order (config layer already exists; components + the
book-event handlers for each card come as the math for each stage lands).

---

### Open questions before Stage 1
- **Approach**: build by **adapting White Room's `game_override.py`** wholesale
  (fastest — reuses split/board-grow/unlock/event-ordering), then cut+retheme?
  I recommend yes.
- **Retriggers / free-spin *spins*?** Your bonuses read as *single* super-charged
  spins (buy → one big board resolution), not N free spins. Confirm: are small/
  super bonus **one enhanced spin each**, or a short set of spins?
- **Nudge scope**: does the nudge slide the whole last reel across *all* 6
  columns (max climb), or a limited distance?
