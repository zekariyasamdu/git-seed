# approve_response_secure.py
import socket
import os
from utils.noise_utils_client import (
    noise_initiator_handshake,
    send_frame,
    recv_frame,
    ensure_initiator_keys,
)
import sys
import json
import threading

OBJECTS_FILE = "objects.json"
LOCK = threading.Lock()

#  python3 -m gitlabs.approve_response

PUSHER_HOST = os.getenv("PUSHER_HOST", "127.0.0.1")
PUSHER_PORT = int(os.getenv("PUSHER_PORT", "6003"))
SOCKET_TIMEOUT = 20.0

OBJECTS_OUTFILE = "objects.json"

def check_code() -> bool:

    return True

def write_in_json_file(new_data: str, filename=OBJECTS_FILE):
    """
    Merge new_data (JSON with {"objects": [...]}) into the existing objects.json file.
    Remove duplicates based on SHA.
    """
    try:
        
        new_json = json.loads(new_data)
        new_objects = new_json.get("objects", [])

        with LOCK:

            if os.path.exists(filename):
                with open(filename, "r") as f:
                    try:
                        existing_data = json.load(f)
                        existing_objects = existing_data.get("objects", [])
                    except json.JSONDecodeError:
                        existing_objects = []
            else:
                existing_objects = []

            merged_objects = existing_objects + new_objects

            seen = set()
            unique_objects = []
            for obj in merged_objects:
                if obj["sha"] not in seen:
                    seen.add(obj["sha"])
                    unique_objects.append(obj)

            with open(filename, "w") as f:  
                json.dump({"objects": unique_objects}, f, indent=2)

        print(f"[+] Merged {len(new_objects)} new objects into {filename} (total: {len(unique_objects)})")

    except Exception as e:
        print(f"[!] Error writing to file: {e}")




def run_hook(old_sha: str, new_sha: str):
    initiator_sk, initiator_pk = ensure_initiator_keys()

    with socket.create_connection((PUSHER_HOST, PUSHER_PORT), timeout=SOCKET_TIMEOUT) as sock:

        nc = noise_initiator_handshake(sock, initiator_sk, timeout=SOCKET_TIMEOUT)
        print("[+] Noise handshake finished (initiator)")

        control_plain = "Approved" if check_code() else "Denied"
        enc_control = nc.encrypt(control_plain.encode())
        send_frame(sock, enc_control, timeout=SOCKET_TIMEOUT)

        if control_plain == "Approved":
            range_plain = f"{old_sha} {new_sha}"
            enc_range = nc.encrypt(range_plain.encode())
            send_frame(sock, enc_range, timeout=SOCKET_TIMEOUT)

            enc_payload = recv_frame(sock, timeout=SOCKET_TIMEOUT)
            payload_plain = nc.decrypt(enc_payload).decode()
            write_in_json_file(payload_plain)
        else:
            print("[+] Push denied. No payload requested.")

if __name__ == "__main__":

    # if len(sys.argv) >= 3:
    #     old, new = sys.argv[1], sys.argv[2]
    # else:
    old, new = "HEAD~1", "HEAD"
    run_hook(old, new)
