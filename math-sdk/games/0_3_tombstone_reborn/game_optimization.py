"""Optimization parameters for TOMBSTONE REBORN (extreme volatility, 3 modes).

Each mode shares three fences whose condition RTPs sum EXACTLY to the mode RTP
(verify_optimization_input asserts this):
    wincap     the 99,999x cap slice (sized per mode)
    0          the dead-spin fence (rtp 0)
    basegame   the paying bulk that carries the remaining RTP

Volatility shaping (per mode `cost`): fatten the sub-cost dud band, thin the
near-cost "refund" band, and boost the 2x-6x cost mid band, so a spin either
stings or genuinely pays.

Target profiles (approached here, exact percentiles are a follow-up tuning
pass with the lookup-table tail tools):
    base         ~92% dead spins
    bonus_small  ~40% of buys return exactly 0
    bonus_super  ~70% of buys return below the 1000x cost
"""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    verify_optimization_input,
)


class OptimizationSetup:
    """Game specific optimization setup."""

    def __init__(self, game_config):
        self.game_config = game_config
        mode_rtps = game_config.mode_rtps
        wincaps = {bm.get_name(): bm.get_wincap() for bm in game_config.bet_modes}

        def params(test_spins, max_m2m=20):
            return ConstructParameters(
                num_show=5000,
                num_per_fence=10000,
                min_m2m=2,
                max_m2m=max_m2m,
                pmb_rtp=1.0,
                sim_trials=5000,
                test_spins=test_spins,
                test_weights=[0.3, 0.4, 0.3],
                score_type="rtp",
            ).return_dict()

        def scaling(cost, profile="default"):
            if profile == "super":
                # lift mass ABOVE cost so ~70% (not ~87%) of buys land below the
                # 1000x price, while keeping a fat extreme tail
                bands = [
                    {"criteria": "basegame", "scale_factor": 1.10, "win_range": (0, 0.6 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 0.70, "win_range": (0.8 * cost, 1.4 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 1.45, "win_range": (1.5 * cost, 5 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 1.20, "win_range": (5 * cost, 20 * cost), "probability": 1.0},
                ]
            else:
                bands = [
                    {"criteria": "basegame", "scale_factor": 1.35, "win_range": (0, 0.6 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 0.75, "win_range": (0.8 * cost, 1.6 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 1.25, "win_range": (2 * cost, 6 * cost), "probability": 1.0},
                ]
            return ConstructScaling(bands).return_dict()

        def mode_block(mode, wincap_rtp, base_hr, test_spins, cost, max_m2m=20):
            base_rtp = round(mode_rtps[mode] - wincap_rtp, 5)
            base_cond = (
                ConstructConditions(rtp=base_rtp, hr=base_hr).return_dict()
                if base_hr is not None
                else ConstructConditions(rtp=base_rtp, hr="x").return_dict()
            )
            return {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=wincap_rtp, av_win=wincaps[mode], search_conditions=wincaps[mode]
                    ).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "basegame": base_cond,
                },
                "scaling": scaling(cost, profile="super" if mode == "bonus_super" else "default"),
                "parameters": params(test_spins, max_m2m=max_m2m),
            }

        self.game_config.opt_params = {
            # base: ~1 in 1M base spins hit the cap; basegame hr ~12 -> ~92% dead
            "base": mode_block("base", wincap_rtp=0.10, base_hr=12.0,
                               test_spins=[50, 100, 200], cost=1),
            # small buy (80x): ~40% return exactly 0 -> basegame hr ~1.67
            "bonus_small": mode_block("bonus_small", wincap_rtp=0.08, base_hr=1.667,
                                      test_spins=[20, 50, 100], cost=80),
            # super buy (1000x): pinned hit-rate (~26% zero) so the median stays
            # positive, a smaller cap slice and a high m2m ceiling to carry the
            # extreme tail; scaling skews the bulk below the 1000x cost
            "bonus_super": mode_block("bonus_super", wincap_rtp=0.12, base_hr=1.35,
                                      test_spins=[10, 20, 50], cost=1000, max_m2m=60),
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
