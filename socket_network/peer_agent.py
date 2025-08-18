import socket, json, sys

HOST = "127.0.0.1"
PORT = 7443

def send_json_line(conn, obj):
    data = (json.dumps(obj) + "\n").encode()
    conn.sendall(data)

def main():
    try:
        with socket.create_connection((HOST, PORT)) as conn:
            print("[client] connected and verified server cert")

            # Send an ANNOUNCE message
            announce_msg = {
                "type": "ANNOUNCE",
                "branch": "main",
                "commit": "abcdef123456",
                "cid": "QmdTPDKnNdomf5ViJ2b8PrAYMepLSmBtzQtNdaU84HPKJN",
                "source": "my-build-machine"
            }
            send_json_line(conn, announce_msg)
            print("[client] sent ANNOUNCE message")

            buf = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
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
                    except Exception as e:
                        print(f"[client] invalid JSON: {e}")

    except Exception as e:
        print(f"[client] error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()