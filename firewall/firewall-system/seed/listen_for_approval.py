# listen_for_approval_secure.py
import socket
import traceback
import sys
from utils.noise_utils_server import (
    ensure_responder_keys,
    noise_responder_handshake,
    recv_frame,
    send_frame,
)
from .generate_new_objects import generate_new_objects
# python3 -m seed.listen_for_approval

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 6003
SOCKET_TIMEOUT = 20.0

def handle_connection(conn, addr):
    print(f"[+] New connection from {addr}")
    responder_sk, responder_pk = ensure_responder_keys()

    try:
        # perform responder handshake
        nc = noise_responder_handshake(conn, responder_sk, timeout=SOCKET_TIMEOUT)
        print("[+] Noise handshake finished (responder)")

        # receive control message - USE decrypt() NOT read_message()
        enc_control = recv_frame(conn, timeout=SOCKET_TIMEOUT)
        if not enc_control:
            print("[!] No control frame received, closing")
            return
        control_plain = nc.decrypt(enc_control).decode()
        print(f"[+] Control: {control_plain}")

        if control_plain.strip() == "Approved":
            # optional commit-range from client
            enc_range = recv_frame(conn, timeout=SOCKET_TIMEOUT)
            if enc_range:
                try:
                    range_plain = nc.decrypt(enc_range).decode()
                    old_sha, new_sha = range_plain.split()
                    print(f"[+] Received range: {old_sha} -> {new_sha}")
                except Exception:
                    old_sha, new_sha = None, None
                    print("[!] Failed to parse range from client")
            else:
                old_sha, new_sha = None, None

            # generate JSON payload and send encrypted
            try:
                payload_text = generate_new_objects(old_sha, new_sha)
                enc_payload = nc.encrypt(payload_text.encode())
                send_frame(conn, enc_payload, timeout=SOCKET_TIMEOUT)
                print("[+] Sent payload")

            except Exception as e:
                print(f"[!] Failed to generate/send payload: {e}")
                traceback.print_exc()

        else:
            print("[+] Push denied. No payload requested.")

    except Exception as e:
        print(f"[!] Connection handler error: {e}", file=sys.stderr)
        traceback.print_exc()

    finally:
        conn.close()
        print(f"[+] Closed connection from {addr}")


def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LISTEN_HOST, LISTEN_PORT))
        s.listen(5)
        print(f"[+] Listening on {LISTEN_HOST}:{LISTEN_PORT}")

        while True:
            conn, addr = s.accept()
            handle_connection(conn, addr)

if __name__ == "__main__":
    try:
        serve()
    except KeyboardInterrupt:
        print("Shutting down")
