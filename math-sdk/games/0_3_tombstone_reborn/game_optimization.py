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

        def scaling(cost, profile="default", criteria="basegame"):
            def band(scale, lo, hi):
                return {
                    "criteria": criteria,
                    "scale_factor": scale,
                    "win_range": (lo, hi),
                    "probability": 1.0,
                }

            if profile == "super2000":
                # BIG BONUS (2000x cost): the cap is only 50x cost, so the
                # 3-star fences bite in COST terms - 5,000x base bet is just
                # 2.5x cost and P(>=5,000) must stay under 5%. Most RTP is
                # packed under 2.5x cost; the 5k/10k/20k/50k bands are starved
                # progressively so P(>=10k) ~ 0.008 and CVaR ~ 45k of 50k.
                bands = [
                    band(1.20, 0, 0.6 * cost),
                    band(0.80, 0.8 * cost, 1.4 * cost),
                    band(1.35, 1.5 * cost, 2.4 * cost),
                    band(0.15, 5000, 10000),
                    band(0.10, 10000, 20000),
                    band(0.04, 20000, 50000),
                    band(0.008, 50000, 99999),
                ]
                return ConstructScaling(bands).return_dict()
            if profile == "super":
                # Stake 3-star shaping: lift mass into the 1.5x-5x cost band and
                # STARVE the 10,000x+ base-bet tail. P(>=10,000x) must stay
                # under 1% and the worst-0.1% average (CVaR abs) under 50,000x,
                # so the 10k/20k/50k bands are suppressed progressively harder.
                # calibrated to sit JUST under the 3-star ceilings (P(10k) ~0.008
                # of the 0.01 allowance, CVaR ~45k of 50k) - as extreme as the
                # rating permits
                bands = [
                    {"criteria": "basegame", "scale_factor": 1.10, "win_range": (0, 0.6 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 0.70, "win_range": (0.8 * cost, 1.4 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 1.45, "win_range": (1.5 * cost, 5 * cost), "probability": 1.0},
                    # the scatter-diluted resim carries far more raw 10k+ mass
                    # than the old books, so the 10k+ bands are starved much
                    # harder than the pre-scatter tuning (2.20/0.50/0.04 landed
                    # P(10k) at 0.029 of the 0.01 allowance on the new books)
                    {"criteria": "basegame", "scale_factor": 0.70, "win_range": (10 * cost, 20 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 0.25, "win_range": (20 * cost, 50 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 0.02, "win_range": (50 * cost, 100 * cost), "probability": 1.0},
                ]
            elif profile == "base":
                # Stake 3-star shaping: base std dev must land under 60 (was
                # 112, dominated by the cap slice plus the 5,000x+ band), so on
                # top of the smaller wincap fence the 1,000x+ region is starved
                # and its RTP pushed down into the 2x-6x band.
                # calibrated for std ~54 of the 60 allowance: cap fence 0.02 +
                # a 1,000x+ band worth ~0.03 rtp keeps real 5,000x+ base hits
                bands = [
                    {"criteria": "basegame", "scale_factor": 1.35, "win_range": (0, 0.6 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 0.75, "win_range": (0.8 * cost, 1.6 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 1.25, "win_range": (2 * cost, 6 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 0.80, "win_range": (200 * cost, 1000 * cost), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 0.15, "win_range": (1000 * cost, 99999 * cost), "probability": 1.0},
                    # the natural bonus rounds also live inside BASE books and
                    # count toward the base std-dev ceiling: keep small rounds
                    # mostly under 1,000x and big-round monsters rare
                    {"criteria": "freegame_small", "scale_factor": 0.10, "win_range": (1000, 99999), "probability": 1.0},
                    {"criteria": "freegame_big", "scale_factor": 0.10, "win_range": (20000, 99999), "probability": 1.0},
                ]
            else:
                # default dud/refund/mid shaping; `criteria` picks whether it
                # shapes single-spin books ("basegame") or rounds ("freegame")
                bands = [
                    band(1.35, 0, 0.6 * cost),
                    band(0.75, 0.8 * cost, 1.6 * cost),
                    band(1.25, 2 * cost, 6 * cost),
                ]
            return ConstructScaling(bands).return_dict()

        def mode_block(mode, wincap_rtp, base_hr, test_spins, cost, max_m2m=20,
                       profile="default"):
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
                "scaling": scaling(cost, profile=profile),
                "parameters": params(test_spins, max_m2m=max_m2m),
            }

        # base carries FIVE fences now: the cap slice, the dead spins, the two
        # natural bonus-trigger fences and the paying bulk. The trigger fences
        # BIND their books through force_search against the scatter force
        # records (kind clamped to 4 in gamestate.run_spin) — a fence with no
        # search conditions matches nothing and silently drops its RTP slice.
        # Trigger rates fall out of rtp / hr:
        #   small round: 0.15 rtp @ hr 200    -> av ~30x,   ~1 in 200 spins
        #   big round:   0.02 rtp @ hr 80,000 -> av ~1600x, ~1 in 80k spins
        base_wincap = 0.01
        base_fg_small = ConstructConditions(
            rtp=0.15, hr=200, search_conditions={"kind": 3, "symbol": "scatter"}
        ).return_dict()
        base_fg_big = ConstructConditions(
            rtp=0.02, hr=80000, search_conditions={"kind": 4, "symbol": "scatter"}
        ).return_dict()
        base_bulk_rtp = round(mode_rtps["base"] - base_wincap - 0.15 - 0.02, 5)
        base_block = {
            "conditions": {
                "wincap": ConstructConditions(
                    rtp=base_wincap, av_win=wincaps["base"], search_conditions=wincaps["base"]
                ).return_dict(),
                "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                "freegame_small": base_fg_small,
                "freegame_big": base_fg_big,
                "basegame": ConstructConditions(rtp=base_bulk_rtp, hr=12.0).return_dict(),
            },
            "scaling": scaling(1, profile="base"),
            "parameters": params([50, 100, 200]),
        }

        # bought bonus rounds have no realistic all-zero outcome (ten bar-awake
        # spins), so they carry just two fences: the cap slice + the round bulk
        def round_block(mode, wincap_rtp, test_spins, cost, profile, max_m2m=20):
            bulk_rtp = round(mode_rtps[mode] - wincap_rtp, 5)
            return {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=wincap_rtp, av_win=wincaps[mode], search_conditions=wincaps[mode]
                    ).return_dict(),
                    "freegame": ConstructConditions(rtp=bulk_rtp, hr="x").return_dict(),
                },
                "scaling": scaling(cost, profile=profile, criteria="freegame"),
                "parameters": params(test_spins, max_m2m=max_m2m),
            }

        self.game_config.opt_params = {
            "base": base_block,
            # small buy (80x): ~40% return exactly 0 -> basegame hr ~1.67
            # (passes every 3-star check as-is - do not disturb)
            "bonus_small": mode_block("bonus_small", wincap_rtp=0.08, base_hr=1.667,
                                      test_spins=[20, 50, 100], cost=80),
            # super buy (1000x): cap slice 0.008 (P(cap) ~ 0.008%, inside the
            # worst-0.1% CVaR window with room for the sub-cap tail), and the
            # super scaling keeps P(>=10k) ~0.008 of the 0.01 allowance
            "bonus_super": mode_block("bonus_super", wincap_rtp=0.006, base_hr=1.35,
                                      test_spins=[10, 20, 50], cost=1000, max_m2m=60,
                                      profile="super"),
            # SMALL BONUS rounds (80x buy): shaped like bonus_small, whose
            # numbers pass every 3-star check at the same cost
            "freespins": round_block("freespins", wincap_rtp=0.08,
                                     test_spins=[20, 50, 100], cost=80,
                                     profile="default"),
            # BIG BONUS rounds (2000x buy): cap fence 0.007 -> P(cap) ~ 1.4e-4,
            # inside the worst-0.1% CVaR window (0.01 landed CVaR at 53.4k of
            # the 50k allowance); super2000 starves the absolute 5k/10k+
            # bands that the 3-star fences measure
            "superspins": round_block("superspins", wincap_rtp=0.007,
                                      test_spins=[5, 10, 20], cost=2000,
                                      max_m2m=60, profile="super2000"),
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
