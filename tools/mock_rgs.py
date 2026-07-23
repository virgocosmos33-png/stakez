"""Local mock of the Stake Engine RGS for testing the frontend without uploading.

Serves /wallet/authenticate, /wallet/play, /wallet/end-round and /bet/event
over HTTPS (the frontend fetcher hardcodes https://) using real books sampled
from the math build in library/publish_files, weighted by the lookup tables -
so bets, autobet, feature buys and win distribution behave like production.

Usage:
    cd math-sdk && env/Scripts/python.exe ../tools/mock_rgs.py [game] [port]

    game: folder name under math-sdk/games (default 0_1_madam_mirror)
    port: https port (default 7777)

Then ONCE per browser: open https://localhost:<port>/health and accept the
self-signed certificate warning. After that open the game with:

    http://localhost:3001/?sessionID=dev&rgs_url=localhost:<port>&lang=en&currency=USD
"""

import csv
import io
import json
import random
import ssl
import subprocess
import sys
import threading
from bisect import bisect_right
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from itertools import accumulate
from pathlib import Path

try:
    import zstandard
except ImportError:
    sys.exit("zstandard missing - run with math-sdk/env/Scripts/python.exe")

ROOT = Path(__file__).resolve().parent.parent
GAME = sys.argv[1] if len(sys.argv) > 1 else "0_1_madam_mirror"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 7777
PUBLISH = ROOT / "math-sdk" / "games" / GAME / "library" / "publish_files"
CACHE_DIR = Path(__file__).resolve().parent / "mock_rgs_cache" / GAME
CERT_DIR = Path(__file__).resolve().parent / "mock_rgs_cache" / "cert"
POOL_SIZE = 400          # weighted book sample kept in memory per mode
START_BALANCE = 10_000_000_000  # $10,000 in API units (1e6 = $1)

MODES = {m["name"]: m for m in json.loads((PUBLISH / "index.json").read_text())["modes"]}

# ---------------------------------------------------------------- book pools


class ModePool:
    """Weighted sample of real books for one bet mode, extracted lazily."""

    def __init__(self, name: str):
        self.name = name
        self.meta = MODES[name]
        self.books: list[dict] = []
        self.lock = threading.Lock()

    def _sample_ids(self) -> list[int]:
        ids, weights = [], []
        with open(PUBLISH / self.meta["weights"], newline="") as f:
            for row in csv.reader(f):
                ids.append(int(row[0]))
                weights.append(int(row[1]))
        cum = list(accumulate(weights))
        total = cum[-1]
        return [ids[bisect_right(cum, random.randrange(total))] for _ in range(POOL_SIZE)]

    def _load(self):
        cache = CACHE_DIR / f"{self.name}.jsonl"
        if cache.exists():
            self.books = [json.loads(l) for l in cache.read_text(encoding="utf-8").splitlines() if l]
            print(f"[{self.name}] {len(self.books)} books from cache")
            return

        wanted = set(self._sample_ids())
        print(f"[{self.name}] extracting {len(wanted)} unique books from "
              f"{self.meta['events']} (first time only, can take a minute)...")
        found = {}
        with open(PUBLISH / self.meta["events"], "rb") as f:
            reader = zstandard.ZstdDecompressor().stream_reader(f)
            for line in io.TextIOWrapper(reader, encoding="utf-8"):
                # cheap id sniff before full json parse
                head = line[:24]
                try:
                    book_id = int(head.split('"id":')[1].split(",")[0])
                except (IndexError, ValueError):
                    book_id = json.loads(line)["id"]
                if book_id in wanted:
                    found[book_id] = line
                    if len(found) == len(wanted):
                        break
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache.write_text("".join(found.values()), encoding="utf-8")
        self.books = [json.loads(l) for l in found.values()]
        print(f"[{self.name}] extracted {len(self.books)} books")

    def draw(self) -> dict:
        with self.lock:
            if not self.books:
                self._load()
        return random.choice(self.books)


POOLS = {name: ModePool(name) for name in MODES}

# ---------------------------------------------------------------- session state

SESSIONS: dict[str, dict] = {}
SESSION_LOCK = threading.Lock()
BET_ID = [1000]


def session(session_id: str) -> dict:
    with SESSION_LOCK:
        return SESSIONS.setdefault(session_id, {"balance": START_BALANCE, "round": None})


# ---------------------------------------------------------------- http handler

BET_LEVELS = [int(v * 1_000_000) for v in
              (0.1, 0.2, 0.4, 0.6, 0.8, 1, 2, 3, 4, 5, 10, 20, 40, 60, 80, 100,
               200, 400, 600, 800, 1000)]

CONFIG = {
    "gameID": GAME,
    "minBet": BET_LEVELS[0],
    "maxBet": BET_LEVELS[-1],
    "stepBet": 100_000,
    "defaultBetLevel": 1_000_000,
    "betLevels": BET_LEVELS,
    "betModes": {},
    "jurisdiction": {
        "socialCasino": False,
        "disabledFullscreen": False,
        "disabledTurbo": False,
        "disabledSuperTurbo": False,
        "disabledAutoplay": False,
        "disabledSlamstop": False,
        "disabledSpacebar": False,
        "disabledBuyFeature": False,
        "displayNetPosition": False,
        "displayRTP": False,
        "displaySessionTimer": False,
        "minimumRoundDuration": 0,
    },
}


