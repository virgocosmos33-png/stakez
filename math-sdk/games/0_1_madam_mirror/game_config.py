"""Madam Mirror - game configuration.

5x4 dynamic-ways game ("xMirror"): Haunted Mirrors reflect a weighted 1-4 of
their neighboring cells into 2-4 apparitions, multiplying the ways count.
Three bonus levels differing by haunted-cell lifetime and stacking.
Wincap 30,000x.
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
        self.game_id = "0_1_madam_mirror"
        self.provider_name = "dramastudios"
        self.game_name = "madam_mirror"
        self.provider_number = 0
        self.working_name = "Madam Mirror"
        self.wincap = 30000.0
        self.win_type = "ways"
        self.rtp = 0.965
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [4] * self.num_reels

        # Paytable: pays per way (x bet), multiplied by the ways count.
        # All values are multiples of 0.1 - the RGS requires payout integers
        # in increments of 10 (win = pay x integer ways, so pays must comply).
        # Highs are the five characters, lows the playing-card ranks:
        #   H1 Lady Mirror, H2 The Wife, H3 The Man, H4 The Little Girl, H5 The Dog
        #   L1 Ace, L2 King, L3 Queen, L4 Jack, L5 Ten
        self.paytable = {
            (5, "H1"): 10, (4, "H1"): 3.0, (3, "H1"): 1.0,
            (5, "H2"): 5.0, (4, "H2"): 1.5, (3, "H2"): 0.6,
            (5, "H3"): 4.0, (4, "H3"): 1.2, (3, "H3"): 0.5,
            (5, "H4"): 3.0, (4, "H4"): 1.0, (3, "H4"): 0.4,
            (5, "H5"): 2.5, (4, "H5"): 0.8, (3, "H5"): 0.3,
            (5, "L1"): 1.2, (4, "L1"): 0.4, (3, "L1"): 0.2,
            (5, "L2"): 1.2, (4, "L2"): 0.4, (3, "L2"): 0.2,
            (5, "L3"): 0.8, (4, "L3"): 0.3, (3, "L3"): 0.1,
            (5, "L4"): 0.8, (4, "L4"): 0.3, (3, "L4"): 0.1,
            (5, "L5"): 0.8, (4, "L5"): 0.3, (3, "L5"): 0.1,
        }

        self.include_padding = True
        # Apparition counts ride on the engine's 'multiplier' symbol attribute:
        # in ways evaluation a symbol with multiplier=m counts as m symbols on
        # its reel (engine behaviour, multiplier_strategy="symbol").
        # "HM" is the Haunted Mirror; it never pays and resolves after the burst.
        # "ME" is the Madam's Eye; it never pays and resolves after conversion.
        # "ttl" is not a symbol - listing it makes the reveal serializer include
        # the remaining-lifetime attribute on persistent haunted cells
        # (2+ = reveals left, -1 = sticky for the whole bonus).
        self.special_symbols = {
            "wild": ["W"],
            "scatter": ["S"],
            "multiplier": [],
            "mirror": ["HM"],
            "eye": ["ME"],
            "ttl": [],
        }

        # Three bonus levels keyed by scatter count (base game),
        # retriggers award a flat +3 inside any level.
        self.freespin_triggers = {
            self.basegame_type: {3: 8, 4: 10, 5: 12},
            self.freegame_type: {2: 3, 3: 3, 4: 3, 5: 3},
        }
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }

        # Bonus level rules, applied per free spin by game_override.apply_mirrors:
        # - mirror_chance: per-spin mirror probability (every level beats the base 0.14)
        # - split_count_weights: surrounding cells a burst reflects, up to a full
        #   block of 6 (1 common .. 6 very rare), slightly more generous per level
        # - lifetime: reveals a haunted cell survives (1 = the spin it drops only,
        #   2 = that spin plus one more, None = sticky for the whole bonus)
        # - stacking: bursts hitting an already-haunted cell ADD apparitions with no
        #   cap and refresh the cell's lifetime; without it, re-hits keep the max
        self.bonus_levels = {
            1: {"name": "THE_SEANCE", "mirror_chance": 0.40, "split_count_weights": {1: 50, 2: 26, 3: 13, 4: 7, 5: 3, 6: 1}, "lifetime": 1, "stacking": False},
            2: {"name": "THE_OTHER_SIDE", "mirror_chance": 0.45, "split_count_weights": {1: 45, 2: 27, 3: 15, 4: 8, 5: 4, 6: 2}, "lifetime": 2, "stacking": True},
            3: {"name": "BLOOD_MOON", "mirror_chance": 0.50, "split_count_weights": {1: 40, 2: 28, 3: 16, 4: 9, 5: 5, 6: 2}, "lifetime": None, "stacking": True},
        }
        self.scatter_to_level = {3: 1, 4: 2, 5: 3}

        # xMirror feature configuration (base game; free spins take the trigger
        # chance and split weights from bonus_levels instead).
        self.mirror_config = {
            # chance a base-game spin gets mirrors at all
            "probability": {self.basegame_type: 0.14},
            # number of mirrors, given the spin has mirrors: multi-mirror drops
            # are the base game's natural path to the wincap (~1 in 10M spins)
            "mirror_count_weights": {1: 80, 2: 17, 3: 3},
            # reels allowed to hold a mirror (never the outer reels)
            "allowed_reels": [1, 2, 3],
            # how many surrounding cells a burst reflects in the base game
            "split_count_weights": {1: 52, 2: 26, 3: 12, 4: 6, 5: 3, 6: 1},
            # apparition count rolled per reflected neighbor cell
            "apparition_weights": {2: 60, 3: 30, 4: 10},
        }

        # The Madam's Eye ("ME"): a rare symbol that only drops on spins that
        # will have split symbols in play (a fresh mirror burst this spin, or
        # haunted cells carried over by persistence). When it lands, EVERY
        # split symbol on the board turns WILD for that spin, keeping its
        # apparition count; the eye itself resolves into a wild too. Haunted
        # cell persistence is untouched - the conversion lasts one spin only.
        self.eye_config = {
            "probability": {self.basegame_type: 0.05, self.freegame_type: 0.08},
        }

        # Reels
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv", "FRWCAP": "FRWCAP.csv", "BRWCAP": "BRWCAP.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        def wincap_condition(scatter_triggers):
            """Bonus wincap books ride wild-heavy FRWCAP reels; the scatter count
            must match the mode's bonus level (a bonus1 buy stays a level-1
            bonus). force_mirrors biases the search (mirrors on every spin, max
            mirror count, max split block, max apparitions) so 30,000x is
            actually reachable - level rules themselves are unchanged."""
            return {
                "reel_weights": {
                    self.basegame_type: {"BR0": 1},
                    self.freegame_type: {"FR0": 1, "FRWCAP": 8},
                },
                "force_wincap": True,
                "force_freegame": True,
                "force_mirrors": True,
                "scatter_triggers": scatter_triggers,
            }

        # base-mode wincap: a pure base-game blowout - multiple mirrors land on
        # one spin, each reflecting a block of up to 6 cells, exploding the ways.
        # Rides a dedicated wild/H1-heavy scatterless strip so the search can
        # actually find 30,000x boards; the optimizer weight makes it ~1 in 10M.
        base_wincap_condition = {
            "reel_weights": {self.basegame_type: {"BRWCAP": 1}},
            "force_wincap": True,
            "force_freegame": False,
            "force_mirrors": True,
        }

        zero_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        basegame_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        def freegame_condition(scatter_triggers):
            return {
                "reel_weights": {
                    self.basegame_type: {"BR0": 1},
                    self.freegame_type: {"FR0": 1},
                },
                "force_wincap": False,
                "force_freegame": True,
                "scatter_triggers": scatter_triggers,
            }

        mode_maxwin = 30000

        # per-mode RTP tilt: buying a bonus returns more than base spinning.
        # Stake verification bounds: every mode in 90.0-96.7%, spread <= 0.5%
        self.mode_rtps = {
            "base": 0.962,
            "bonus1": 0.965,
            "bonus2": 0.966,
            "bonus3": 0.9665,
            # ante: same per-cost RTP as base; the 0.25x surcharge buys DOUBLE
            # the bonus trigger rate (1 in 109 vs 1 in 218), paid for by both
            # the surcharge and a ~33% thinner base-spin win contribution
            "ante": 0.962,
            # feature spins: guaranteed mirrors, priced off the measured
            # conditional EVs (8.26x / 19.87x / 38.84x at 96.5%)
            "feature1": 0.965,
            "feature2": 0.965,
            "feature3": 0.965,
        }

        # ANTE: every base spin shows a scatter on reel 1 (game_override
        # injects it post-draw). Trigger then needs just 2+ scatters elsewhere.
        def ante_condition(base_condition):
            condition = dict(base_condition)
            condition["force_scatter_reel"] = 0
            return condition

        # FEATURE SPINS: the base spin is guaranteed to land N+ mirrors
        # (mirror count still drawn from the natural weights, truncated at N).
        def mirror_condition(base_condition, min_mirrors):
            condition = dict(base_condition)
            condition["force_mirror_min"] = min_mirrors
            return condition

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.mode_rtps["base"],
                max_win=mode_maxwin,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwin,
                        conditions=base_wincap_condition,
                    ),
                    # NLC profile: most of the RTP lives in the bonuses
                    Distribution(
                        criteria="freegame",
                        quota=0.08,
                        conditions=freegame_condition({3: 100, 4: 25, 5: 6}),
                    ),
                    Distribution(criteria="0", quota=0.549, win_criteria=0.0, conditions=zero_condition),
                    Distribution(criteria="basegame", quota=0.37, conditions=basegame_condition),
                ],
            ),
            BetMode(
                name="ante",
                cost=1.25,
                rtp=self.mode_rtps["ante"],
                max_win=mode_maxwin,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwin,
                        conditions=ante_condition(base_wincap_condition),
                    ),
                    # double trigger rate: more freegame books in the pool,
                    # weighted to land at 1-in-109 by the optimizer
                    Distribution(
                        criteria="freegame",
                        quota=0.14,
                        conditions=ante_condition(freegame_condition({3: 100, 4: 25, 5: 6})),
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.539,
                        win_criteria=0.0,
                        conditions=ante_condition(zero_condition),
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.32,
                        conditions=ante_condition(basegame_condition),
                    ),
                ],
            ),
            BetMode(
                name="feature1",
                cost=10.0,
                rtp=self.mode_rtps["feature1"],
                max_win=mode_maxwin,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwin,
                        conditions=mirror_condition(base_wincap_condition, 1),
                    ),
                    # natural bonus triggers still happen on mirror spins (~1.2%)
                    Distribution(
                        criteria="freegame",
                        quota=0.02,
                        conditions=mirror_condition(freegame_condition({3: 100, 4: 25, 5: 6}), 1),
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.979,
                        conditions=mirror_condition(basegame_condition, 1),
                    ),
                ],
            ),
            BetMode(
                name="feature2",
                cost=20.0,
                rtp=self.mode_rtps["feature2"],
                max_win=mode_maxwin,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwin,
                        conditions=mirror_condition(base_wincap_condition, 2),
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.02,
                        conditions=mirror_condition(freegame_condition({3: 100, 4: 25, 5: 6}), 2),
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.979,
                        conditions=mirror_condition(basegame_condition, 2),
                    ),
                ],
            ),
            BetMode(
                name="feature3",
                cost=40.0,
                rtp=self.mode_rtps["feature3"],
                max_win=mode_maxwin,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwin,
                        conditions=mirror_condition(base_wincap_condition, 3),
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.02,
                        conditions=mirror_condition(freegame_condition({3: 100, 4: 25, 5: 6}), 3),
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.979,
                        conditions=mirror_condition(basegame_condition, 3),
                    ),
                ],
            ),
            BetMode(
                name="bonus1",
                cost=100.0,
                rtp=self.mode_rtps["bonus1"],
                max_win=mode_maxwin,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwin,
                        conditions=wincap_condition({3: 1}),
                    ),
                    Distribution(criteria="freegame", quota=0.999, conditions=freegame_condition({3: 1})),
                ],
            ),
            BetMode(
                name="bonus2",
                cost=400.0,
                rtp=self.mode_rtps["bonus2"],
                max_win=mode_maxwin,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwin,
                        conditions=wincap_condition({4: 1}),
                    ),
                    Distribution(criteria="freegame", quota=0.999, conditions=freegame_condition({4: 1})),
                ],
            ),
            BetMode(
                name="bonus3",
                cost=1000.0,
                rtp=self.mode_rtps["bonus3"],
                max_win=mode_maxwin,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    # the cap hits ~1 in 200 buys here: extra book variety needed
                    Distribution(
                        criteria="wincap",
                        quota=0.004,
                        win_criteria=mode_maxwin,
                        conditions=wincap_condition({5: 1}),
                    ),
                    Distribution(criteria="freegame", quota=0.996, conditions=freegame_condition({5: 1})),
                ],
            ),
        ]
