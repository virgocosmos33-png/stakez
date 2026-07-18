"""Minimal Scenario.com API client for Madam Mirror asset generation.

Reads credentials from scenariocrd.txt at the workspace root so keys are
never hardcoded in scripts. Docs: https://docs.scenario.com/
"""

from __future__ import annotations

import base64
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[4]
CRED_FILE = WORKSPACE / "scenariocrd.txt"
API_ROOT = "https://api.cloud.scenario.com/v1"


def _load_credentials() -> tuple[str, str]:
    api_key = secret = None
    for line in CRED_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.lower().startswith("api key:"):
            api_key = line.split(":", 1)[1].strip()
        elif line.lower().startswith("secret key:"):
            secret = line.split(":", 1)[1].strip()
    if not api_key or not secret:
        raise RuntimeError("scenariocrd.txt is missing api/secret key lines")
    return api_key, secret


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
