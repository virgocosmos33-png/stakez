"""THE WHITE ROOM per-symbol animation concepts for gen_symbol_spines.py.

Each paying/special id maps to a distinct clinical-horror motion language so
land / win do not share the Madam Mirror punch+wobble+wisp pack. High-pay
win is a grow (bigger + lift, no thrash). postWin holds that size with a
shared inhale, not a mesh wave.
"""

from __future__ import annotations

import math

# High-pay win / postWin: grow out of the pocket. Not White Room squash.
GROW_IDS = {"h1", "h2", "h3", "h4", "h5"}
WIN_GROW_END = 1.12
WIN_GROW_LIFT = 8

# Concept ids drive land/win/postWin builders in gen_symbol_spines.py
CONCEPT_BY_GID = {
    "h1": "restraint_snap",      # Patient — straps jolt, thrash
    "h2": "clinical_glare",      # Doctor — fluorescent freeze, cold bloom
    "h3": "grin_lunge",          # Grin — face punches forward, jaw stretch
    "h4": "doorway_void",        # Doorway — slam then void suck
    "h5": "memory_glitch",       # File 404 — digital stamp glitch
    "l1": "tile_crack_a",        # ceramic stamp crack family
    "l2": "tile_crack_b",
    "l3": "tile_crack_c",
    "l4": "tile_crack_d",
    "l5": "tile_crack_e",
    "w": "skin_seal",            # Sealed — taut skin rip
    "s": "ash_dissolve",         # Memory Reset — dust dissolve
    "hm": "pane_shatter",        # Observation Pane — glass break
    "me": "cctv_blink",          # It Knows — shutter blink (if rigged)
}


def hex_rgba(tint, alpha):
    r, g, b = tint
    return f"{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}{int(max(0, min(1, alpha)) * 255):02x}"


def white_rgba(alpha):
    return hex_rgba((1, 1, 1), alpha)


def _shard_burst(gid, tint, t0, t1, dist=110, spin=170):
    """Porcelain/glass chips to corners — White Room, not purple gems."""
    slots, bones = {}, {}
    for j, (sx, sy) in zip((1, 2, 3, 4), ((-1, -1), (1, -1), (1, 1), (-1, 1))):
        variant = ["a", "b", "c", "a"][j - 1]
        slots[f"{gid}_shard{j}"] = {
            "attachment": [
                {"name": None},
                {"time": t0, "name": f"fx_shard_{variant}"},
                {"time": t1, "name": None},
            ],
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": t0, "color": hex_rgba(tint, 0.95)},
                {"time": t1, "color": hex_rgba(tint, 0)},
            ],
        }
        bones[f"shard{j}"] = {
            "translate": [
                {"time": t0, "x": sx * 18, "y": sy * 18},
                {"time": t1, "x": sx * dist, "y": sy * dist - 14},
            ],
            "rotate": [
                {"time": t0, "value": 0},
                {"time": t1, "value": (spin + 35 * j) * (1 if sx > 0 else -1)},
            ],
            "scale": [
                {"time": t0, "x": 1.05, "y": 1.05},
                {"time": t1, "x": 0.55, "y": 0.55},
            ],
        }
    return slots, bones


def _dust_wisps(gid, tint, t0, t1, rise=90, angles=(-120, -90, -55)):
    """Clinical dust / ash — replaces gothic spectral wisps."""
    slots, bones = {}, {}
    for i, angle in zip((1, 2, 3), angles):
        rad = math.radians(angle)
        dx, dy = math.cos(rad) * rise, math.sin(rad) * rise
        slots[f"{gid}_wisp{i}"] = {
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": t0, "color": hex_rgba(tint, 0)},
                {"time": t0 + 0.12, "color": hex_rgba(tint, 0.55)},
                {"time": t1, "color": hex_rgba(tint, 0)},
            ]
        }
        bones[f"wisp{i}"] = {
            "translate": [
                {"x": dx * 0.1, "y": dy * 0.1},
                {"time": t0, "x": dx * 0.1, "y": dy * 0.1},
                {"time": t1, "x": dx, "y": dy - 20},
            ],
            "scale": [
                {"x": 0.55, "y": 0.55},
                {"time": t1, "x": 1.35, "y": 1.35},
            ],
        }
    return slots, bones


