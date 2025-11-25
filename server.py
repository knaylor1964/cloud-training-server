import http.server
import socketserver

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            # Send response code 200 (OK)
            self.send_response(200)
            # Tell the browser we are sending JSON
            self.send_header("Content-type", "application/json")
            self.end_headers()
            # Send a simple JSON message
            self.wfile.write(b'{"ok": true, "message": "Server is working"}')
        else:
            # For all other paths, use normal file handling
            super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server running on port", PORT)
    httpd.serve_forever()
