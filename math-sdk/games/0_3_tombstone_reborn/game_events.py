"""Custom book events for TOMBSTONE REBORN.

All board row indices are emitted padding-adjusted (+1) to line up with the
reveal / winInfo events (which prepend the top padding symbol).

Event stream order for a spin:
    reveal
    specialBar                 (what the top cards are, if any)
    [digUp] [coffinOpen] [gunsmoke] [splitGang] [splitOutlaws]
    [superSplit] [bounty|nudge]
    winInfo / setWin / setTotal
    finalWin
"""


def _padrow(pos):
    return {"reel": pos["reel"], "row": pos["row"] + 1}


def special_bar_event(gamestate):
    """The top bar resolves: lists every cell and the card it revealed.

    cells: one entry per bar cell that is NOT empty
      - reel:  the column the card sits above
      - kind:  split_gang | split_outlaws | gunsmoke | digup | coffin
    barMode: which unlock state produced this bar (base/small/super/off).
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "specialBar",
        "barMode": gamestate.bar_mode,
        "cells": [
            {"reel": c["reel"], "kind": c["kind"]}
            for c in gamestate.special_bar
            if c["kind"] != "none"
        ],
    }
    gamestate.book.add_event(event)


def dig_up_event(gamestate):
    """DIG UP unlocked the last-reel lane mid-spin (base/small only - it is
    already open in the super bonus)."""
    event = {
        "index": len(gamestate.book.events),
        "type": "digUp",
        "reel": gamestate.config.num_reels - 1,
    }
    gamestate.book.add_event(event)


def coffin_open_event(gamestate, grown):
    """TOMBSTONE OPEN grew short reels taller, revealing extra symbols.

    reels: one entry per reel that grew
      - reel:     reel index
      - added:    how many rows were appended at the bottom
      - newCells: the freshly revealed symbols, bottom-most last
          - row:  padding-adjusted board row
          - name: symbol name
    totalWays: ways count after the growth.
    """
    reels = []
    for g in grown:
        reels.append({
            "reel": g["reel"],
            "added": g["added"],
            "newCells": [{"row": c["row"] + 1, "name": c["name"]} for c in g["cells"]],
        })
    event = {
        "index": len(gamestate.book.events),
        "type": "coffinOpen",
        "reels": reels,
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def gunsmoke_event(gamestate, symbol, cells):
    """GUNSMOKE turned one whole symbol type into WILDs.

    symbol: the type that was converted.
    cells:  the board cells that became wild (padding-adjusted rows).
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "gunsmoke",
        "symbol": symbol,
        "cells": [_padrow(c) for c in cells],
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def split_event(gamestate, kind, factor, cells):
    """SPLIT-GANG / SPLIT-OUTLAWS added ways to every premium / low on board.

    kind:   "gang" (premiums) or "outlaws" (lows).
    factor: how many ways were added to each affected cell.
    cells:  affected cells, each with its resulting per-cell ways multiplier.
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "splitGang" if kind == "gang" else "splitOutlaws",
        "factor": factor,
        "cells": [
            {"reel": c["reel"], "row": c["row"] + 1, "multiplier": c["multiplier"]}
            for c in cells
        ],
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def super_split_event(gamestate, factor, wild_cells, split_cells):
    """SUPERSPLIT: the last reel turned wild and EVERY paying symbol was split.

    factor:     ways added to each paying cell.
    wildCells:  cells on the last reel that became wild.
    cells:      every split cell with its resulting per-cell ways multiplier.
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "superSplit",
        "factor": factor,
        "wildCells": [_padrow(c) for c in wild_cells],
        "cells": [
            {"reel": c["reel"], "row": c["row"] + 1, "multiplier": c["multiplier"]}
            for c in split_cells
        ],
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def bounty_event(gamestate, symbol, win_mult):
    """BOUNTY: a random premium landed on the last reel carrying a WIN mult.

    symbol:  the premium that landed.
    winMult: the WIN multiplier it carries (multiplies the whole spin win).
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "bounty",
        "reel": gamestate.config.num_reels - 1,
        "symbol": symbol,
        "winMult": win_mult,
    }
    gamestate.book.add_event(event)


def nudge_event(gamestate, symbol, base_mult, passed, win_mult, steps=None):
    """NUDGE: the nudge wild racked LEFT from the lane, one notch per reel,
    stepping onto exactly one cell of each column and leaving it WILD. Every
    premium it crushed added to the WIN multiplier.

    symbol:    what rides ("W" — the nudge wild wears its own face).
    baseMult:  the WIN multiplier before the slide.
    passed:    how many premiums the walk crushed.
    winMult:   the final WIN multiplier after the walk.
    steps:     the full path right-to-left (reel last-1..0), padding-adjusted
               rows; `name` is the symbol that WAS there, `premium` whether it
               bumped the multiplier. The last step is always the first reel's
               middle cell — the rider's resting place.
    hits:      kept for older frontends: the premium steps only.
    """
    steps = steps or []
    event = {
        "index": len(gamestate.book.events),
        "type": "nudge",
        "symbol": symbol,
        "baseMult": base_mult,
        "passed": passed,
        "winMult": win_mult,
        "steps": [
            {
                "reel": s["reel"],
                "row": s["row"] + 1,
                "name": s.get("name"),
                "premium": bool(s.get("premium")),
            }
            for s in steps
        ],
        "hits": [
            {"reel": s["reel"], "row": s["row"] + 1, "name": s.get("name")}
            for s in steps
            if s.get("premium")
        ],
    }
    gamestate.book.add_event(event)