# ---------------------------------------------------------------- land


def land_animation(gid, tint):
    concept = CONCEPT_BY_GID.get(gid, "tile_crack_a")

    if concept == "restraint_snap":
        # lateral strap jolt — not squash-slam
        return {
            "bones": {
                "card": {
                    "translate": [
                        {"x": -14},
                        {"time": 0.07, "x": 11},
                        {"time": 0.14, "x": -6},
                        {"time": 0.22, "x": 3},
                        {"time": 0.32, "x": 0},
                    ],
                    "scale": [
                        {"x": 1.08, "y": 0.94},
                        {"time": 0.10, "x": 0.96, "y": 1.04},
                        {"time": 0.22, "x": 1.02, "y": 0.99},
                        {"time": 0.32, "x": 1.0, "y": 1.0},
                    ],
                }
            }
        }

    if concept == "clinical_glare":
        # hard stop — fluorescent freeze, almost no bounce
        return {
            "bones": {
                "card": {
                    "scale": [
                        {"x": 1.04, "y": 1.04},
                        {"time": 0.06, "x": 0.985, "y": 0.985},
                        {"time": 0.18, "x": 1.0, "y": 1.0},
                    ],
                    "translate": [
                        {"y": 8},
                        {"time": 0.08, "y": 0},
                    ],
                }
            },
            "slots": {
                f"{gid}_glow": {
                    "rgba": [
                        {"color": "ffffff00"},
                        {"time": 0.04, "color": "ffffff66"},
                        {"time": 0.22, "color": "ffffff00"},
                    ]
                }
            },
        }

    if concept == "grin_lunge":
        return {
            "bones": {
                "card": {
                    "scale": [
                        {"x": 0.88, "y": 0.88},
                        {"time": 0.10, "x": 1.14, "y": 1.14},
                        {"time": 0.20, "x": 0.98, "y": 0.98},
                        {"time": 0.30, "x": 1.0, "y": 1.0},
                    ],
                    "translate": [
                        {"y": -18},
                        {"time": 0.10, "y": 6},
                        {"time": 0.30, "y": 0},
                    ],
                }
            }
        }

    if concept == "doorway_void":
        # door slam — heavy vertical crush into the row
        return {
            "bones": {
                "card": {
                    "scale": [
                        {"x": 1.22, "y": 0.72},
                        {"time": 0.12, "x": 0.94, "y": 1.06},
                        {"time": 0.24, "x": 1.02, "y": 0.98},
                        {"time": 0.34, "x": 1.0, "y": 1.0},
                    ],
                    "translate": [
                        {"y": 38},
                        {"time": 0.12, "y": -8},
                        {"time": 0.24, "y": 3},
                        {"time": 0.34, "y": 0},
                    ],
                }
            }
        }

    if concept == "memory_glitch":
        return {
            "bones": {
                "card": {
                    "translate": [
                        {"x": -10, "y": 4},
                        {"time": 0.05, "x": 12, "y": -3},
                        {"time": 0.10, "x": -7, "y": 2},
                        {"time": 0.16, "x": 4, "y": -1},
                        {"time": 0.24, "x": 0, "y": 0},
                    ],
                    "shear": [
                        {"x": 6},
                        {"time": 0.08, "x": -5},
                        {"time": 0.16, "x": 2},
                        {"time": 0.24, "x": 0},
                    ],
                    "scale": [
                        {"x": 1.06, "y": 0.94},
                        {"time": 0.12, "x": 0.97, "y": 1.03},
                        {"time": 0.24, "x": 1.0, "y": 1.0},
                    ],
                }
            }
        }

    if concept.startswith("tile_crack"):
        # ceramic tile clack — rotate settle, different phase per low
        phase = {"a": 1, "b": -1, "c": 1, "d": -1, "e": 1}[concept[-1]]
        return {
            "bones": {
                "card": {
                    "rotate": [
                        {"value": 7 * phase},
                        {"time": 0.10, "value": -3 * phase},
                        {"time": 0.20, "value": 1.2 * phase},
                        {"time": 0.30, "value": 0},
                    ],
                    "scale": [
                        {"x": 1.10, "y": 0.90},
                        {"time": 0.10, "x": 0.96, "y": 1.04},
                        {"time": 0.22, "x": 1.01, "y": 0.995},
                        {"time": 0.30, "x": 1.0, "y": 1.0},
                    ],
                    "translate": [
                        {"y": 16},
                        {"time": 0.10, "y": -4},
                        {"time": 0.30, "y": 0},
                    ],
                }
            }
        }

    if concept == "skin_seal":
        return {
            "bones": {
                "card": {
                    "scale": [
                        {"x": 1.12, "y": 0.90},
                        {"time": 0.14, "x": 0.97, "y": 1.05},
                        {"time": 0.28, "x": 1.0, "y": 1.0},
                    ],
                }
            }
        }

    if concept == "ash_dissolve":
        # soft float-in — no hard slam
        return {
            "bones": {
                "card": {
                    "scale": [
                        {"x": 0.92, "y": 0.92},
                        {"time": 0.18, "x": 1.02, "y": 1.02},
                        {"time": 0.32, "x": 1.0, "y": 1.0},
                    ],
                    "translate": [
                        {"y": -22},
                        {"time": 0.20, "y": 2},
                        {"time": 0.32, "y": 0},
                    ],
                }
            },
            "slots": {
                f"{gid}_aura": {
                    "rgba": [
                        {"color": hex_rgba(tint, 0.25)},
                        {"time": 0.28, "color": hex_rgba(tint, 0)},
                    ]
                }
            },
        }

    if concept == "pane_shatter":
        return {
            "bones": {
                "card": {
                    "translate": [
                        {"x": -5},
                        {"time": 0.06, "x": 5},
                        {"time": 0.12, "x": -3},
                        {"time": 0.20, "x": 0},
                    ],
                    "scale": [
                        {"x": 1.03, "y": 1.03},
                        {"time": 0.20, "x": 1.0, "y": 1.0},
                    ],
                }
            }
        }

    # cctv_blink / fallback
    return {
        "bones": {
            "card": {
                "scale": [
                    {"x": 1.08, "y": 0.92},
                    {"time": 0.10, "x": 0.98, "y": 1.02},
                    {"time": 0.22, "x": 1.0, "y": 1.0},
                ]
            }
        }
    }


