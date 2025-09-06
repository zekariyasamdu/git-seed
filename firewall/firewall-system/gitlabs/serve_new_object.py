import socket
import os
import traceback
import sys
import threading
# Update import path to go up one level to utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.noise_utils_server import (
    ensure_responder_keys,
    noise_responder_handshake,
    send_frame,
)
# Import firewall from utils
from utils.firewall import firewall

# OBJECTS_PATH = "/var/opt/gitlab/git-data/repositories/@hashed/6b/86/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b.git"
OBJECTS_PATH = "/home/zach/Documents/test_connections/objects.json"
HOST = "0.0.0.0"
PORT = 5001
SOCKET_TIMEOUT = 20.0

# Load firewall configuration - it's in the same gitlab folder
FIREWALL_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'firewall.conf')
firewall.load_config_from_file(FIREWALL_CONFIG_PATH)

def load_object():
    path = os.path.join(OBJECTS_PATH)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()

def handle_connection(conn, addr):
    client_ip = addr[0]
    
    # Firewall check - reject before any processing
    if not firewall.is_allowed(client_ip):
        print(f"[!] Firewall blocked connection from {client_ip}")
        conn.close()
        return

    print(f"[+] New connection from {addr}")
    responder_sk, responder_pk = ensure_responder_keys()

    try:
        nc = noise_responder_handshake(conn, responder_sk, timeout=SOCKET_TIMEOUT)
        print("[+] Noise handshake finished (responder)")

        try:
            payload_bytes = load_object()
            enc_payload = nc.encrypt(payload_bytes)
            send_frame(conn, enc_payload, timeout=SOCKET_TIMEOUT)
            print("[+] Sent payload")

        except Exception as e:
            print(f"[!] Failed to generate/send payload: {e}")
            traceback.print_exc()

    except Exception as e:
        print(f"[!] Connection handler error: {e}", file=sys.stderr)
        traceback.print_exc()

    finally:
        conn.close()
        print(f"[+] Closed connection from {addr}")

def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[*] Listening on {HOST}:{PORT} ...")

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_connection, daemon=True, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    try:
        serve()
    except KeyboardInterrupt:
        print("Shutting down")