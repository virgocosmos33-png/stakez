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

        def buy_mode_params(mode_name, test_spins, wincap_rtp):
            """Bonus buys share one shape: a wincap slice (sized per level) + freegame bulk."""
            return {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=wincap_rtp, av_win=wincaps[mode_name], search_conditions=wincaps[mode_name]
                    ).return_dict(),
                    "freegame": ConstructConditions(rtp=0.965 - wincap_rtp, hr="x").return_dict(),
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
                    "basegame": ConstructConditions(hr=4.0, rtp=0.545).return_dict(),
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
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
