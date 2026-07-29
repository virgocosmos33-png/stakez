"""Custom book events for THE WHITE ROOM (Wild Reel + Unlocked Slots + 3-level bonuses).

All row indices are emitted padding-adjusted (+1), matching reveal/winInfo.
The legacy xMirror "split" events (mirrorBurst / madamsEye) have been removed.
"""


def bonus_level_event(gamestate):
    """Announces which bonus level (1/2/3) was awarded, straight after freeSpinTrigger."""
    event = {
        "index": len(gamestate.book.events),
        "type": "bonusLevel",
        "level": gamestate.fs_level,
        "name": gamestate.config.bonus_levels[gamestate.fs_level]["name"],
        # no level pre-haunts cells anymore; field kept for the frontend type
        "startHaunted": [],
    }
    gamestate.book.add_event(event)


def wild_reel_event(gamestate):
    """Wild Reel: bottom-slot symbols grow their middle reel into a rising wild.

    reels: one entry per triggered middle reel:
      - reel: reel index (0-based)
      - baseRows: the reel's normal height before the feature
      - added: how many wild rows rose from the bottom slot
      - cells: the risen wild cells (padding-adjusted row + multiplier)
      - ways: what the whole column is now worth on its own. A reel grown to
        its full four rows is worth 4 before any multiplier, so this never
        reads below 4 — it is the number the column shows the player.
    The frontend uses this to extend the reel to `baseRows + added` rows,
    pushing the existing symbols up and dropping WILDs into the new bottom cells.
    """
    cfg = getattr(gamestate.config, "wild_reel_config", {}) or {}
    reels = []
    for info in gamestate.cell_seal_info:
        reels.append(
            {
                "reel": info["reel"],
                "baseRows": info["base_rows"],
                "added": info["added"],
                "cells": [
                    {"row": cell["row"] + 1, "multiplier": cell["mult"]}
                    for cell in info["cells"]
                ],
                "ways": gamestate.reel_ways(info["reel"]),
            }
        )
    event = {
        "index": len(gamestate.book.events),
        "type": "wildReel",
        "label": cfg.get("label", "Wild Reel"),
        "reels": reels,
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def unlocked_slots_event(gamestate):
    """Bonus board expansion: the reserved slots unlock and fill with premiums
    or wilds, growing the board toward 6/7 reels.

    level: current bonus level (1/2/3).
    unlocked: which slot groups are open this level ("bottom"/"right"/"left").
    bottom: premiums dropped into the bottom slots of middle reels 1-3
      - reel, row (padding-adjusted board row), name.
    sides: the RIGHT/LEFT columns that became extra reels
      - side: "right" | "left"
      - reel: board reel index the column was appended at
      - cells: filled slots top-to-bottom
          - row: padding-adjusted board index (matches winInfo positions)
          - slotRow: visual slot row (0-based, top-to-bottom)
          - name, multiplier (wild slots only)
    totalWays: ways count of the fully-expanded board.
    """
    info = gamestate.slot_info or {}
    cfg = getattr(gamestate.config, "unlocked_slot_config", {}) or {}

    bottom = [
        {"reel": c["reel"], "row": c["row"] + 1, "name": c["name"]}
        for c in info.get("bottom", [])
    ]
    sides = []
    for s in info.get("sides", []):
        cells = []
        for board_idx, c in enumerate(s["cells"]):
            cell = {"row": board_idx + 1, "slotRow": c["row"], "name": c["name"]}
            if c.get("mult", 1) and c["name"] in gamestate.config.special_symbols.get("wild", []):
                cell["multiplier"] = c["mult"]
            cells.append(cell)
        sides.append({"side": s["side"], "reel": s["reel"], "cells": cells})

    event = {
        "index": len(gamestate.book.events),
        "type": "unlockedSlots",
        "label": cfg.get("label", "Unlocked Slots"),
        "level": info.get("level", gamestate.fs_level),
        "unlocked": info.get("unlocked", []),
        "bottom": bottom,
        "sides": sides,
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def stretch_reel_event(gamestate):
    """STRETCH: one or more reels were stretched, giving their symbols extra x-ways.

    reels: one entry per stretched reel:
      - reel: reel index (0-based) - also the bottom cell that dropped STRETCH
      - mode: "wild" (whole reel is wild -> wild column + centred total) or
              "normal" (real symbols stretch in place, each shows its x-ways)
      - baseRows: reel height
      - reelWays: this reel's total ways (sum of its per-symbol multipliers)
      - cells: every symbol on the reel (padding-adjusted row + its multiplier)
    """
    cfg = getattr(gamestate.config, "stretch_config", {}) or {}
    reels = []
    for info in gamestate.stretch_info:
        reels.append(
            {
                "reel": info["reel"],
                "mode": info.get("mode", "normal"),
                "baseRows": info["base_rows"],
                "reelWays": info.get("reel_ways", info["base_rows"]),
                "cells": [{"row": c["row"] + 1, "multiplier": c["multiplier"]} for c in info["cells"]],
            }
        )
    event = {
        "index": len(gamestate.book.events),
        "type": "stretchReel",
        "label": cfg.get("label", "Stretch"),
        "reels": reels,
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def clone_symbol_event(gamestate):
    """CLONE: every copy of one chosen symbol turned into a premium.

    cell: where the CLONE card landed - a BOTTOM cell {"reel"} or a SIDE slot
      {"side", "slotRow"}.
    from / to: the source symbol and the premium it became.
    cells: the converted board cells (padding-adjusted row).
    """
    info = gamestate.clone_info or {}
    cfg = getattr(gamestate.config, "clone_config", {}) or {}
    event = {
        "index": len(gamestate.book.events),
        "type": "cloneSymbol",
        "label": cfg.get("label", "Clone"),
        "cell": info.get("cell") or {"reel": info.get("reel")},
        "from": info.get("from"),
        "to": info.get("to"),
        "cells": [{"reel": c["reel"], "row": c["row"] + 1} for c in info.get("cells", [])],
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


def split_symbols_event(gamestate):
    """SPLIT: one winning symbol type had +1..+10 ways ADDED to each of its
    winning cells.

    cell: where the SPLIT card landed - a BOTTOM cell {"reel"} or a SIDE slot
      {"side", "slotRow"}.
    symbol: the winning symbol that was split.
    mult: the split factor applied.
    cells: the affected board cells (padding-adjusted row + resulting
      multiplier). Cells on a wild column carry "wild": true so the frontend
      reads them as the column being torn through rather than as a symbol win.
    wildReels: every wild column the split went through, with what each is now
      worth, so its badge can be re-stamped.
    """
    info = gamestate.split_info or {}
    cfg = getattr(gamestate.config, "split_config", {}) or {}
    event = {
        "index": len(gamestate.book.events),
        "type": "splitSymbols",
        "label": cfg.get("label", "Split"),
        "cell": info.get("cell") or {"reel": info.get("reel")},
        "symbol": info.get("symbol"),
        "mult": info.get("mult"),
        "cells": [
            {
                "reel": c["reel"],
                "row": c["row"] + 1,
                "multiplier": c["multiplier"],
                **({"wild": True} if c.get("wild") else {}),
            }
            for c in info.get("cells", [])
        ],
        "wildReels": info.get("wild_reels", []),
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)