# ---------------------------------------------------------------- win


def win_grow_animation():
    """High-pay win: one grow toward camera, then sit at the inhale size."""
    return {
        "bones": {
            "card": {
                "scale": [
                    {"x": 1.0, "y": 1.0},
                    {"time": 0.18, "x": 1.20, "y": 1.20},
                    {"time": 0.40, "x": 1.14, "y": 1.14},
                    {"time": 0.68, "x": WIN_GROW_END, "y": WIN_GROW_END},
                ],
                "translate": [
                    {},
                    {"time": 0.18, "y": 14},
                    {"time": 0.40, "y": 10},
                    {"time": 0.68, "y": WIN_GROW_LIFT},
                ],
            }
        }
    }


def win_animation(gid, tint):
    if gid in GROW_IDS:
        return win_grow_animation()
    concept = CONCEPT_BY_GID.get(gid, "tile_crack_a")

    if concept == "restraint_snap":
        slots = {
            f"{gid}_glow": {
                "rgba": [
                    {"color": "ffffff00"},
                    {"time": 0.10, "color": "ffffff99"},
                    {"time": 0.22, "color": "ffffff22"},
                    {"time": 0.40, "color": "ffffff66"},
                    {"time": 0.75, "color": "ffffff00"},
                ]
            },
            f"{gid}_aura": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.14, "color": hex_rgba(tint, 0.35)},
                    {"time": 0.70, "color": hex_rgba(tint, 0)},
                ]
            },
            f"{gid}_streak": {"rgba": [{"color": white_rgba(0)}]},
            f"{gid}_ring": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.18, "color": hex_rgba(tint, 0.55)},
                    {"time": 0.55, "color": hex_rgba(tint, 0)},
                ]
            },
        }
        bones = {
            "card": {
                "translate": [
                    {},
                    {"time": 0.08, "x": -18},
                    {"time": 0.16, "x": 16},
                    {"time": 0.26, "x": -12},
                    {"time": 0.38, "x": 8},
                    {"time": 0.52, "x": -3},
                    {"time": 0.70, "x": 0},
                ],
                "scale": [
                    {},
                    {"time": 0.10, "x": 1.16, "y": 0.88},
                    {"time": 0.22, "x": 0.92, "y": 1.10},
                    {"time": 0.40, "x": 1.06, "y": 0.96},
                    {"time": 0.65, "x": 1.0, "y": 1.0},
                ],
                "rotate": [
                    {},
                    {"time": 0.12, "value": -5},
                    {"time": 0.24, "value": 6},
                    {"time": 0.40, "value": -2},
                    {"time": 0.60, "value": 0},
                ],
            },
            "ring": {
                "scale": [
                    {"x": 0.45, "y": 0.45},
                    {"time": 0.18, "x": 0.45, "y": 0.45},
                    {"time": 0.55, "x": 1.55, "y": 1.55},
                ]
            },
        }
        ss, sb = _shard_burst(gid, tint, 0.16, 0.62, dist=100)
        slots.update(ss)
        bones.update(sb)
        return {"slots": slots, "bones": bones}

    if concept == "clinical_glare":
        # cold bloom — NO wobble, harsh white flash + fluorescent streak once
        slots = {
            f"{gid}_glow": {
                "rgba": [
                    {"color": "ffffff00"},
                    {"time": 0.08, "color": "ffffffdd"},
                    {"time": 0.20, "color": "ffffff44"},
                    {"time": 0.55, "color": "ffffff22"},
                    {"time": 0.85, "color": "ffffff00"},
                ]
            },
            f"{gid}_aura": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.12, "color": hex_rgba(tint, 0.50)},
                    {"time": 0.70, "color": hex_rgba(tint, 0)},
                ]
            },
            f"{gid}_streak": {
                "rgba": [
                    {"color": white_rgba(0)},
                    {"time": 0.10, "color": white_rgba(0.95)},
                    {"time": 0.28, "color": white_rgba(0.95)},
                    {"time": 0.34, "color": white_rgba(0)},
                ]
            },
            f"{gid}_ring": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.14, "color": hex_rgba(tint, 0.70)},
                    {"time": 0.60, "color": hex_rgba(tint, 0)},
                ]
            },
        }
        bones = {
            "card": {
                "scale": [
                    {},
                    {"time": 0.10, "x": 1.08, "y": 1.08},
                    {"time": 0.35, "x": 1.04, "y": 1.04},
                    {"time": 0.75, "x": 1.0, "y": 1.0},
                ],
            },
            "streak": {
                "translate": [
                    {"x": -280},
                    {"time": 0.32, "x": 280},
                ]
            },
            "ring": {
                "scale": [
                    {"x": 0.6, "y": 0.6},
                    {"time": 0.14, "x": 0.6, "y": 0.6},
                    {"time": 0.60, "x": 1.65, "y": 1.65},
                ]
            },
        }
        return {"slots": slots, "bones": bones}

    if concept == "grin_lunge":
        slots = {
            f"{gid}_glow": {
                "rgba": [
                    {"color": "ffffff00"},
                    {"time": 0.08, "color": "ffffffaa"},
                    {"time": 0.35, "color": "ffffff33"},
                    {"time": 0.80, "color": "ffffff00"},
                ]
            },
            f"{gid}_aura": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.12, "color": hex_rgba(tint, 0.45)},
                    {"time": 0.70, "color": hex_rgba(tint, 0)},
                ]
            },
            f"{gid}_streak": {"rgba": [{"color": white_rgba(0)}]},
            f"{gid}_ring": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.12, "color": hex_rgba(tint, 0.65)},
                    {"time": 0.50, "color": hex_rgba(tint, 0)},
                ]
            },
        }
        bones = {
            "card": {
                "scale": [
                    {},
                    {"time": 0.06, "x": 0.82, "y": 0.90},
                    {"time": 0.16, "x": 1.28, "y": 1.18},
                    {"time": 0.30, "x": 0.96, "y": 1.04},
                    {"time": 0.50, "x": 1.08, "y": 0.96},
                    {"time": 0.75, "x": 1.0, "y": 1.0},
                ],
                "shear": [
                    {},
                    {"time": 0.14, "x": 8},
                    {"time": 0.28, "x": -6},
                    {"time": 0.50, "x": 2},
                    {"time": 0.70, "x": 0},
                ],
            },
            "ring": {
                "scale": [
                    {"x": 0.4, "y": 0.4},
                    {"time": 0.12, "x": 0.4, "y": 0.4},
                    {"time": 0.50, "x": 1.8, "y": 1.8},
                ]
            },
        }
        ds, db = _dust_wisps(gid, tint, 0.14, 0.72, rise=70, angles=(-150, -90, -30))
        slots.update(ds)
        bones.update(db)
        return {"slots": slots, "bones": bones}

    if concept == "doorway_void":
        slots = {
            f"{gid}_glow": {
                "rgba": [
                    {"color": "ffffff00"},
                    {"time": 0.10, "color": "ffffff55"},
                    {"time": 0.30, "color": "00000088"},
                    {"time": 0.55, "color": "ffffff44"},
                    {"time": 0.85, "color": "ffffff00"},
                ]
            },
            f"{gid}_aura": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.20, "color": hex_rgba((0.3, 0.3, 0.3), 0.55)},
                    {"time": 0.70, "color": hex_rgba(tint, 0)},
                ]
            },
            f"{gid}_streak": {"rgba": [{"color": white_rgba(0)}]},
            f"{gid}_ring": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.22, "color": hex_rgba(tint, 0.40)},
                    {"time": 0.65, "color": hex_rgba(tint, 0)},
                ]
            },
        }
        bones = {
            "card": {
                "scale": [
                    {},
                    {"time": 0.10, "x": 1.10, "y": 0.85},
                    {"time": 0.28, "x": 0.72, "y": 0.72},  # void suck
                    {"time": 0.48, "x": 1.15, "y": 1.15},
                    {"time": 0.75, "x": 1.0, "y": 1.0},
                ],
            },
            "ring": {
                "scale": [
                    {"x": 1.4, "y": 1.4},
                    {"time": 0.22, "x": 1.4, "y": 1.4},
                    {"time": 0.65, "x": 0.5, "y": 0.5},  # ring collapses inward
                ]
            },
        }
        return {"slots": slots, "bones": bones}

    if concept == "memory_glitch":
        slots = {
            f"{gid}_glow": {
                "rgba": [
                    {"color": "ffffff00"},
                    {"time": 0.06, "color": "ffffffcc"},
                    {"time": 0.10, "color": "ffffff00"},
                    {"time": 0.16, "color": "ffffffaa"},
                    {"time": 0.22, "color": "ffffff00"},
                    {"time": 0.40, "color": "ffffff66"},
                    {"time": 0.80, "color": "ffffff00"},
                ]
            },
            f"{gid}_aura": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.15, "color": hex_rgba(tint, 0.30)},
                    {"time": 0.70, "color": hex_rgba(tint, 0)},
                ]
            },
            f"{gid}_streak": {
                "rgba": [
                    {"color": white_rgba(0)},
                    {"time": 0.08, "color": white_rgba(0.7)},
                    {"time": 0.14, "color": white_rgba(0)},
                    {"time": 0.30, "color": white_rgba(0.5)},
                    {"time": 0.38, "color": white_rgba(0)},
                ]
            },
            f"{gid}_ring": {"rgba": [{"color": hex_rgba(tint, 0)}]},
        }
        bones = {
            "card": {
                "translate": [
                    {},
                    {"time": 0.05, "x": -16, "y": 2},
                    {"time": 0.10, "x": 18, "y": -4},
                    {"time": 0.16, "x": -12, "y": 6},
                    {"time": 0.24, "x": 8, "y": -2},
                    {"time": 0.36, "x": -4, "y": 1},
                    {"time": 0.55, "x": 0, "y": 0},
                ],
                "shear": [
                    {},
                    {"time": 0.08, "x": 12},
                    {"time": 0.14, "x": -14},
                    {"time": 0.22, "x": 7},
                    {"time": 0.40, "x": 0},
                ],
                "scale": [
                    {},
                    {"time": 0.08, "x": 1.20, "y": 0.85},
                    {"time": 0.16, "x": 0.88, "y": 1.15},
                    {"time": 0.30, "x": 1.05, "y": 0.97},
                    {"time": 0.55, "x": 1.0, "y": 1.0},
                ],
            },
            "streak": {
                "translate": [
                    {"x": -300, "y": 40},
                    {"time": 0.14, "x": 300, "y": -40, "curve": "stepped"},
                    {"time": 0.28, "x": -300, "y": -20},
                    {"time": 0.40, "x": 300, "y": 20},
                ]
            },
        }
        return {"slots": slots, "bones": bones}

    if concept.startswith("tile_crack"):
        # porcelain crack + chips — no gothic sheen wobble
        rot_dir = 1 if concept[-1] in "ace" else -1
        slots = {
            f"{gid}_glow": {
                "rgba": [
                    {"color": "ffffff00"},
                    {"time": 0.10, "color": "ffffff77"},
                    {"time": 0.45, "color": "ffffff22"},
                    {"time": 0.80, "color": "ffffff00"},
                ]
            },
            f"{gid}_aura": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.14, "color": hex_rgba(tint, 0.28)},
                    {"time": 0.70, "color": hex_rgba(tint, 0)},
                ]
            },
            f"{gid}_streak": {"rgba": [{"color": white_rgba(0)}]},
            f"{gid}_ring": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.12, "color": hex_rgba(tint, 0.50)},
                    {"time": 0.50, "color": hex_rgba(tint, 0)},
                ]
            },
        }
        bones = {
            "card": {
                "scale": [
                    {},
                    {"time": 0.08, "x": 0.96, "y": 0.96},
                    {"time": 0.16, "x": 1.10, "y": 1.10},
                    {"time": 0.35, "x": 0.99, "y": 0.99},
                    {"time": 0.60, "x": 1.0, "y": 1.0},
                ],
                "rotate": [
                    {},
                    {"time": 0.12, "value": 3 * rot_dir},
                    {"time": 0.28, "value": -2 * rot_dir},
                    {"time": 0.50, "value": 0},
                ],
            },
            "ring": {
                "scale": [
                    {"x": 0.5, "y": 0.5},
                    {"time": 0.12, "x": 0.5, "y": 0.5},
                    {"time": 0.50, "x": 1.5, "y": 1.5},
                ]
            },
        }
        ss, sb = _shard_burst(gid, tint, 0.14, 0.58, dist=125, spin=200)
        slots.update(ss)
        bones.update(sb)
        return {"slots": slots, "bones": bones}

    if concept == "skin_seal":
        slots = {
            f"{gid}_glow": {
                "rgba": [
                    {"color": "ffffff00"},
                    {"time": 0.12, "color": "ffffffbb"},
                    {"time": 0.30, "color": "ffffff33"},
                    {"time": 0.80, "color": "ffffff00"},
                ]
            },
            f"{gid}_aura": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.16, "color": hex_rgba(tint, 0.40)},
                    {"time": 0.70, "color": hex_rgba(tint, 0)},
                ]
            },
            f"{gid}_streak": {
                "rgba": [
                    {"color": white_rgba(0)},
                    {"time": 0.18, "color": white_rgba(0.6)},
                    {"time": 0.40, "color": white_rgba(0)},
                ]
            },
            f"{gid}_ring": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.20, "color": hex_rgba(tint, 0.45)},
                    {"time": 0.60, "color": hex_rgba(tint, 0)},
                ]
            },
        }
        bones = {
            "card": {
                "scale": [
                    {},
                    {"time": 0.10, "x": 1.18, "y": 0.86},  # skin taut
                    {"time": 0.22, "x": 0.94, "y": 1.08},  # rip release
                    {"time": 0.45, "x": 1.04, "y": 0.98},
                    {"time": 0.70, "x": 1.0, "y": 1.0},
                ],
            },
            "streak": {
                "translate": [
                    {"x": -200, "y": 0},
                    {"time": 0.40, "x": 200, "y": 0},
                ]
            },
            "ring": {
                "scale": [
                    {"x": 0.55, "y": 0.55},
                    {"time": 0.20, "x": 0.55, "y": 0.55},
                    {"time": 0.60, "x": 1.6, "y": 1.6},
                ]
            },
        }
        return {"slots": slots, "bones": bones}

    if concept == "ash_dissolve":
        slots = {
            f"{gid}_glow": {
                "rgba": [
                    {"color": "ffffff00"},
                    {"time": 0.15, "color": "ffffff66"},
                    {"time": 0.70, "color": "ffffff00"},
                ]
            },
            f"{gid}_aura": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.10, "color": hex_rgba(tint, 0.55)},
                    {"time": 0.80, "color": hex_rgba(tint, 0)},
                ]
            },
            f"{gid}_streak": {"rgba": [{"color": white_rgba(0)}]},
            f"{gid}_ring": {
                "rgba": [
                    {"color": hex_rgba(tint, 0)},
                    {"time": 0.18, "color": hex_rgba(tint, 0.35)},
                    {"time": 0.65, "color": hex_rgba(tint, 0)},
                ]
            },
        }
        bones = {
            "card": {
                "scale": [
                    {},
                    {"time": 0.20, "x": 1.06, "y": 1.06},
                    {"time": 0.55, "x": 0.92, "y": 1.08},
                    {"time": 0.85, "x": 1.0, "y": 1.0},
                ],
            },
            "ring": {
                "scale": [
                    {"x": 0.7, "y": 0.7},
                    {"time": 0.18, "x": 0.7, "y": 0.7},
                    {"time": 0.65, "x": 1.4, "y": 1.4},
                ]
            },
        }
        ds, db = _dust_wisps(gid, tint, 0.08, 0.85, rise=110, angles=(-140, -95, -40))
        slots.update(ds)
        bones.update(db)
        ss, sb = _shard_burst(gid, tint, 0.20, 0.70, dist=90, spin=90)  # soft ash chips
        # soften shard alpha via already-set tint
        slots.update(ss)
        bones.update(sb)
        return {"slots": slots, "bones": bones}

    if concept == "pane_shatter":
        # win on HM uses hm_break separately; this is a fallback win track
        return hm_break_animation(tint)

    # cctv / fallback — shutter blink
    slots = {
        f"{gid}_glow": {
            "rgba": [
                {"color": "ffffff00"},
                {"time": 0.05, "color": "ffffffee"},
                {"time": 0.10, "color": "000000cc"},
                {"time": 0.16, "color": "ffffffcc"},
                {"time": 0.22, "color": "00000088"},
                {"time": 0.40, "color": "ffffff44"},
                {"time": 0.75, "color": "ffffff00"},
            ]
        },
        f"{gid}_aura": {
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.15, "color": hex_rgba(tint, 0.40)},
                {"time": 0.70, "color": hex_rgba(tint, 0)},
            ]
        },
        f"{gid}_streak": {"rgba": [{"color": white_rgba(0)}]},
        f"{gid}_ring": {
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.18, "color": hex_rgba(tint, 0.55)},
                {"time": 0.55, "color": hex_rgba(tint, 0)},
            ]
        },
    }
    bones = {
        "card": {
            "scale": [
                {},
                {"time": 0.08, "x": 1.12, "y": 0.88},
                {"time": 0.18, "x": 0.96, "y": 1.06},
                {"time": 0.40, "x": 1.0, "y": 1.0},
            ],
        },
        "ring": {
            "scale": [
                {"x": 0.5, "y": 0.5},
                {"time": 0.18, "x": 0.5, "y": 0.5},
                {"time": 0.55, "x": 1.55, "y": 1.55},
            ]
        },
    }
    return {"slots": slots, "bones": bones}


