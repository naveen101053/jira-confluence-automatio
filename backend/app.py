import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if urlsplit(self.path).path != "/health":
            self.send_error(404, "Not Found")
            return

        payload = json.dumps(
            {
                "status": "ok",
                "service": "jira-report-backend",
                "mode": "health-only",
                "reporting": "not-implemented",
            }
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    port = int(os.environ.get("PORT", "8000"))
    if not 1 <= port <= 65535:
        raise ValueError("PORT must be between 1 and 65535")

    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    logging.info("Health-only backend listening on port %s", port)
    server.serve_forever()


if __name__ == "__main__":
    main()
