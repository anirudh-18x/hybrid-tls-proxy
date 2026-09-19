import socket
import ssl
import subprocess
import os
import json
import time
from pathlib import Path


PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8443

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 9443

CERT_FILE = "certs/server.crt"
KEY_FILE = "certs/server.key"

RESULT_FILE = Path("results/latest.json")


# ---------------------------------------------------------
# TLS MODE
# ---------------------------------------------------------

MODE = os.getenv("TLS_MODE", "classical")

if MODE == "hybrid":
    TLS_GROUP = "X25519MLKEM768"
else:
    TLS_GROUP = "X25519"


# ---------------------------------------------------------
# TLS SERVER CONTEXT
# ---------------------------------------------------------

def create_server_context():

    context = ssl.SSLContext(
        ssl.PROTOCOL_TLS_SERVER
    )

    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3

    context.load_cert_chain(
        certfile=CERT_FILE,
        keyfile=KEY_FILE
    )

    return context


# ---------------------------------------------------------
# SAVE METRICS
# ---------------------------------------------------------

def save_metrics(
    mode,
    tls_version,
    cipher,
    backend_group,
    request_bytes,
    response_bytes,
    handshake_time
):

    data = {

        "mode": mode,

        "tls_version": tls_version,

        "backend_group": backend_group,

        "authentication": "RSA-PSS",

        "cipher": cipher,

        "request_bytes": request_bytes,

        "response_bytes": response_bytes,

        "handshake_time_ms": round(
            handshake_time * 1000,
            2
        )

    }

    RESULT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    RESULT_FILE.write_text(
        json.dumps(
            data,
            indent=2
        )
    )

    print(
        f"[PROXY] Metrics saved to "
        f"{RESULT_FILE}"
    )


# ---------------------------------------------------------
# START PROXY
# ---------------------------------------------------------

def start_proxy():

    tls_context = create_server_context()

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (PROXY_HOST, PROXY_PORT)
    )

    server.listen(5)

    print("=" * 55)
    print("[PROXY] Hybrid TLS Proxy")
    print("=" * 55)
    print(
        f"[PROXY] Listening: "
        f"{PROXY_HOST}:{PROXY_PORT}"
    )

    print(
        f"[PROXY] TLS Mode: "
        f"{MODE}"
    )

    print(
        f"[PROXY] Backend Group: "
        f"{TLS_GROUP}"
    )

    print("=" * 55)

    while True:

        client_socket, client_address = server.accept()

        print(
            f"\n[PROXY] Client connected: "
            f"{client_address}"
        )

        try:

            # -----------------------------------------
            # CLIENT → PROXY TLS
            # -----------------------------------------

            handshake_start = time.perf_counter()

            tls_client = tls_context.wrap_socket(
                client_socket,
                server_side=True
            )

            handshake_time = (
                time.perf_counter()
                - handshake_start
            )

            tls_version = tls_client.version()

            cipher_info = tls_client.cipher()

            cipher = cipher_info[0]

            print(
                "[PROXY] Client TLS established"
            )

            print(
                f"[PROXY] TLS version: "
                f"{tls_version}"
            )

            print(
                f"[PROXY] Cipher: "
                f"{cipher}"
            )

            # -----------------------------------------
            # PROXY → BACKEND TLS
            # -----------------------------------------

            openssl = subprocess.Popen(
                [
                    "openssl",
                    "s_client",

                    "-connect",
                    f"{BACKEND_HOST}:{BACKEND_PORT}",

                    "-tls1_3",

                    "-groups",
                    TLS_GROUP,

                    "-quiet",
                ],

                stdin=subprocess.PIPE,

                stdout=subprocess.PIPE,

                stderr=subprocess.PIPE,
            )

            print(
                "[PROXY] Backend TLS "
                "connection started"
            )

            print(
                f"[PROXY] Backend group: "
                f"{TLS_GROUP}"
            )

            # -----------------------------------------
            # RECEIVE HTTP REQUEST
            # -----------------------------------------

            request = tls_client.recv(8192)

            request_bytes = len(request)

            print(
                f"[PROXY] HTTP request received: "
                f"{request_bytes} bytes"
            )

            # -----------------------------------------
            # SEND REQUEST TO BACKEND
            # -----------------------------------------

            openssl.stdin.write(request)

            openssl.stdin.flush()

            print(
                "[PROXY] Request sent to backend"
            )

            # -----------------------------------------
            # RECEIVE BACKEND RESPONSE
            # -----------------------------------------

            response = openssl.stdout.read(8192)

            response_bytes = len(response)

            print(
                f"[PROXY] Backend response: "
                f"{response_bytes} bytes"
            )

            # -----------------------------------------
            # SEND RESPONSE TO CLIENT
            # -----------------------------------------

            tls_client.sendall(response)

            print(
                "[PROXY] Response sent to client"
            )

            # -----------------------------------------
            # SAVE METRICS
            # -----------------------------------------

            save_metrics(

                mode=MODE,

                tls_version=tls_version,

                cipher=cipher,

                backend_group=TLS_GROUP,

                request_bytes=request_bytes,

                response_bytes=response_bytes,

                handshake_time=handshake_time
            )

            print(
                "[PROXY] Request completed"
            )

            # -----------------------------------------
            # CLEANUP
            # -----------------------------------------

            openssl.stdin.close()

            openssl.terminate()

            tls_client.close()

        except Exception as error:

            print(
                f"[PROXY] Error: {error}"
            )

        finally:

            try:
                client_socket.close()

            except Exception:
                pass


if __name__ == "__main__":

    start_proxy()
