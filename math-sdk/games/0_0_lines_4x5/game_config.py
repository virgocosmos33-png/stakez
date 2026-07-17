"""Game-specific configuration file, inherits from src/config/config.py"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "0_0_lines_4x5"
        self.provider_number = 0
        self.working_name = "Lines 4x5 Game"
        self.wincap = 5000.0
        self.win_type = "lines"
        self.rtp = 0.9670
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [4] * self.num_reels
        # Board and Symbol Properties
        self.paytable = {
            (5, "W"): 50,
            (4, "W"): 20,
            (3, "W"): 10,
            (5, "H1"): 50,
            (4, "H1"): 20,
            (3, "H1"): 10,
            (5, "H2"): 15,
            (4, "H2"): 5,
            (3, "H2"): 3,
            (5, "H3"): 10,
            (4, "H3"): 3,
            (3, "H3"): 2,
            (5, "H4"): 8,
            (4, "H4"): 2,
            (3, "H4"): 1,
            (5, "L1"): 5,
            (4, "L1"): 1,
            (3, "L1"): 0.5,
            (5, "L2"): 3,
            (4, "L2"): 0.7,
            (3, "L2"): 0.3,
            (5, "L3"): 3,
            (4, "L3"): 0.7,
            (3, "L3"): 0.3,
            (5, "L4"): 2,
            (4, "L4"): 0.5,
            (3, "L4"): 0.2,
            (5, "L5"): 1,
            (4, "L5"): 0.3,
            (3, "L5"): 0.1,
        }

        # 50 paylines defined for a 5-reel, 4-row grid (row indices 0-3)
        self.paylines = {
            1: [0, 0, 0, 0, 0],
            2: [1, 1, 1, 1, 1],
            3: [2, 2, 2, 2, 2],
            4: [3, 3, 3, 3, 3],
            5: [0, 1, 2, 1, 0],
            6: [3, 2, 1, 2, 3],
            7: [1, 2, 3, 2, 1],
            8: [2, 1, 0, 1, 2],
            9: [0, 0, 1, 0, 0],
            10: [3, 3, 2, 3, 3],
            11: [1, 0, 0, 0, 1],
            12: [2, 3, 3, 3, 2],
            13: [0, 1, 0, 1, 0],
            14: [3, 2, 3, 2, 3],
            15: [1, 2, 1, 2, 1],
            16: [2, 1, 2, 1, 2],
            17: [0, 1, 1, 1, 0],
            18: [3, 2, 2, 2, 3],
            19: [1, 0, 1, 0, 1],
            20: [2, 3, 2, 3, 2],
            21: [0, 0, 0, 1, 2],
            22: [3, 3, 3, 2, 1],
            23: [2, 1, 0, 0, 0],
            24: [1, 2, 3, 3, 3],
            25: [0, 1, 2, 3, 3],
            26: [3, 2, 1, 0, 0],
            27: [0, 0, 1, 2, 3],
            28: [3, 3, 2, 1, 0],
            29: [1, 1, 0, 1, 1],
            30: [2, 2, 3, 2, 2],
            31: [1, 1, 2, 1, 1],
            32: [2, 2, 1, 2, 2],
            33: [0, 2, 0, 2, 0],
            34: [3, 1, 3, 1, 3],
            35: [1, 3, 1, 3, 1],
            36: [2, 0, 2, 0, 2],
            37: [0, 2, 1, 2, 0],
            38: [3, 1, 2, 1, 3],
            39: [1, 0, 2, 0, 1],
            40: [2, 3, 1, 3, 2],
            41: [0, 3, 0, 3, 0],
            42: [3, 0, 3, 0, 3],
            43: [1, 2, 2, 2, 1],
            44: [2, 1, 1, 1, 2],
            45: [0, 1, 3, 1, 0],
            46: [3, 2, 0, 2, 3],
            47: [0, 3, 3, 3, 0],
            48: [3, 0, 0, 0, 3],
            49: [1, 1, 3, 1, 1],
            50: [2, 2, 0, 2, 2],
        }

        self.include_padding = True
        self.special_symbols = {"wild": ["W"], "scatter": ["S"], "multiplier": ["W"]}

        # xNudge-style feature: a full stack of wilds lands misaligned on one reel,
        # nudges down into view, and each nudge step adds +1x to the wild multiplier.
        self.nudge_config = {
            # chance that a spin turns into a nudging wild-stack spin, per gametype
            "probability": {self.basegame_type: 0.05, self.freegame_type: 0.12},
            # reels allowed to hold the wild stack (middle reels, NLC-style)
            "allowed_reels": [1, 2, 3],
            # weighted number of nudge steps (also = extra multiplier gained)
            "nudge_weights": {1: 50, 2: 30, 3: 20},
        }

        self.freespin_triggers = {
            self.basegame_type: {3: 8, 4: 12, 5: 15},
            self.freegame_type: {2: 3, 3: 5, 4: 8, 5: 12},
        }
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }
        # Reels
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv", "WCAP": "FRWCAP.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]
        self.padding_symbol_values = {"W": {"multiplier": {2: 100, 3: 50, 4: 50, 5: 50, 10: 30, 20: 20, 50: 5}}}

        freegame_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            "scatter_triggers": {3: 50, 4: 20, 5: 5},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {
                    2: 60,
                    3: 80,
                    4: 50,
                    5: 20,
                    10: 15,
                    20: 10,
                    50: 5,
                },
            },
            "force_wincap": False,
            "force_freegame": True,
        }

        basegame_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "mult_values": {self.basegame_type: {1: 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        wincap_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1, "WCAP": 5},
            },
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {2: 10, 3: 20, 4: 50, 5: 60, 10: 100, 20: 90, 50: 50},
            },
            "scatter_triggers": {4: 1, 5: 2},
            "force_wincap": True,
            "force_freegame": True,
        }

        zerowin_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {2: 100, 3: 80, 4: 50, 5: 20, 10: 10, 20: 5, 50: 1},
            },
            "force_wincap": False,
            "force_freegame": False,
        }

        mode_maxwins = {"base": 5000, "bonus": 5000}
        # Contains all game-logic simulation conditions
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=mode_maxwins["base"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwins["base"],
                        conditions=wincap_condition,
                    ),
                    Distribution(criteria="freegame", quota=0.1, conditions=freegame_condition),
                    Distribution(criteria="0", quota=0.4, win_criteria=0.0, conditions=zerowin_condition),
                    Distribution(criteria="basegame", quota=0.5, conditions=basegame_condition),
                ],
            ),
            BetMode(
                name="bonus",
                cost=100.0,
                rtp=self.rtp,
                max_win=mode_maxwins["bonus"],
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwins["bonus"],
                        conditions=wincap_condition,
                    ),
                    Distribution(criteria="freegame", quota=0.1, conditions=freegame_condition),
                ],
            ),
        ]
