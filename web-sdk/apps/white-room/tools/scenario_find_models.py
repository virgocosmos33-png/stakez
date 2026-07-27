"""Search Scenario public models for the generators used on the previous game."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

TERMS = ["p-image", "seedream", "audio", "video", "veo", "kling", "elevenlabs", "lyria", "sfx"]

for term in TERMS:
    try:
        result = s.request("GET", f"/models/public?pageSize=6&search={term}")
        models = result.get("models", [])
        print(f"== {term} ({len(models)})")
        for m in models:
            caps = ",".join(m.get("capabilities", [])[:6])
            print(f"  {m.get('id')} | {m.get('name')!r} | type={m.get('type')} | caps={caps}")
    except Exception as error:  # noqa: BLE001
        print(f"== {term} ERROR: {error}")
