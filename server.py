import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path and query string
        parsed = urlparse(self.path)

        # /status endpoint
        if parsed.path == "/status":
            data = {"ok": True, "message": "Server is working"}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
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

            m = get_number("m", 0.0)    # hourly wage
            hours = get_number("x", 0.0)  # total hours worked
            b = get_number("b", 0.0)    # bonus / tips

            # Overtime rules: time-and-a-half over 40 hours
            regular_hours = min(hours, 40.0)
            overtime_hours = max(hours - 40.0, 0.0)

            regular_pay = regular_hours * m
            overtime_pay = overtime_hours * m * 1.5

            gross = regular_pay + overtime_pay + b  # total before tax

            result = {
                "m": m,
                "hours": hours,
                "bonus": b,
                "regular_hours": regular_hours,
                "overtime_hours": overtime_hours,
                "regular_pay": regular_pay,
                "overtime_pay": overtime_pay,
                "y": gross,  # total weekly gross
            }

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
