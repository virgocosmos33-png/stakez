"""Custom book events for TOMBSTONE REBORN.

All board row indices are emitted padding-adjusted (+1) to line up with the
reveal / winInfo events (which prepend the top padding symbol).

Event stream order for a spin:
    reveal
    boardSpecials              (feature symbols planted on the board)
    [tombstone]  (lid crack when SUPER scatter opened the lane this spin)
    [nudgeWays] [winMult]
    [gunsmoke] [winMult]
    [split] [winMult]   (also doubles a standing nudge stack)
    [superSplit] [winMult]
    [lanePremium]              (last-reel premium WAYS — not WIN multi)
    [shooter] [winMult]
    [specialsWild]             (feature symbols become the revolver)
    winInfo / setWin / setTotal
    finalWin
"""


def _padrow(pos):
    return {"reel": pos["reel"], "row": pos["row"] + 1}


def bonus_upgrade_event(gamestate, position, spin, new_total):
    """The 1-in-100 UPGRADE: a 4th scatter dropped mid small-bonus round.

    The grave lane is open from this spin on and the round's spin count is
    topped back up to a full fresh round.

    position: the cell the scatter landed on (padding-adjusted row).
    spin:     which round spin the drop happened on (1-based).
    totalFs:  the new (topped-up) total spin count.
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "bonusUpgrade",
        "position": _padrow(position),
        "spin": int(spin),
        "totalFs": int(new_total),
    }
    gamestate.book.add_event(event)


def board_specials_event(gamestate):
    """Feature symbols that landed on this spin, plus lane-unlock state.

    cells: one entry per planted feature (not MARK/SUPERSPLIT — those live
      on the last reel and fire as shooter/superSplit).
      - reel, row (padded), kind
    lastUnlocked: the grave lane is open for this spin.
    barMode: which rate table produced the plant (base/small/super/wake/off).
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "boardSpecials",
        "barMode": gamestate.bar_mode,
        "lastUnlocked": bool(gamestate.last_unlocked),
        "cells": [
            {"reel": c["reel"], "row": c["row"] + 1, "kind": c["kind"]}
            for c in getattr(gamestate, "board_specials", [])
        ],
    }
    gamestate.book.add_event(event)


def special_bar_event(gamestate):
    """Kept so older books/tools that import the name don't break."""
    board_specials_event(gamestate)


def tombstone_event(gamestate):
    """SUPER scatter unlocked the last-reel lane this spin (base/small only —
    it is already open in the super bonus)."""
    event = {
        "index": len(gamestate.book.events),
        "type": "tombstone",
        "reel": gamestate.config.num_reels - 1,
    }
    gamestate.book.add_event(event)


def dig_up_event(gamestate):
    """Legacy alias — Dig Up was renamed Tombstone."""
    tombstone_event(gamestate)


def coffin_open_event(gamestate, grown):
    """Removed mechanic. Kept so older imports don't crash."""
    return