class Handler(BaseHTTPRequestHandler):
    # keep-alive: reuse connections so the browser doesn't re-handshake TLS
    # on every request (all responses carry Content-Length)
    protocol_version = "HTTP/1.1"
    timeout = 30

    def log_message(self, fmt, *args):  # quieter default log
        # command/path are unset when a keep-alive connection times out idle
        cmd = getattr(self, "command", None)
        if cmd is None:
            return  # idle keep-alive close - not interesting
        import datetime
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"  {ts} {cmd} {getattr(self, 'path', '?')} {args[1] if len(args) > 1 else ''}")

    def _send(self, payload, status=200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/health"):
            self._send({"status": "ok", "mockRgs": True})
        else:
            self._send({"error": "not found"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            body = {}
        sess = session(str(body.get("sessionID") or "default"))

        if self.path == "/wallet/authenticate":
            round_ = sess["round"] if sess["round"] and sess["round"]["active"] else None
            self._send({
                "balance": {"amount": sess["balance"], "currency": "USD"},
                "config": CONFIG,
                "round": round_,
            })

        elif self.path == "/wallet/play":
            mode = str(body.get("mode") or "base").lower()
            if mode not in POOLS:
                self._send({"error": f"unknown mode {mode}"})
                return
            amount = int(body.get("amount") or 0)
            cost = int(round(amount * MODES[mode]["cost"]))
            if cost <= 0 or cost > sess["balance"]:
                self._send({"error": "insufficient funds",
                            "message": f"cost {cost} > balance {sess['balance']}"})
                return
            book = POOLS[mode].draw()
            pm = float(book.get("payoutMultiplier") or 0)
            BET_ID[0] += 1
            sess["balance"] -= cost
            sess["round"] = {
                "betID": BET_ID[0],
                "amount": amount,
                "payout": int(round(amount * pm)),
                "payoutMultiplier": pm,
                "active": True,
                "state": book["events"],
                "mode": mode,
                "event": None,
            }
            print(f"  -> bet #{BET_ID[0]} session={body.get('sessionID')} mode={mode} "
                  f"cost=${cost / 1e6:g} win={pm}x balance=${sess['balance'] / 1e6:g}")
            self._send({
                "balance": {"amount": sess["balance"], "currency": "USD"},
                "round": sess["round"],
            })

        elif self.path == "/wallet/end-round":
            if sess["round"] and sess["round"]["active"]:
                sess["balance"] += sess["round"]["payout"]
                sess["round"]["active"] = False
            self._send({"balance": {"amount": sess["balance"], "currency": "USD"}})

        elif self.path == "/bet/event":
            if sess["round"]:
                sess["round"]["event"] = body.get("event")
            self._send({"event": body.get("event"), "status": "ok"})

        else:
            self._send({"error": f"no route {self.path}"}, 404)


# ---------------------------------------------------------------- tls + main


def ensure_cert() -> tuple[Path, Path]:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    cert, key = CERT_DIR / "cert.pem", CERT_DIR / "key.pem"
    if not (cert.exists() and key.exists()):
        print("generating self-signed localhost certificate...")
        # Git-for-Windows openssl can hang on console handles when spawned
        # from Python - detach stdin/stdout and wait on the output files
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
             "-keyout", str(key), "-out", str(cert), "-days", "3650",
             "-subj", "/CN=localhost",
             "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1"],
            check=True, stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60,
        )
    return cert, key


class TLSThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, addr, handler, ssl_context: ssl.SSLContext):
        self.ssl_context = ssl_context
        super().__init__(addr, handler)

    def handle_error(self, request, client_address):
        import traceback
        exc = sys.exception()
        # idle keep-alive closes and aborted handshakes are routine
        if isinstance(exc, (TimeoutError, ConnectionError, ssl.SSLError)):
            return
        traceback.print_exc()

    def finish_request(self, request, client_address):
        # TLS handshake must happen in the worker thread: wrapping the LISTEN
        # socket runs handshakes on the accept loop, so one stalled speculative
        # browser connection freezes every request behind it (this showed up as
        # betting suddenly hanging after a few rounds)
        try:
            tls = self.ssl_context.wrap_socket(request, server_side=True)
        except (ssl.SSLError, OSError):
            return  # aborted preconnect / cert probe - ignore
        self.RequestHandlerClass(tls, client_address, self)


def main():
    cert, key = ensure_cert()
    # warm the base pool in the background so the first spin is instant-ish
    if "base" in POOLS:
        threading.Thread(target=POOLS["base"].draw, daemon=True).start()

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=str(cert), keyfile=str(key))
    server = TLSThreadingHTTPServer(("0.0.0.0", PORT), Handler, ctx)

    print(f"\nmock RGS for {GAME} listening on https://localhost:{PORT}")
    print(f"1) open https://localhost:{PORT}/health once and accept the cert warning")
    print("2) open the game with:")
    print(f"   ?sessionID=dev&rgs_url=localhost:{PORT}&lang=en&currency=USD\n")
    server.serve_forever()


if __name__ == "__main__":
    main()
