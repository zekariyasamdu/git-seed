#!/usr/bin/env python3
import subprocess
import os
import json
import sys
import socket
import socket
import os
from utils.noise_utils_client import (
    noise_initiator_handshake,
    recv_frame,
    ensure_initiator_keys,
)
import sys

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
FALLBACK_FETCH = True
SOCKET_TIMEOUT = 20.0
# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def run_git_command(args):
    """Run a git command and return stdout"""
    result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def fetch_refs():
    """Fetch refs from GitLab normally"""
    print("[*] Fetching refs from GitLab...")
    run_git_command(["fetch", "origin"])

def write_in_json_file(data, filename="new_objects.json"):
    try:
        with open(filename, "a") as f:
            f.write(data + "\n")  # append JSON per line
        print(f"Appended objects to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def download_objects_json_socket(host, port):
    """Download objects.json from the server socket"""
    print(f"[*] Connecting to server {host}:{port} ...")
    data = b""

    # load or generate initiator keys
    initiator_sk, initiator_pk = ensure_initiator_keys()

    try:
        with socket.create_connection((host, port), timeout=SOCKET_TIMEOUT) as sock:
            # perform initiator handshake
            nc = noise_initiator_handshake(sock, initiator_sk, timeout=SOCKET_TIMEOUT)
            print("[+] Noise handshake finished (initiator)")

            # receive encrypted payload
            enc_data = recv_frame(sock, timeout=SOCKET_TIMEOUT)
            data = nc.decrypt(enc_data)
            write_in_json_file(data.decode())

    except Exception as e:
        print(f"[!] Failed to fetch objects.json from socket: {e}")
        return None

    try:
        objects = json.loads(data.decode())
        print(f"[*] Loaded {len(objects['objects'])} objects from JSON")
        return objects
    except Exception as e:
        print(f"[!] Failed to parse objects.json: {e}")
        return None



# def fetch_ipfs_object(cid, sha):
#     """Fetch an object from IPFS and write to .git/objects/<first_two>/<rest>"""
#     folder, fname = sha[:2], sha[2:]
#     obj_path = f".git/objects/{folder}/{fname}"
#     os.makedirs(os.path.dirname(obj_path), exist_ok=True)

#     if os.path.exists(obj_path):
#         return

#     print(f"[*] Fetching object {sha} from IPFS ({cid})...")
#     try:
#         subprocess.run(["ipfs", "cat", cid, "-o", obj_path], check=True)
#         print("[*] All objects restored from IPFS.")
#     except subprocess.CalledProcessError as e:
#         print(f"[!] Failed to fetch {sha} from IPFS: {e}")

# def restore_objects_from_ipfs(objects_json):
#     """Restore all objects in objects.json from IPFS"""
#     for obj in objects_json.get("objects", []):
#         fetch_ipfs_object(obj["cid"], obj["sha"])


'''


'''
def main():
    try:
        fetch_refs()
    except Exception as e:
        print(f"[!] Git fetch failed: {e}")
        if not FALLBACK_FETCH:
            sys.exit(1)

    objects_json = download_objects_json_socket(SERVER_HOST, SERVER_PORT)
    if not objects_json:
        print("[!] No objects.json available. Exiting.")
        if FALLBACK_FETCH:
            print("[*] Proceeding with normal Git fetch only.")
            return
        else:
            sys.exit(1)
    # restore_objects_from_ipfs(objects_json)


if __name__ == "__main__":
    main()