def gunsmoke_event(gamestate, symbol, cells, added=0, win_mult=1):
    """GUNSMOKE turned one whole symbol type into WILDs.

    symbol:  the type that was converted.
    cells:   the board cells that became wild (padding-adjusted rows).
             Never includes a NUDGE stack or the rows it already swallowed.
    added:   WIN multi gained this volley (1 per shot).
    winMult: stacked WIN multiplier AFTER this volley.
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "gunsmoke",
        "symbol": symbol,
        "cells": [_padrow(c) for c in cells],
        "added": int(added),
        "winMult": int(win_mult),
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def split_event(gamestate, factor, symbols, cells, added=0, win_mult=1):
    """SPLIT added ways to every copy of the chosen symbol type.

    factor:  ways added to each paying face (2-7). A standing nudge stack
             is also hit and doubled, even when it was not the chosen type.
    symbols: the types that were selected (includes W when a nudge was doubled).
    cells:   affected cells, each with its resulting per-cell ways multiplier.
    added:   WIN multi gained this split (1 per trigger).
    winMult: stacked WIN multiplier AFTER this split.
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "split",
        "factor": factor,
        "symbols": list(symbols),
        "cells": [
            {"reel": c["reel"], "row": c["row"] + 1, "multiplier": c["multiplier"]}
            for c in cells
        ],
        "added": int(added),
        "winMult": int(win_mult),
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def nudge_ways_event(
    gamestate, reel, full_reel, start_row, initial, final, steps, cells, added=0, win_mult=1
):
    """NUDGE WAYS: a ways-wild on reel 1 or 2, optionally nudging down.

    fullReel:     the whole reel landed as the nudge — no doubling, no WIN tick.
    startRow:     padded origin row.
    initialWays:  ways on the origin (2-9).
    finalWays:    ways on the stack after every nudge (doubled each step).
    steps:        each downward notch {row (padded), ways}.
    cells:        final stack, each with its ways multiplier.
    added:        WIN multi gained (1 per downward step).
    winMult:      stacked WIN multiplier AFTER this nudge.
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "nudgeWays",
        "reel": int(reel),
        "fullReel": bool(full_reel),
        "startRow": int(start_row) + 1,
        "initialWays": int(initial),
        "finalWays": int(final),
        "steps": [{"row": s["row"] + 1, "ways": int(s["ways"])} for s in steps],
        "cells": [
            {"reel": c["reel"], "row": c["row"] + 1, "multiplier": c["multiplier"]}
            for c in cells
        ],
        "added": int(added),
        "winMult": int(win_mult),
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def super_split_event(gamestate, factor, wild_cells, split_cells, added=0, win_mult=1):
    """SUPERSPLIT: the last reel turned wild and EVERY symbol was split.

    factor:     ways added to each cell.
    wildCells:  cells on the last reel that became wild.
    cells:      every split cell with its resulting per-cell ways multiplier.
    added:      WIN multi gained this trigger (always 1).
    winMult:    stacked WIN multiplier AFTER this trigger.
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
        "added": int(added),
        "winMult": int(win_mult),
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def lane_premium_event(gamestate, symbol, ways, cells):
    """Last-reel premium landed with extra WAYS. Does not touch the WIN multi.

    symbol: the premium that landed.
    ways:   per-cell ways stamped on the lane.
    cells:  the lane cell with its ways multiplier.
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "lanePremium",
        "reel": gamestate.config.num_reels - 1,
        "symbol": symbol,
        "ways": int(ways),
        "cells": [
            {"reel": c["reel"], "row": c["row"] + 1, "multiplier": c["multiplier"]}
            for c in cells
        ],
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def bounty_event(gamestate, symbol, win_mult, added=None):
    """BOUNTY: a premium on the last reel stacked `added` onto the WIN multi.

    symbol:  the premium that landed.
    winMult: the stacked WIN multiplier AFTER this bounty.
    added:   how much this bounty contributed (defaults to winMult).
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "bounty",
        "reel": gamestate.config.num_reels - 1,
        "symbol": symbol,
        "winMult": int(win_mult),
        "added": int(added if added is not None else win_mult),
    }
    gamestate.book.add_event(event)


def shooter_event(gamestate, hits, added, win_mult):
    """MARK: the last-reel shooter fired at every premium.

    hits:    premium cells that were shot (padding-adjusted rows).
    added:   WIN multi gained this trigger (always 1).
    winMult: stacked WIN multiplier AFTER this trigger.
    """
    event = {
        "index": len(gamestate.book.events),
        "type": "shooter",
        "reel": gamestate.config.num_reels - 1,
        "hits": [_padrow(c) for c in hits],
        "added": int(added),
        "winMult": int(win_mult),
    }
    gamestate.book.add_event(event)


def win_mult_event(gamestate, added, total, source):
    """HUD tick: the stacked WIN multiplier just changed."""
    event = {
        "index": len(gamestate.book.events),
        "type": "winMult",
        "added": int(added),
        "winMult": int(total),
        "source": source,
    }
    gamestate.book.add_event(event)


def specials_wild_event(gamestate, cells):
    """Every remaining feature symbol transformed into the revolver WILD."""
    event = {
        "index": len(gamestate.book.events),
        "type": "specialsWild",
        "cells": [_padrow(c) for c in cells],
    }
    gamestate.book.add_event(event)


def nudge_event(gamestate, symbol, base_mult, passed, win_mult, steps=None):
    """Legacy no-op name: the old sideways nudge was removed."""
    return
