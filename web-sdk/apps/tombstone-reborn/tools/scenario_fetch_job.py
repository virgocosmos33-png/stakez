"""Fetch a Scenario job's status; if successful, download its asset(s).

Usage: python tools/scenario_fetch_job.py <jobId> [out_name.mp4] [--all]

Without --all only the first asset is saved (out_name verbatim). With --all every
asset of the job is saved as out_name with an index suffix, which is what a
multi-variant image job (numOutputs > 1) needs so the variants can be compared.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import scenario_api as s  # noqa: E402

OUT = Path(__file__).parent / "scenario_out"

args = [a for a in sys.argv[1:] if not a.startswith("--")]
download_all = "--all" in sys.argv
job_id = args[0]
out_name = args[1] if len(args) > 1 else None

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
    wanted = asset_ids if download_all else asset_ids[:1]
    stem, suffix = Path(out_name).stem, Path(out_name).suffix
    for index, asset_id in enumerate(wanted, start=1):
        asset = s.request("GET", f"/assets/{asset_id}").get("asset", {})
        dest = OUT / (out_name if len(wanted) == 1 else f"{stem}_{index}{suffix}")
        s.download(asset["url"], dest)
        print(f"saved {dest} ({dest.stat().st_size:,} B)")
