"""Local preview server for VFXPACKSHEETS: static files plus pack edits."""
from __future__ import annotations

import argparse
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from edit_pack import delete_frames, delete_pack, set_curve, set_loop  # noqa: E402
from paths import resolve_dest  # noqa: E402

HOST = "127.0.0.1"
PORT = 8791
MAX_BODY = 64 * 1024


class PreviewHandler(SimpleHTTPRequestHandler):
    dest: Path

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send_json(self, code: int, payload: dict) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        if length > MAX_BODY:
            raise ValueError("Request is too large")
        raw = self.rfile.read(length)
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object")
        return data

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/status":
            self._send_json(200, {"writable": True, "dest": str(self.dest)})
            return
        super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            body = self._read_json()
        except (ValueError, json.JSONDecodeError) as err:
            self._send_json(400, {"error": str(err)})
            return
        slug = str(body.get("id") or "").strip()
        try:
            if path == "/api/pack/delete":
                names = body.get("frames") or []
                if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
                    raise ValueError("frames must be a list of filenames")
                entry = delete_frames(self.dest, slug, names)
                self._send_json(200, {"ok": True, "pack": entry})
                return
            if path == "/api/pack/remove":
                result = delete_pack(self.dest, slug)
                self._send_json(200, {"ok": True, "removed": result})
                return
            if path == "/api/pack/loop":
                start = body.get("loopStart", None)
                end = body.get("loopEnd", None)
                if start is not None:
                    start = int(start)
                if end is not None:
                    end = int(end)
                entry = set_loop(self.dest, slug, start, end)
                self._send_json(200, {"ok": True, "pack": entry})
                return
            if path == "/api/pack/curve":
                curve = str(body.get("speedCurve") or body.get("speed_curve") or "").strip()
                phases = body.get("framePhases", body.get("frame_phases"))
                scales = body.get("frameScales", body.get("frame_scales"))
                entry = set_curve(self.dest, slug, curve, phases, scales)
                self._send_json(200, {"ok": True, "pack": entry})
                return
        except ValueError as err:
            self._send_json(400, {"error": str(err)})
            return
        except OSError:
            self._send_json(500, {"error": "Could not write the pack"})
            return
        self._send_json(404, {"error": "Unknown API path"})


def serve(dest: Path, host: str = HOST, port: int = PORT) -> None:
    dest = dest.resolve()
    dest_s = str(dest)
    library = dest

    class Bound(PreviewHandler):
        dest = library

        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=dest_s, **kwargs)

    httpd = ThreadingHTTPServer((host, port), Bound)
    print(f"VFX preview  http://{host}:{port}/viewer.html", flush=True)
    print(f"library      {dest}", flush=True)
    httpd.serve_forever()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dest", type=Path, default=None)
    p.add_argument("--host", default=HOST)
    p.add_argument("--port", type=int, default=PORT)
    args = p.parse_args()
    dest = resolve_dest(args.dest)
    if args.host not in ("127.0.0.1", "localhost"):
        raise SystemExit("serve_preview.py binds localhost only")
    serve(dest, args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
