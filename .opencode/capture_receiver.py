import json, hashlib, datetime, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

OUT = Path(r"W:\Legal\.opencode\browser_capture_results.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(n)
        try:
            obj = json.loads(body.decode("utf-8", errors="ignore"))
            with OUT.open("a", encoding="utf-8") as f:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())


if __name__ == "__main__":
    srv = HTTPServer(("127.0.0.1", 19876), H)
    print("listening", flush=True)
    srv.serve_forever()
