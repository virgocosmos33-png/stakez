# Stake Engine — Compliance & Approval Reference

Distilled from the official docs at https://stake-engine.com/docs (full-page screenshots
of every docs page live in `docs_screenshots/shots/`, one PNG per URL). This is the
checklist our game must satisfy to get approved and stay published.

Last verified against the docs: 2026-07-17.

---

## 1. Review process (Submission Checklist)

- Three independent reviewers rate the game **0–3 stars** each, across design, gameplay,
  and math compliance. Ratings hidden until all three submit.
- **Average >= 1 star -> approved** for production. Average < 1 star -> rejected (can resubmit
  after addressing feedback).
- Review can take a couple of hours if clean; incomplete/non-compliant submissions can
  take weeks and get deprioritised.

### Quality ranking consequences (Game Quality Rankings)
- 3 stars: featured placement, Burst Games / Stake Exclusives eligibility.
- 2 stars: can appear in Burst Games / Exclusives if popular.
- 1 star: **not published** — asked to resubmit after improvements.
- Common causes of low ratings: shallow gameplay (players quit after 1–2 bets),
  **over-reliance on generic AI-generated assets** (standard fonts, gradients, emoji icons
  are explicitly called out), inconsistent visual design, missing engaging features.
- A 3-star game: tested on a range of devices, optimised bundle size, clean animations
  and art, in-depth concept.

## 2. Math verification — hard numeric limits

### File size (fails publish outright)
- No single events file (`.jsonl.zst`) over **4.2 GB**.
- No game mode with more than **10,000,000 events**.

### Summary statistics (reviewed for every mode)
- Mode cost correctly represented in game rules.
- **RTP must be within 90.00%–96.70%**, and all modes within **0.5%** of each other.
- Max win must match the game rules description for each mode.
- Max win must be **realistically obtainable** — typically more frequent than
  **1 in 10,000,000** (depends on payout amount).
- Run **100,000–1,000,000 sims per mode** for outcome diversity (avoid repeats in a session).
- A reasonable portion of sims must pay: **~90% non-paying may be grounds for rejection**.
- The most likely single simulation must not be overwhelmingly dominant.
- Non-zero-win hit rate should be **< 1 in 20 bets or more frequent** (i.e. >= 5% of spins pay).
- Base mode (1x cost) standard deviation within industry norms; no zero-weight-payout
  domination; no un-obtainable gaps between intermediate wins and the max payout.

### Risk limits by star tier
| Limit | 2-star | 3-star |
|---|---|---|
| Maximum Exposure | $10,000,000 | $50,000,000 |
| **Maximum Payout Multiplier** | **25,000x** | **100,000x** |
| Maximum Bet Cost | $100,000 | $500,000 |
| Maximum Cost Multiplier (buy modes) | 1,000x | 1,500x |
| Base (1x) std dev min | 0.6 | 0.6 |
| Base (1x) std dev max | 50.0 | 60.0 |
| P(>=5000x) / P(>=10000x) | 1e-2 / 8e-2 | 1e-2 / 2e-2 |
| Risk Limits (CVaR) | 700 | 800 |
| Liability (ETL, >40x bet) | 0.8 | 0.9 |
| Liability (ETL, P>=10000) | 0.6 | 0.8 |

- RGS hard-caps any bet size at **$500,000 USD** (error 400 beyond that).
- **P(>=5000)/P(>=10000) cost scaling** (high-cost modes get leniency): worst case across
  all modes is used, but measured probability is scaled first:
  - cost >= 1000x -> probability x 0.2
  - 500 <= cost < 1000 -> x 0.5
  - 200 <= cost < 500 -> x 0.8
- **CVaR** = expected payout in the worst 0.1% of outcomes. Two variants considered:
  normalized (CVaR / bet cost) and un-normalized (absolute).
- **ETL** = proportion of total RTP concentrated in wins >= 40x cost-multiplier (or >10,000x).
  Normalized ETL 0.5 means half the game's RTP comes from those tail wins.

## 3. Frontend requirements (Frontend and Communication)

### Game display
- **Unique audio and visual assets** — the web-sdk sample assets will NOT be approved.
- No visual bugs, broken/missing assets or animations.
- Must support Stake's **mini-player popout** (game keeps working scaled down).
- Must support **mobile view** with all UI functional during screen scaling.
- All images and fonts must load from the **Stake Engine CDN**.

### Rules and paytable (in-game info popup)
- Detailed description of all game rules accessible from the UI.
- Cost of each bet mode + what's being purchased described.
- **RTP of the game (and each mode) clearly communicated.**
- **Max win amount for each mode clearly displayed.**
- Payout amounts for all symbol combinations presented.
- All obtainable special-symbol values listed (multipliers etc.).
- Feature trigger descriptions, e.g. "3 Scatters award 10 free spins; 4 Scatters award 15…".

### UI components
- UI guide describing every button.
- Player can change bet size; all bet levels from RGS auth response usable.
- Current balance displayed.
- Final win clearly shown for non-zero results.
- Multi-action outcomes: payout must **incrementally update** to the final multiplier.
- Sound-disable option required.
- **Spacebar must map to the bet button.**
- Autoplay must be player-confirmed — no automatic consecutive bets from one click.

### Other checks
- No console/network errors or leaked game info in the network tab.
- Game tested against its own stated rules, various currencies/languages.
- "Fastplay" mode must still show legible win info.

