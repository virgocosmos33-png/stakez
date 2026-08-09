"""TOMBSTONE REBORN - 6-reel variable-height WAYS game (EXTREME volatility).

He died. He came back. This build layers a from-scratch special system on top
of a ways board. Nothing here is copied from The White Room - it is only used
as a reference for how the engine plumbs custom events.

Board:            3 | 4 | 4 | 2 | 2 | 1      (num_rows per reel)
Premiums:         H1 Gunslinger, H2 Duchess, H3 Butcher,
                  H4 Card Shark, H5 Preacher
Lows (L1-L5):     bullet, whiskey, spur, horseshoe, playing card
Wild  (W):        the revolver (substitutes; pays only on a full 6-wide line)

THE SPECIAL BAR (top row of 6 cells, one above each reel column). Each cell can
drop a card that fires a BOARD-WIDE effect. It is nearly dead in the base game
(specials appear "very rarely"), fully active in the Small Bonus and Super
Bonus. Cards (never paying symbols themselves):
  SPLIT-GANG    (+ways to EVERY premium on the board)
  SPLIT-OUTLAWS (+ways to EVERY low on the board)
  GUNSMOKE      (turn one whole symbol type into WILDs)
  DIG UP        (unlock the last-reel lane for this spin - even in base)
  TOMBSTONE OPEN(grow the short reels taller, revealing extra symbols)

THE LAST-REEL LANE (reel index 5, the 1-high column). Locked normally; opened
by DIG UP, and permanently open in the Super Bonus. When open it drops:
  BOUNTY     (a random premium lands there carrying a WIN multiplier)
  NUDGE      (a bounty premium slides left, +WIN-mult for each premium passed)
  SUPERSPLIT (reel 5 turns wild AND every paying symbol on the board is split)

MULTIPLIERS - two distinct kinds:
  WAYS mult  = split/gunsmoke fold into the ways COUNT (engine "symbol" strat).
  WIN  mult  = bounty/nudge multiply the whole spin's win at the very end.

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
        # the extreme tail comes from split/gunsmoke exploding the ways COUNT and
        # bounty/nudge stacking a WIN multiplier on top - not from fat base pays.
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
        # "wild" flags the revolver; "multiplier" is an (empty) category so the
        # reveal/board events serialize the per-cell ways multiplier that splits
        # stamp onto ordinary symbols. No symbol carries the multiplier flag by
        # default - it is assigned at runtime.
        self.special_symbols = {"wild": ["W"], "multiplier": []}

        # No free spins - single enhanced spins only. Kept defined so any engine
        # lookups that expect the keys don't crash; the custom draw never uses
        # them.
        self.freespin_triggers = {self.basegame_type: {}, self.freegame_type: {}}
        self.anticipation_triggers = {self.basegame_type: 99, self.freegame_type: 99}

        # ---- SPECIAL BAR (top cards) ----------------------------------------
        # cells: how many bar cells (one above each of the first `cells` reels).
        # weights[<mode>]: per-cell content distribution. "base" is nearly dead.
        self.special_bar_config = {
            "cells": 6,
            "weights": {
                "off": {"none": 1},
                "base": {
                    "none": 985, "split_gang": 4, "split_outlaws": 4,
                    "gunsmoke": 3, "digup": 1, "coffin": 3,
                },
                "small": {
                    "none": 56, "split_gang": 14, "split_outlaws": 14,
                    "gunsmoke": 8, "digup": 2, "coffin": 6,
                },
                "super": {
                    "none": 26, "split_gang": 22, "split_outlaws": 18,
                    "gunsmoke": 12, "digup": 10, "coffin": 12,
                },
            },
        }

        # ---- LAST-REEL LANE (reel 5) ----------------------------------------
        self.last_reel_config = {
            "weights": {
                "locked": {"none": 1},
                "unlocked": {"none": 22, "bounty": 34, "nudge": 28, "supersplit": 16},
            },
            # which premium the bounty/nudge lands (weighted toward weaker prems)
            "premium_weights": {"H5": 26, "H4": 20, "H3": 15, "H2": 10, "H1": 6},
            # the WIN multiplier the bounty premium carries
            "bounty_mult_weights": {2: 40, 3: 26, 5: 16, 10: 9, 25: 5, 50: 3, 100: 1},
            # nudge slides across the 5 columns left of the lane; each premium it
            # passes adds this much to the WIN multiplier
            "nudge_add_per_premium": 1,
        }

        # ---- FEATURE TUNING --------------------------------------------------
        # split factors are ADDED to each affected cell's ways multiplier
        self.split_config = {
            "gang_weights": {1: 40, 2: 26, 3: 16, 5: 10, 8: 5, 10: 3},
            "outlaw_weights": {1: 45, 2: 26, 3: 16, 5: 8, 8: 3, 10: 2},
            "cell_cap": 30,
        }
        self.gunsmoke_config = {
            "source_weights": {
                "L5": 16, "L4": 14, "L3": 13, "L2": 12, "L1": 11,
                "H5": 9, "H4": 7, "H3": 6, "H2": 5, "H1": 4,
            },
        }
        self.coffin_config = {
            "target_rows": 4,
            "grow_weights": {1: 46, 2: 30, 3: 16, 4: 8},
        }
        self.supersplit_config = {
            "all_ways_weights": {2: 40, 3: 28, 5: 18, 8: 9, 10: 5},
        }

        # ---- Reels -----------------------------------------------------------
        self.reels = {}
        for name in ("BR0", "WCAP"):
            self.reels[name] = self.read_reels_csv(os.path.join(self.reels_path, f"{name}.csv"))
        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["BR0"]

        # ---- Distribution condition builders --------------------------------
        def cond(reel="BR0", bar="off", last=False, count=0, boost="none",
                 force_wincap=False):
            return {
                "reel_weights": {self.basegame_type: {reel: 1}},
                "force_wincap": force_wincap,
                "force_freegame": False,
                "bar_mode": bar,
                "last_unlocked": last,
                "force_special_count": count,
                "boost": boost,
            }

        self.mode_rtps = {"base": 0.965, "bonus_small": 0.965, "bonus_super": 0.965}

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
                    Distribution(
                        criteria="basegame",
                        quota=0.549,
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
                        criteria="0",
                        quota=0.20,
                        win_criteria=0.0,
                        conditions=cond(reel="BR0", bar="super", last=True, count=6),
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.798,
                        conditions=cond(reel="BR0", bar="super", last=True, count=6),
                    ),
                ],
            ),
        ]
