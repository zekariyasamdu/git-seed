#!/usr/bin/env python3
import subprocess
import os
import json
import sys
import socket
import threading

import os
from utils.noise_utils_client import (
    noise_initiator_handshake,
    recv_frame,
    ensure_initiator_keys,
)

OBJECTS_FILE = "objects.json"
LOCK = threading.Lock()
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



def download_objects_json_socket(host, port):
    """Download objects.json from the server socket"""
    print(f"[*] Connecting to server {host}:{port} ...")
    data = b""


    initiator_sk, initiator_pk = ensure_initiator_keys()

    try:
        with socket.create_connection((host, port), timeout=SOCKET_TIMEOUT) as sock:

            nc = noise_initiator_handshake(sock, initiator_sk, timeout=SOCKET_TIMEOUT)
            print("[+] Noise handshake finished (initiator)")


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




def restore_objects_from_ipfs(objects_json):
    """Restore Git objects from IPFS to .git/objects/ directory using ipfs get"""
    if not objects_json or "objects" not in objects_json:
        print("[!] No objects to restore")
        return
    
    objects = objects_json["objects"]
    restored_count = 0
    skipped_count = 0
    

    repo_root = os.path.abspath(os.path.dirname(os.getcwd())) 
    git_objects_dir = os.path.join(repo_root, ".git", "objects")
    
    print(f"[*] Restoring objects to: {git_objects_dir}")
    
    os.makedirs(git_objects_dir, exist_ok=True)
    
    for obj in objects:
        sha = obj["sha"]
        cid = obj["cid"]
        folder_name = obj["folder_name"]
        file_name = obj["file_name"]
        obj_type = obj["type"]
        
        object_path = os.path.join(git_objects_dir, folder_name, file_name)
        if os.path.exists(object_path):
            print(f"[*] Object {sha} already exists, skipping")
            skipped_count += 1
            continue
        
        object_dir = os.path.join(git_objects_dir, folder_name)
        os.makedirs(object_dir, exist_ok=True)
        
        try:
            print(f"[*] Downloading object {sha} ({obj_type}) from IPFS ({cid})...")
            
            result = subprocess.run([
                "ipfs", "get", cid,
                "--output", object_path
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"[!] ipfs get failed for {cid}: {result.stderr}")
                if os.path.exists(object_path):
                    os.remove(object_path)
                continue

            try:
                original_cwd = os.getcwd()
                os.chdir(repo_root)
                
                verify_result = subprocess.run([
                    "git", "cat-file", "-t", sha
                ], capture_output=True, text=True, timeout=10)
                
                os.chdir(original_cwd)
                
                if verify_result.returncode == 0:
                    print(f"[+] Restored object {sha} ({obj_type})")
                    restored_count += 1
                else:
                    print(f"[!] Failed to verify object {sha}: {verify_result.stderr}")
                    if os.path.exists(object_path):
                        os.remove(object_path)
                    
            except subprocess.TimeoutExpired:
                print(f"[!] Timeout verifying object {sha}")
                if os.path.exists(object_path):
                    os.remove(object_path)
            except Exception as e:
                print(f"[!] Error verifying object {sha}: {e}")
                if os.path.exists(object_path):
                    os.remove(object_path)
                    
        except subprocess.TimeoutExpired:
            print(f"[!] Timeout downloading object {sha}")
            if os.path.exists(object_path):
                os.remove(object_path)
        except Exception as e:
            print(f"[!] Failed to download object {sha} from IPFS: {e}")
            if os.path.exists(object_path):
                os.remove(object_path)
    
    print(f"[+] Restoration complete: {restored_count} objects restored, {skipped_count} already existed")

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
    restore_objects_from_ipfs(objects_json)


if __name__ == "__main__":
    main()
