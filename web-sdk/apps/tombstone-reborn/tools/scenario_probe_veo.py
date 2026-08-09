"""Print the inference parameter schema for candidate audio-capable video models."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

for model_id in ("model_veo3-1-fast", "model_veo3-1"):
    info = s.request("GET", f"/models/{model_id}")
    model = info.get("model", info)
    out = {
        "id": model.get("id"),
        "name": model.get("name"),
        "capabilities": model.get("capabilities"),
        "parameters": model.get("parameters") or model.get("inferenceParameters"),
        "schema": model.get("schema"),
    }
    text = json.dumps(out, indent=1, default=str)
    print(text.encode("ascii", "replace").decode()[:4000])
    print("=" * 60)
