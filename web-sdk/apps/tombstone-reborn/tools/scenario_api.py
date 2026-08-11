"""Minimal Scenario.com API client for Madam Mirror asset generation.

Credentials come from the panel app settings:
  game-builder/.scenario-settings.json  →  { "apiKey", "secretKey" }
Legacy fallback: repo-root scenariocrd.txt (api key: / secret key: lines).
Docs: https://docs.scenario.com/
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[4]
APP_SETTINGS = WORKSPACE / "game-builder" / ".scenario-settings.json"
LEGACY_TXT = WORKSPACE / "scenariocrd.txt"
# Keys kept outside the repo so they never land in a commit; the path is passed
# in by the operator (assets-raw/SCENARIO_REPLACE_STATUS.md documents the var).
CRED_TXT = Path(os.environ["SCENARIO_CRED_TXT"]) if os.environ.get("SCENARIO_CRED_TXT") else None
# Scenario dashboard export (id,secret) — same file the older tools use
LEGACY_CSV = Path(os.environ.get("SCENARIO_KEY_CSV", r"c:\Users\Emex33\Downloads\projectchimera.csv"))
API_ROOT = "https://api.cloud.scenario.com/v1"


def _read_key_secret_txt(path: Path) -> tuple[str, str] | None:
    api_key = secret = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.lower().startswith("api key:"):
            api_key = line.split(":", 1)[1].strip()
        elif line.lower().startswith("secret key:"):
            secret = line.split(":", 1)[1].strip()
    return (api_key, secret) if api_key and secret else None


def _load_credentials() -> tuple[str, str]:
    if CRED_TXT is not None and CRED_TXT.is_file():
        found = _read_key_secret_txt(CRED_TXT)
        if found:
            return found
    if APP_SETTINGS.is_file():
        try:
            data = json.loads(APP_SETTINGS.read_text(encoding="utf-8"))
            api_key = (data.get("apiKey") or "").strip()
            secret = (data.get("secretKey") or "").strip()
            if api_key and secret:
                return api_key, secret
        except (OSError, json.JSONDecodeError):
            pass
    # Legacy plaintext file (pre-app-settings)
    if LEGACY_TXT.is_file():
        found = _read_key_secret_txt(LEGACY_TXT)
        if found:
            return found
    # Dashboard CSV export: columns id,secret
    if LEGACY_CSV.is_file():
        import csv

        with LEGACY_CSV.open(encoding="utf-8") as f:
            row = next(csv.DictReader(f))
        api_key = (row.get("id") or "").strip()
        secret = (row.get("secret") or "").strip()
        if api_key and secret:
            return api_key, secret
    raise RuntimeError(
        "Scenario credentials missing — set SCENARIO_CRED_TXT to a file with "
        "'api key:' / 'secret key:' lines, save them in the panel "
        "(MCP / AI → Provider), or write game-builder/.scenario-settings.json"
    )


def _auth_header() -> str:
    api_key, secret = _load_credentials()
    token = base64.b64encode(f"{api_key}:{secret}".encode()).decode()
    return f"Basic {token}"


def request(method: str, path: str, payload: dict | None = None, timeout: int = 120):
    url = path if path.startswith("http") else f"{API_ROOT}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", _auth_header())
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        body = error.read().decode(errors="replace")
        raise RuntimeError(f"{method} {url} -> HTTP {error.code}: {body[:500]}") from error


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=300) as response:
        dest.write_bytes(response.read())
    return dest


def wait_for_job(job_id: str, poll_seconds: float = 4, timeout_seconds: int = 600) -> dict:
    """Poll a generation job until success/failure; returns the job payload."""
    started = time.time()
    while True:
        job = request("GET", f"/jobs/{job_id}")
        status = job.get("job", job).get("status")
        if status in ("success", "failure", "canceled"):
            return job
        if time.time() - started > timeout_seconds:
            raise TimeoutError(f"Scenario job {job_id} still {status} after {timeout_seconds}s")
        time.sleep(poll_seconds)


if __name__ == "__main__":
    me = request("GET", "/me")
    print(json.dumps(me, indent=1)[:800])
