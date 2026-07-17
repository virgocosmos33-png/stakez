"""Custom book events for Madam Mirror (xMirror feature + 3-level bonuses).

All row indices are emitted padding-adjusted (+1), matching reveal/winInfo.
"""


def mirror_burst_event(gamestate):
    """Haunted Mirrors crack and reflect their neighbors into apparitions.

    mirrors: one entry per Haunted Mirror on the reveal:
      - mirror: cell the HM landed on
      - reflected: the 1-4 hit neighbor cells with their new apparition totals
        (stacking levels: total after adding onto an already-haunted cell)
      - mirrorBecomes: symbol the mirror resolves into (highest-paying neighbor)
    totalWays: ways count of the resolved board (product of per-reel apparition sums).
    """
    mirrors = []
    for info in gamestate.mirror_info:
        mirrors.append(
            {
                "mirror": {"reel": info["reel"], "row": info["row"] + 1},
                "reflected": [
                    {"reel": cell["reel"], "row": cell["row"] + 1, "apparitions": cell["apparitions"]}
                    for cell in info["reflected"]
                ],
                "mirrorBecomes": {"name": info["becomes"]},
            }
        )

    event = {
        "index": len(gamestate.book.events),
        "type": "mirrorBurst",
        "mirrors": mirrors,
        "totalWays": gamestate.count_board_ways(),
    }
    gamestate.book.add_event(event)


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
