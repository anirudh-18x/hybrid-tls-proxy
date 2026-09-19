from http.server import HTTPServer, BaseHTTPRequestHandler


class BackendHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        message = b"Hello from the Hybrid TLS Backend!"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()

        self.wfile.write(message)

    def log_message(self, format, *args):
        print(f"[BACKEND] {self.address_string()} - {format % args}")


server = HTTPServer(("127.0.0.1", 9000), BackendHandler)

print("[BACKEND] Server started on http://127.0.0.1:9000")

server.serve_forever()
