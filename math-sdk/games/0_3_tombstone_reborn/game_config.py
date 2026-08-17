"""TOMBSTONE REBORN - 6-reel variable-height WAYS game (EXTREME volatility).

He died. He came back. This build layers a from-scratch special system on top
of a ways board. Nothing here is copied from The White Room - it is only used
as a reference for how the engine plumbs custom events.

Board:            3 | 4 | 4 | 2 | 2 | 1      (num_rows per reel)
Premiums:         H1 Gunslinger, H2 Duchess, H3 Butcher,
                  H4 Card Shark, H5 Preacher
Lows (L1-L5):     bullet, whiskey, spur, horseshoe, playing card
Wild  (W):        the revolver (substitutes; pays only on a full 6-wide line)

FEATURE SYMBOLS land ON THE BOARD (no left special bar). After they fire they
transform into the revolver WILD. Nearly dead in the base game; awake in the
Small Bonus and Super Bonus:
  SP SPLIT          (pick 1 symbol type, add 2-7 ways to every copy;
                     also doubles a standing NUDGE stack)
  GS GUNSMOKE       (turn one whole symbol type into WILDs;
                     cannot hit a NUDGE stack or the rows it already ate)
  NW NUDGE WAYS     (reels 2-3 only: fires first, nudges down doubling ways)
  SU SUPER SCATTER  (4th scatter / upgrade; also opens the last reel this spin)

THE LAST-REEL LANE (reel index 5, the 1-high column). Locked normally; opened
when a SUPER scatter lands, and permanently open in the Super Bonus / big
bonus round. When open it drops ONLY:
  a PREMIUM carrying extra WAYS (no lows, ever — not a WIN multiplier)
  SH MARK     (shoots every premium; +1 WIN multi when it triggers)
  SS SUPERSPLIT (reel 5 turns wild AND every symbol on the board is split; +1 WIN multi)

MULTIPLIERS - two distinct kinds:
  WAYS mult  = split / nudge-ways / supersplit / last-reel premium fold into the ways COUNT.
  WIN  mult  = a separate HUD stack. +1 per split, per gunsmoke shot, per
               nudge-down step, and +1 each time MARK or SUPERSPLIT triggers.
               Sticky across the SUPER / big bonus round; reset each SMALL bonus spin.

MODES (all single enhanced spins, all can reach the 99,999x cap):
  base         1x     bar nearly dead, last lane locked, ~92% dead spins
  bonus_small  80x    bar unlocked, last lane locked, ~40% return exactly 0
  bonus_super  1000x  bar + last lane unlocked, 6 specials guaranteed
"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Game specific configuration class."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "0_3_tombstone_reborn"
        self.provider_name = "dramastudios"
        self.game_name = "tombstone_reborn"
        self.provider_number = 0
        self.working_name = "TOMBSTONE REBORN"
        self.wincap = 99999.0
        self.win_type = "ways"
        self.rtp = 0.965
        self.construct_paths()

        # Game Dimensions - variable column heights
        self.num_reels = 6
        self.num_rows = [3, 4, 4, 2, 2, 1]

        # WAYS paytable (per-way x bet). Per-way values are intentionally small:
        # the extreme tail comes from split/gunsmoke exploding the ways COUNT,
        # last-reel premium WAYS, and the stacked WIN multiplier on top - not
        # from fat base pays.
        self.paytable = {
            (6, "W"): 10.0,
            (6, "H1"): 5.0, (5, "H1"): 1.5, (4, "H1"): 0.5, (3, "H1"): 0.2,
            (6, "H2"): 3.0, (5, "H2"): 1.0, (4, "H2"): 0.4, (3, "H2"): 0.2,
            (6, "H3"): 2.5, (5, "H3"): 0.8, (4, "H3"): 0.3, (3, "H3"): 0.1,
            (6, "H4"): 2.0, (5, "H4"): 0.6, (4, "H4"): 0.3, (3, "H4"): 0.1,
            (6, "H5"): 1.5, (5, "H5"): 0.5, (4, "H5"): 0.2, (3, "H5"): 0.1,
            (6, "L1"): 1.0, (5, "L1"): 0.4, (4, "L1"): 0.2, (3, "L1"): 0.1,
            (6, "L2"): 1.0, (5, "L2"): 0.4, (4, "L2"): 0.2, (3, "L2"): 0.1,
            (6, "L3"): 0.8, (5, "L3"): 0.3, (4, "L3"): 0.1, (3, "L3"): 0.1,
            (6, "L4"): 0.8, (5, "L4"): 0.3, (4, "L4"): 0.1, (3, "L4"): 0.1,
            (6, "L5"): 0.6, (5, "L5"): 0.2, (4, "L5"): 0.1, (3, "L5"): 0.1,
        }

        self.paying_symbols = [
            "H1", "H2", "H3", "H4", "H5", "L1", "L2", "L3", "L4", "L5", "W",
        ]
        self.premium_symbols = ["H1", "H2", "H3", "H4", "H5"]
        self.low_symbols = ["L1", "L2", "L3", "L4", "L5"]
        self.wild_symbol = "W"

        self.include_padding = True
        # "wild" flags the revolver; "scatter" the coffin-plate bonus symbol S;
        # "multiplier" is an (empty) category so the reveal/board events
        # serialize the per-cell ways multiplier that splits stamp onto
        # ordinary symbols. No symbol carries the multiplier flag by default -
        # it is assigned at runtime.
        # feature symbols land on the board, fire, then become wild. "feature"
        # is serialized onto the reveal so the frontend can tell them apart.
        self.feature_symbols = ["SP", "GS", "NW", "SH", "SS"]
        self.special_symbols = {
            "wild": ["W"],
            "scatter": ["S", "SU"],
            "multiplier": [],
            "feature": list(self.feature_symbols),
        }

        # BONUS ROUNDS. 3 scatters trigger the SMALL BONUS (fs_spins spins, the
        # special bar awake on every spin), 4+ the BIG BONUS (same spins, the
        # grave lane PERMANENTLY open on top). Scatters live only on columns
        # 0-4 with strip spacing wider than any window, so counts are exact
        # per-column presence (max 5). No retriggers: the freegame strips (FR0
        # / WCAP) carry no S at all - the only scatter a round can ever show is
        # the 1-in-100 UPGRADE drop (see fs_upgrade_per_spin), which plants
        # the SUPER tombstone (SU) rather than another BONUS (S).
        self.fs_spins = 10
        # per-spin chance the small bonus drops its 4th scatter and upgrades to
        # the big bonus (lane open + spins topped back up): ~1 in 100 rounds
        self.fs_upgrade_per_spin = 0.001
        self.freespin_triggers = {
            self.basegame_type: {3: self.fs_spins, 4: self.fs_spins, 5: self.fs_spins},
            self.freegame_type: {},
        }
        self.anticipation_triggers = {self.basegame_type: 2, self.freegame_type: 99}

        # ---- SPECIAL BAR (top cards) ----------------------------------------
        # cells: how many bar cells (one above each of the first `cells` reels).
        # weights[<mode>]: per-cell content distribution. "base" is nearly dead.
        self.special_bar_config = {
            "cells": 6,
            "weights": {
                "off": {"none": 1},
                "base": {
                    "none": 985, "split": 7, "gunsmoke": 3, "nudge": 5,
                },
                "small": {
                    "none": 56, "split": 21, "gunsmoke": 8, "nudge": 15,
                },
                # the SMALL BONUS round bar: awake (a card most spins) but
                # diluted vs "small" - ten of these spins sell for 80x where
                # ONE "small" spin sells for 80x
                "wake": {
                    "none": 300, "split": 21, "gunsmoke": 8, "nudge": 15,
                },
                "super": {
                    "none": 26, "split": 33, "gunsmoke": 12, "nudge": 29,
                },
            },
        }

        # ---- LAST-REEL LANE (reel 5) ----------------------------------------
        # Unlocked lane NEVER drops lows. Only a premium (always with extra
        # WAYS on that cell) or one of the two lane specials: MARK / SUPERSPLIT.
        self.last_reel_config = {
            "drop_weights": {
                # single unlocked spin (bought super / super-scatter open): premiums dominate
                "unlocked": {"premium": 55, "shooter": 28, "supersplit": 17},
                # 10-spin big bonus: starve the two specials so most rounds stay
                # under cost (~25% of rounds profitable)
                "round": {"premium": 82, "shooter": 12, "supersplit": 6},
            },
            "premium_weights": {"H5": 26, "H4": 20, "H3": 15, "H2": 10, "H1": 6},
            # WAYS stamped on the last-reel premium cell (not the HUD WIN multi)
            "premium_ways_weights": {2: 40, 3: 26, 5: 16, 10: 9, 25: 5, 50: 3, 100: 1},
        }

        # ---- FEATURE TUNING --------------------------------------------------
        # SPLIT: pick ONE type on the board, ADD 2-7 ways to every copy.
        # Also doubles any standing NUDGE stack (nudge fires first).
        # Ways are extremely weighted toward the low end.
        self.split_config = {
            "count_weights": {1: 1},
            "ways_weights": {2: 140, 3: 32, 4: 16, 5: 8, 6: 3, 7: 1},
            "source_weights": {
                "L5": 16, "L4": 14, "L3": 13, "L2": 12, "L1": 11,
                "H5": 9, "H4": 7, "H3": 6, "H2": 5, "H1": 4, "W": 3,
            },
            "cell_cap": 99,
        }
        self.gunsmoke_config = {
            "source_weights": {
                "L5": 16, "L4": 14, "L3": 13, "L2": 12, "L1": 11,
                "H5": 9, "H4": 7, "H3": 6, "H2": 5, "H1": 4,
            },
        }
        # NUDGE WAYS: reels 1 and 2 only (the two 4-high columns). Initial ways
        # 2-9, extremely weighted toward 2. Lands on a row and nudges DOWN,
        # doubling the stack's ways each step — or drops as a full reel and
        # keeps the initial ways with no doubling.
        self.nudge_ways_config = {
            "reels": (1, 2),
            "initial_ways_weights": {
                2: 140, 3: 32, 4: 16, 5: 8, 6: 4, 7: 2, 8: 1, 9: 1,
            },
            "place_weights": {
                "full": 18,
                0: 15,
                1: 25,
                2: 32,
                3: 10,
            },
        }
        self.supersplit_config = {
            "all_ways_weights": {2: 55, 5: 32, 10: 13},
        }

        # ---- Reels -----------------------------------------------------------
        # BR0  base strip, sparse teaser scatters on columns 0-4
        # BRT  trigger strip, dense scatters - forced-freegame books draw here
        # FR0  freegame strip, NO scatters (rounds cannot retrigger)
        # WCAP wincap strip (no scatters)
        # (see reels/_add_scatters.py)
        self.reels = {}
        for name in ("BR0", "BRT", "FR0", "WCAP"):
            self.reels[name] = self.read_reels_csv(os.path.join(self.reels_path, f"{name}.csv"))
        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        # ---- Distribution condition builders --------------------------------
        # scatters: the base-spin scatter target for this book's criteria -
        #   "none" (redraw any accidental 3+), "exactly3" (small bonus trigger)
        #   or "atleast4" (big bonus trigger).
        # fs_*: how the bonus round's spins draw - bar mode, whether the grave
        #   lane is permanently open, which strip, and whether the 4th-scatter
        #   upgrade is forced onto spin 1 (wincap books: the small bonus can
        #   only reach the cap THROUGH the upgrade).
        def cond(reel="BR0", bar="off", last=False, count=0, boost="none",
                 force_wincap=False, force_freegame=False, scatters="none",
                 fs_reel="FR0", fs_bar="wake", fs_last=False,
                 fs_force_upgrade=False):
            return {
                "reel_weights": {
                    self.basegame_type: {reel: 1},
                    self.freegame_type: {fs_reel: 1},
                },
                "force_wincap": force_wincap,
                "force_freegame": force_freegame,
                "bar_mode": bar,
                "last_unlocked": last,
                "force_special_count": count,
                "boost": boost,
                "scatters": scatters,
                "fs_bar": fs_bar,
                "fs_last": fs_last,
                "fs_force_upgrade": fs_force_upgrade,
            }

        self.mode_rtps = {
            "base": 0.965,
            "bonus_small": 0.965,
            "bonus_super": 0.965,
            "freespins": 0.965,
            "superspins": 0.965,
        }

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.00,
                rtp=self.mode_rtps["base"],
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions=cond(reel="WCAP", bar="super", last=True, count=6,
                                        boost="max", force_wincap=True),
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.45,
                        win_criteria=0.0,
                        conditions=cond(reel="BR0", bar="base", last=False),
                    ),
                    # natural bonus triggers: 3 scatters -> SMALL BONUS round
                    # (bar awake), 4+ -> BIG BONUS round (lane open too)
                    Distribution(
                        criteria="freegame_small",
                        quota=0.02,
                        conditions=cond(reel="BRT", bar="base", scatters="exactly3",
                                        force_freegame=True,
                                        fs_bar="wake", fs_last=False),
                    ),
                    Distribution(
                        criteria="freegame_big",
                        quota=0.005,
                        conditions=cond(reel="BRT", bar="base", scatters="atleast4",
                                        force_freegame=True,
                                        fs_bar="wake", fs_last=True),
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.524,
                        conditions=cond(reel="BR0", bar="base", last=False),
                    ),
                ],
            ),
            BetMode(
                name="bonus_small",
                cost=80.00,
                rtp=self.mode_rtps["bonus_small"],
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions=cond(reel="WCAP", bar="super", last=False, count=6,
                                        boost="max", force_wincap=True),
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.40,
                        win_criteria=0.0,
                        conditions=cond(reel="BR0", bar="small", last=False),
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.599,
                        conditions=cond(reel="BR0", bar="small", last=False),
                    ),
                ],
            ),
            BetMode(
                name="bonus_super",
                cost=1000.00,
                rtp=self.mode_rtps["bonus_super"],
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.002,
                        win_criteria=self.wincap,
                        conditions=cond(reel="WCAP", bar="super", last=True, count=6,
                                        boost="max", force_wincap=True),
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.998,
                        conditions=cond(reel="BR0", bar="super", last=True, count=6),
                    ),
                ],
            ),
            # ---- BONUS ROUNDS (multi-spin, scatter-triggered, also buyable) --
            # SMALL BONUS: 3 scatters trigger fs_spins spins with the special
            # bar awake ("wake") every spin. 1 in ~100 rounds drops a 4th
            # scatter mid-round and UPGRADES to the big bonus (lane opens for
            # the rest, spins topped back up). The cap is only reachable
            # through that upgrade - wincap books force it on spin 1.
            BetMode(
                name="freespins",
                cost=80.00,
                rtp=self.mode_rtps["freespins"],
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.002,
                        win_criteria=self.wincap,
                        conditions=cond(reel="BRT", bar="base", scatters="exactly3",
                                        force_freegame=True, force_wincap=True,
                                        fs_reel="WCAP", fs_bar="super", fs_last=False,
                                        fs_force_upgrade=True, boost="max"),
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.998,
                        conditions=cond(reel="BRT", bar="base", scatters="exactly3",
                                        force_freegame=True,
                                        fs_bar="wake", fs_last=False),
                    ),
                ],
            ),
            # BIG BONUS: 4+ scatters trigger fs_spins spins with the bar awake
            # at the bought-small level AND the grave lane permanently open -
            # last-reel premium ways / MARK / supersplit live on every spin.
            BetMode(
                name="superspins",
                cost=2000.00,
                rtp=self.mode_rtps["superspins"],
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.002,
                        win_criteria=self.wincap,
                        conditions=cond(reel="BRT", bar="base", scatters="atleast4",
                                        force_freegame=True, force_wincap=True,
                                        fs_reel="WCAP", fs_bar="super", fs_last=True,
                                        boost="max"),
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.998,
                        conditions=cond(reel="BRT", bar="base", scatters="atleast4",
                                        force_freegame=True,
                                        fs_bar="wake", fs_last=True),
                    ),
                ],
            ),
        ]
