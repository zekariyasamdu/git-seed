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
#  python3 -m gitlabs.approve_response

# Set this to the pusher host that the container can reach (your host)
PUSHER_HOST = os.getenv("PUSHER_HOST", "127.0.0.1")
PUSHER_PORT = int(os.getenv("PUSHER_PORT", "6003"))
SOCKET_TIMEOUT = 20.0  # keep small to avoid blocking hook

OBJECTS_OUTFILE = "objects.json"  # append JSON lines here

def check_code() -> bool:
    # Your validation logic here. For now always approve.
    return True

def save_objects_json(json_text: str, filename=OBJECTS_OUTFILE):
    try:
        # append newline-delimited JSON entries
        with open(filename, "a") as f:
            f.write(json_text.strip() + "\n")
        print(f"[+] Appended objects JSON to {filename}", file=sys.stderr)
    except Exception as e:
        print(f"[!] Error saving objects json: {e}", file=sys.stderr)

def run_hook(old_sha: str, new_sha: str):
    # load or generate our initiator keypair (responder public not required with XX)
    initiator_sk, initiator_pk = ensure_initiator_keys()
    # create TCP connection
    with socket.create_connection((PUSHER_HOST, PUSHER_PORT), timeout=SOCKET_TIMEOUT) as sock:
        # perform initiator handshake (no responder PK required for XX)
        nc = noise_initiator_handshake(sock, initiator_sk, timeout=SOCKET_TIMEOUT)
        print("[+] Noise handshake finished (initiator)")

        control_plain = "Approved" if check_code() else "Denied"
        enc_control = nc.encrypt(control_plain.encode())  # Use encrypt() after handshake
        send_frame(sock, enc_control, timeout=SOCKET_TIMEOUT)

        if control_plain == "Approved":
            # optionally tell pusher the commit range
            range_plain = f"{old_sha} {new_sha}"
            enc_range = nc.encrypt(range_plain.encode())
            send_frame(sock, enc_range, timeout=SOCKET_TIMEOUT)

            # receive encrypted JSON payload frame
            enc_payload = recv_frame(sock, timeout=SOCKET_TIMEOUT)
            payload_plain = nc.decrypt(enc_payload).decode()  # Use decrypt() after handshake
            # Save to objects.json
            save_objects_json(payload_plain)
        else:
            print("[+] Push denied. No payload requested.")

if __name__ == "__main__":
    # Example usage: you should call this from your hook and pass old,new
    # if len(sys.argv) >= 3:
    #     old, new = sys.argv[1], sys.argv[2]
    # else:
    #     # fallback for testing
    old, new = "HEAD~1", "HEAD"
    run_hook(old, new)
