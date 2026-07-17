"""Custom book events for the 4x5 lines game (xNudge wild feature)."""

from src.events.events import json_ready_sym


def wild_nudge_event(gamestate):
    """Emitted after the reveal: describes the wild stack nudging into place.

    The reveal event shows the misaligned stack (top `nudges` wilds hidden above
    the window). The client animates `nudges` downward steps, then displays the
    final all-wild reel where every wild carries the accumulated multiplier.
    """
    special_attributes = list(gamestate.config.special_symbols.keys())
    reel = gamestate.nudge_info["reel"]
    final_reel = [json_ready_sym(sym, special_attributes) for sym in gamestate.board[reel]]

    event = {
        "index": len(gamestate.book.events),
        "type": "wildNudge",
        "reel": reel,
        "nudges": gamestate.nudge_info["nudges"],
        "multiplier": gamestate.nudge_info["multiplier"],
        "finalReel": final_reel,
    }
    gamestate.book.add_event(event)
