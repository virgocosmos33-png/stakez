"""List every video-capable model on the Scenario account (id, name, caps)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

seen: dict[str, dict] = {}
cursor = ""
for _page in range(10):
    path = "/models/public?pageSize=100" + (f"&paginationToken={cursor}" if cursor else "")
    result = s.request("GET", path)
    for model in result.get("models", []):
        seen[model.get("id")] = model
    cursor = result.get("nextPaginationToken") or ""
    if not cursor:
        break

video = [m for m in seen.values() if any("vid" in c for c in m.get("capabilities", []))]
print(f"total models: {len(seen)}, video-capable: {len(video)}")
for m in video:
    caps = ",".join(m.get("capabilities", []))
    name = str(m.get("name")).encode("ascii", "replace").decode()
    print(f"  {m.get('id')} | {name!r} | caps={caps}")
