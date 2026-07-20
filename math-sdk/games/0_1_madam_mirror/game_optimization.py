"""Optimization parameters for Madam Mirror (NLC-style extreme volatility).

Base game is deliberately starved (~55% zero-win spins, base RTP share ~55%);
the rest of the RTP lives in the three bonus levels.

Wincap (30,000x) hit-rate targets per mode, NLC-profile:
  base   ~1 in 10,000,000 spins  (rtp 0.003 = 30000/1e7)
  bonus1 ~1 in 100,000 buys      (rtp 0.003 = 300x cost / 1e5)
  bonus2 ~1 in 7,500 buys        (rtp 0.010 = 75x cost / 7.5e3)
  bonus3 ~1 in 200 buys          (rtp 0.150 = 30x cost / 2e2)
bonus3 pays the cap often; the counterweight is a fat band of low/dud books
where stacked cells never connect into paying ways.
"""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    ConstructFenceBias,
    verify_optimization_input,
)


class OptimizationSetup:
    """Game specific optimization setup."""

    def __init__(self, game_config):
        self.game_config = game_config
        wincaps = {}
        for bm in game_config.bet_modes:
            wincaps[bm.get_name()] = bm.get_wincap()

        mode_rtps = game_config.mode_rtps

        def buy_mode_params(mode_name, test_spins, wincap_rtp):
            """Bonus buys share one shape: a wincap slice (sized per level) + freegame bulk."""
            return {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=wincap_rtp, av_win=wincaps[mode_name], search_conditions=wincaps[mode_name]
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=mode_rtps[mode_name] - wincap_rtp, hr="x"
                    ).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "freegame", "scale_factor": 0.9, "win_range": (20, 50), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 1.2, "win_range": (5000, 10000), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=10,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=test_spins,
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            }

        def feature_mode_params(cost, wincap_rtp, freegame_rtp):
            """Feature spins: one guaranteed-mirror base spin. Bulk of the RTP
            sits in the basegame fence; a thin freegame fence covers natural
            triggers landing on the mirror spin.

            NOTE: only ONE fence may use hr="x" (the optimizer assigns it the
            leftover probability). The freegame fence gets an explicit hit rate
            matching its 2% book quota, otherwise its RTP silently vanishes."""
            rtp_total = 0.965
            return {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=wincap_rtp, av_win=30000, search_conditions=30000
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=freegame_rtp, hr=50, search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(
                        rtp=rtp_total - wincap_rtp - freegame_rtp, hr="x"
                    ).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "basegame", "scale_factor": 1.2, "win_range": (1, 5), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 1.2, "win_range": (5000, 10000), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=10,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            }

        self.feature_mode_params = feature_mode_params

        self.game_config.opt_params = {
            "base": {
                "conditions": {
                    # ~1 in 5M base spins hit the cap (multi-mirror blowout):
                    # comfortably above Stake's "more frequent than 1 in 10M" floor
                    "wincap": ConstructConditions(
                        rtp=0.006, av_win=wincaps["base"], search_conditions=wincaps["base"]
                    ).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.414, hr=220, search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    # basegame absorbs the base-mode RTP tilt (bonuses pay more)
                    "basegame": ConstructConditions(
                        hr=4.0, rtp=mode_rtps["base"] - 0.006 - 0.414
                    ).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "basegame", "scale_factor": 1.2, "win_range": (1, 2), "probability": 1.0},
                        {"criteria": "basegame", "scale_factor": 1.5, "win_range": (10, 20), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 1.2, "win_range": (5000, 10000), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=10,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[50, 100, 200],
                    test_weights=[0.3, 0.4, 0.3],
                    score_type="rtp",
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["basegame"],
                    bias_ranges=[(1.5, 3.5)],
                    bias_weights=[0.4],
                ).return_dict(),
            },
            "bonus1": buy_mode_params("bonus1", test_spins=[10, 20, 50], wincap_rtp=0.003),
            "bonus2": buy_mode_params("bonus2", test_spins=[10, 20, 50], wincap_rtp=0.010),
            "bonus3": buy_mode_params("bonus3", test_spins=[5, 10, 20], wincap_rtp=0.150),
            # ANTE (cost 1.25x, rtp 0.962 of cost): the 0.25x surcharge buys a
            # DOUBLED bonus trigger rate. Budget per cost unit:
            #   bonus part  = 2 x 0.4173 / 1.25 = 0.666  (trigger 1 in 109)
            #   base wins   = 0.962 - 0.004 - 0.666 = 0.292 (x0.67 of base)
            "ante": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.004, av_win=wincaps["ante"], search_conditions=wincaps["ante"]
                    ).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.666, hr=109, search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(hr=6.0, rtp=0.292).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {"criteria": "basegame", "scale_factor": 1.2, "win_range": (1, 2), "probability": 1.0},
                        {"criteria": "basegame", "scale_factor": 1.5, "win_range": (10, 20), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
                        {"criteria": "freegame", "scale_factor": 1.2, "win_range": (5000, 10000), "probability": 1.0},
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=10,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[50, 100, 200],
                    test_weights=[0.3, 0.4, 0.3],
                    score_type="rtp",
                ).return_dict(),
                "distribution_bias": ConstructFenceBias(
                    applied_criteria=["basegame"],
                    bias_ranges=[(1.5, 3.5)],
                    bias_weights=[0.4],
                ).return_dict(),
            },
            # FEATURE SPINS (guaranteed mirrors). Priced off measured natural
            # EVs: E[pay | 1+/2+/3 mirrors] = 8.26x / 19.87x / 38.84x, so costs
            # 10x / 20x / 40x land within +-17% of fair at 96.5% of cost.
            # freegame share = P(trigger | mirrors) x E[bonus] / cost.
            "feature1": self.feature_mode_params(cost=10.0, wincap_rtp=0.002, freegame_rtp=0.100),
            "feature2": self.feature_mode_params(cost=20.0, wincap_rtp=0.003, freegame_rtp=0.050),
            "feature3": self.feature_mode_params(cost=40.0, wincap_rtp=0.005, freegame_rtp=0.025),
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