def hm_break_animation(tint):
    """Observation pane burst: flash, intact->cracked, porcelain shards."""
    slots = {
        "hm": {"attachment": [{"name": "hm"}, {"time": 0.16, "name": "hm_cracked"}]},
        "hm_glow": {
            "rgba": [
                {"color": "ffffff00"},
                {"time": 0.10, "color": "ffffffdd"},
                {"time": 0.20, "color": "ffffff40"},
                {"time": 0.55, "color": "ffffff00"},
            ]
        },
        "hm_ring": {
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.12, "color": hex_rgba(tint, 0)},
                {"time": 0.18, "color": hex_rgba(tint, 0.85)},
                {"time": 0.55, "color": hex_rgba(tint, 0)},
            ]
        },
        "hm_streak": {"rgba": [{"color": white_rgba(0)}]},
        "hm_aura": {
            "rgba": [
                {"color": hex_rgba(tint, 0)},
                {"time": 0.16, "color": hex_rgba(tint, 0.40)},
                {"time": 0.50, "color": hex_rgba(tint, 0)},
            ]
        },
    }
    bones = {
        "card": {
            "scale": [
                {},
                {"time": 0.10, "x": 1.12, "y": 1.12},
                {"time": 0.22, "x": 0.96, "y": 0.96},
                {"time": 0.40, "x": 1.0, "y": 1.0},
            ],
            "translate": [
                {},
                {"time": 0.08, "x": -4},
                {"time": 0.14, "x": 5},
                {"time": 0.20, "x": 0},
            ],
        },
        "ring": {
            "scale": [
                {"x": 0.35, "y": 0.35},
                {"time": 0.12, "x": 0.35, "y": 0.35},
                {"time": 0.55, "x": 1.85, "y": 1.85},
            ]
        },
    }
    ss, sb = _shard_burst("hm", tint, 0.16, 0.55, dist=130, spin=210)
    slots.update(ss)
    bones.update(sb)
    return {"slots": slots, "bones": bones}


