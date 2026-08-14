"""Deprecated wrapper — the room is now plate + lamp sprites.

Run tools/bake_saloon_room.py (this file just forwards).
"""

from __future__ import annotations

import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    runpy.run_path(os.path.join(HERE, "bake_saloon_room.py"), run_name="__main__")
