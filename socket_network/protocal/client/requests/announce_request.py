import socket, json, sys

MAIN_NODE_HOST = "127.0.0.1"
MAIN_NODE_PORT = 7443

def send_json_line(conn, obj):
    data = (json.dumps(obj) + "\n").encode()
    conn.sendall(data)

def announce(CID, context):

        try:
            with socket.create_connection((MAIN_NODE_HOST, MAIN_NODE_PORT)) as sock:
                with context.wrap_socket(sock, server_hostname=MAIN_NODE_HOST) as ssock:

                        # Send an ANNOUNCE message
                        announce_msg = {
                            "type": "ANNOUNCE",
                            "cid": CID,
                            "ip": "127...",
                            "seed": "main node"
                        }
                        send_json_line(ssock, announce_msg)
                        print("[client] sent ANNOUNCE message")

                        # Receive the response
                        buf = b""
                        while True:
                            chunk = ssock.recv(4096)
                            if not chunk:

                                print("Failed to connect!")
                                break
                            buf += chunk
                            while b"\n" in buf:
                                line, buf = buf.split(b"\n", 1)
                                if not line.strip():
                                    continue
                                try:
                                    msg = json.loads(line.decode())
                                    print(f"[client] received: {msg}")

                                    if msg.get("type") == "APPROVED":
                                        print("[client] update approved, exiting.")
                                        return
                                    else:
                                        print("[client] update denied, exiting.")

                                except Exception as e:
                                    print(f"[client] invalid JSON: {e}")

        except Exception as e:
                print(f"[client] error: {e}")
                sys.exit(1)
