"""Fetch a Scenario job's status; if successful, download its first asset.

Usage: python tools/scenario_fetch_job.py <jobId> [out_name.mp4]
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

OUT = Path(__file__).parent / "scenario_out"

job_id = sys.argv[1]
out_name = sys.argv[2] if len(sys.argv) > 2 else None

job = s.request("GET", f"/jobs/{job_id}")
job_data = job.get("job", job)
status = job_data.get("status")
print(f"status: {status}")

if status != "success":
    print(json.dumps(job_data, indent=1, default=str).encode("ascii", "replace").decode()[:2500])
    raise SystemExit(1)

asset_ids = job_data.get("metadata", {}).get("assetIds") or []
print(f"assets: {asset_ids}")
if out_name and asset_ids:
    asset = s.request("GET", f"/assets/{asset_ids[0]}").get("asset", {})
    dest = OUT / out_name
    s.download(asset["url"], dest)
    print(f"saved {dest} ({dest.stat().st_size:,} B)")
