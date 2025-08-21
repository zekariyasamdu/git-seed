import socket
import os
import json

HOST = "0.0.0.0"
PORT = 6000
BACKUP_DIR = ".backup"
DAG_FILE = "dag.json"

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)
dag_path = os.path.join(BACKUP_DIR, DAG_FILE)

# Load existing DAG safely
dag_data = {}
if os.path.exists(dag_path):
    try:
        with open(dag_path, "r") as f:
            content = f.read().strip()
            if content:  # only load if file is not empty
                dag_data = json.loads(content)
    except json.JSONDecodeError:
        print(f"[!] Warning: {dag_path} is not valid JSON. Starting with empty DAG.")

def peer_mode():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"[+] Socket server listening on {HOST}:{PORT}", flush=True)

        while True:
            try:
                conn, addr = sock.accept()
                with conn:
                    print(f"[+] Connected by {addr}", flush=True)
                    data = b""
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        data += chunk

                    if data:
                        incoming_json = json.loads(data.decode())
                        print(f"[+] Received {len(incoming_json)} commits", flush=True)

                        # Merge incoming DAG into existing DAG
                        dag_data.update(incoming_json)

                        # Write updated DAG back to file
                        with open(dag_path, "w") as f:
                            json.dump(dag_data, f, indent=2)
                        print(f"[+] DAG updated, total commits: {len(dag_data)}", flush=True)

            except Exception as e:
                print(f"Server warning: {e}", flush=True)

if __name__ == "__main__":
    peer_mode()
