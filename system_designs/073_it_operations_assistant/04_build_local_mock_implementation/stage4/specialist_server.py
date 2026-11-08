"""Optional separate-process LOCAL specialist. Plain HTTP JSON, not A2A."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json


class SpecialistHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/diagnose":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 2048:
                self.send_error(413)
                return
            request = json.loads(self.rfile.read(length))
            ids = request["evidence_ids"]
            if request["service"] != "checkout-api" or not isinstance(ids, list):
                self.send_error(400)
                return
        except (ValueError, KeyError, TypeError):
            self.send_error(400)
            return
        result = {
            "status": "hypothesis_only",
            "specialist": "mock-database-specialist",
            "suggestion": "Inspect database connection saturation; no database metrics were supplied.",
            "evidence_ids": [eid for eid in ids if eid == "METRIC-07"],
        }
        encoded = json.dumps(result).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    print("Local specialist at http://127.0.0.1:8765/diagnose (not A2A)")
    ThreadingHTTPServer(("127.0.0.1", 8765), SpecialistHandler).serve_forever()