## 4. Jurisdiction requirements (stake.us social casino)

US requirements prohibit gambling terms. RGS passes `social=true/false` query param;
recommended to keep a `sweeps_<lang>` language file. Banned words -> replacements
(full table in `docs_screenshots/shots/docs_approval-guidelines_jurisdiction-requirements.png`):

- bet -> play, total bet -> total play, betting -> playing
- buy / purchase / bought -> play / instantly triggered
- **buy bonus -> bonus / feature**, gamble/wager -> play
- cash / money -> coins, currency -> token, fund -> balance
- pay out / paid out / pays out -> win / won
- stake -> play amount, credit -> balance, rebet -> respin
- deposit -> get coins, withdraw -> redeem

## 5. Game tile assets (submission requirement)

- `GameTitle-BG.png/jpg` — environmental background of the game world.
- `GameTitle-FG.png` — feature character/key item, transparent background.
- `ProviderName-Logo.png` — studio logo, transparent, legible small.
- BG + FG combined must not exceed **3 MB**.

## 6. Required game disclaimer (info popup)

Template (or equivalent message):
> "Malfunction voids all wins and plays. A consistent internet connection is required. In
> the event of a disconnection, reload the game to finish any uncompleted rounds. The
> expected return is calculated over many plays. The game display is not representative of
> any physical device and is for illustrative purposes only. Winnings are settled according
> to the amount received from the Remote Game Server and not from events within the web
> browser."

## 7. Bet Replay (new games — approval requirement)

- Bet Replay support is **mandatory for new game approvals**.
- Frontend reads query parameters and fetches replay data from an RGS endpoint; during
  replay the game plays the round non-interactively (no balance, no bet controls),
  "Play the round as normal" -> show final result. Player sessions are NOT required.

## 8. RGS / integration facts

- Session auth + bet transactions exclusively through the RGS; frontend never computes money.
- Bet-level verification: RGS `/authenticate` response returns valid bet levels; frontend
  must respect them.
- Strict XSS policy — game build must contain only static files, no external sources.
- English-only build is acceptable (on-screen text hardcoded is fine if language params ignored).
- ~40 supported currencies incl. USD, EUR, JPY, BTC-style display handled by Stake.

## 9. Payments (business, not review)

- Option 1: **10% GGR revenue share** (negative months carry forward as debt).
- Option 2: **7.5% guaranteed** on expected GGR from RTP (no debt, stable).
- Payouts monthly from $0.01, wallet per team.

---

## 10. Madam Mirror — current status vs. these rules

Measured from the 2026-07-17 full run (`math-sdk/games/0_1_madam_mirror/library/stats_summary.json`):

| Check | Limit | Ours | Status |
|---|---|---|---|
| RTP within 90–96.7%, modes within 0.5% | 90.0–96.70% | 0.965 all 4 modes | OK |
| Events per mode | <= 10M | 200k / 50k / 50k / 50k | OK |
| Sims per mode | 100k–1M | 200k base, 50k buys | base OK; buys a bit low, consider 100k |
| Zero-win portion (base) | ~<= 90% | 74.5% | OK |
| Non-zero hit rate (base) | >= 1 in 20 | 1 in 3.93 | OK |
| Base std dev | 0.6–50 (2-star) | 14.68 | OK |
| Max win obtainable | > 1 in 10,000,000 | 1 in 10,000,004 (base) | BORDERLINE — bump wincap quota |
| **Max payout multiplier** | **25,000x (2-star)** / 100,000x (3-star) | **30,000x** | RISK — needs 3-star rating, or reduce cap to 25,000x |
| Max cost multiplier | 1,000x (2-star) | bonus3 = 1,000x | at the limit, OK |
| P(>=5000x) bonus3 (scaled x0.2 for 1000x cost) | <= 1e-2 | 0.0119*0.2 = 0.0024 | OK with scaling |
| P(>=10000x) bonus3 (scaled) | <= 2e-2 | 0.0071*0.2 = 0.0014 | OK with scaling |
| CVaR normalized (CVaR/cost) | 700–800 | base 203, b1 12, b2 20, b3 30 | OK normalized; local checker flags raw values |
| ETL | 0.8–0.9 | local numbers (4.3, 184) are not proportions — recompute per docs definition | VERIFY |

Note: `utils/rgs_verification.py` (our local checker) appears to compare **un-normalized**
CVaR and a different ETL formula than the docs describe (docs: proportion of RTP, 0–1).
The docs' cost-scaled/normalized interpretations are considerably more lenient for buy
modes. Confirm against Stake's actual reviewer tooling before panicking about the flags.

### Frontend gaps to close before submission (apps/ways)
- [ ] In-game rules popup: rules, per-mode RTP + max win, full paytable, feature triggers.
- [ ] Disclaimer text (section 6) in the info popup.
- [ ] UI guide for buttons; spacebar = bet; sound toggle; autoplay confirmation.
- [ ] Incremental win counter matching final payout on multi-event rounds.
- [ ] Mini-player popout + mobile scaling audit.
- [ ] Bet Replay support.
- [ ] `sweeps_<lang>` wording file (no "bet/buy/cash/stake" strings) for stake.us.
- [ ] Game tile assets: BG, FG, provider logo (<= 3MB combined).
- [ ] All assets unique (ours are — generated art, no sample-game assets).
