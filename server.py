import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Break the URL into path and query string
        parsed = urlparse(self.path)

        # /status endpoint
        if parsed.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            data = {"ok": True, "message": "Server is working"}
            self.wfile.write(json.dumps(data).encode("utf-8"))

        # /money endpoint: y = m*x + b
        elif parsed.path == "/money":
            # Parse query parameters: ?m=20&x=5&b=100
            qs = parse_qs(parsed.query)

            def get_number(name, default=0.0):
                try:
                    return float(qs.get(name, [default])[0])
                except ValueError:
                    return default

            m = get_number("m", 0.0)
            x = get_number("x", 0.0)
            b = get_number("b", 0.0)

            y = m * x + b

            result = {"m": m, "x": x, "b": b, "y": y}

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))

        # Everything else → normal file handling
        else:
            super().do_GET()


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server running on port", PORT)
    httpd.serve_forever()