# ---------------------------------------------------------------- postWin breath


def postwin_animation(gid, mesh_grid=4):
    """Looping inhale — the whole plated card grows a little and lifts.

    No mesh wave. Scale reads as coming toward camera; a few pixels of Y
    keep the top proud of the timber instead of getting shaved off.
    mesh_grid is unused (kept so gen_symbol_spines can still pass it).
    """
    del mesh_grid
    if gid in GROW_IDS:
        return {
            "bones": {
                "card": {
                    "scale": [
                        {"x": WIN_GROW_END, "y": WIN_GROW_END},
                        {"time": 0.40, "x": 1.16, "y": 1.16},
                        {"time": 1.00, "x": 1.13, "y": 1.13},
                        {"time": 1.80, "x": WIN_GROW_END, "y": WIN_GROW_END},
                    ],
                    "translate": [
                        {"y": WIN_GROW_LIFT},
                        {"time": 0.40, "y": 10},
                        {"time": 1.00, "y": 9},
                        {"time": 1.80, "y": WIN_GROW_LIFT},
                    ],
                }
            }
        }
    return {
        "bones": {
            "card": {
                "scale": [
                    {"x": 1.0, "y": 1.0},
                    {"time": 0.38, "x": 1.08, "y": 1.08},
                    {"time": 0.95, "x": 1.07, "y": 1.07},
                    {"time": 1.45, "x": 1.03, "y": 1.03},
                    {"time": 1.8, "x": 1.0, "y": 1.0},
                ],
                "translate": [
                    {},
                    {"time": 0.38, "y": 7},
                    {"time": 0.95, "y": 6},
                    {"time": 1.45, "y": 2},
                    {"time": 1.8, "y": 0},
                ],
            }
        }
    }
