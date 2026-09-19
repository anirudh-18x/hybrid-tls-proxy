import socket

PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8443

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 9000


def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((PROXY_HOST, PROXY_PORT))
    server.listen(5)

    print(f"[PROXY] Listening on {PROXY_HOST}:{PROXY_PORT}")
    print(f"[PROXY] Forwarding to {BACKEND_HOST}:{BACKEND_PORT}")

    while True:
        client_socket, client_address = server.accept()

        print(f"[PROXY] Client connected: {client_address}")

        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect((BACKEND_HOST, BACKEND_PORT))

        request = client_socket.recv(4096)

        print(f"[PROXY] Received {len(request)} bytes")

        backend_socket.sendall(request)

        response = backend_socket.recv(4096)

        print(f"[PROXY] Received {len(response)} bytes from backend")

        client_socket.sendall(response)

        backend_socket.close()
        client_socket.close()

        print("[PROXY] Connection completed")


if __name__ == "__main__":
    start_proxy()
