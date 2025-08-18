import ssl, threading, json, queue, subprocess, time


clients_lock = threading.Lock()
clients = set()
broadcast_q = queue.Queue()

def verify_update(announce: dict) -> tuple[bool, str]:
    """
    Check for any CI/CD problems
    """
    cid = announce.get("cid", "")
    branch = announce.get("branch", "")
    if not cid or not branch:
        return (False, "missing cid/branch")

    # Example policy: only allow 'main'
    if branch != "main":
        return (False, "only 'main' branch is accepted")

    try:
        # Quick proof the CID is known/fetchable by IPFS (local node)
        # Fastest is 'ipfs ls CID' for DAGs or 'ipfs block stat' for raw/UnixFS blocks
        # Fallback to a short-'ipfs cat' probe with timeout.
        probe = subprocess.run(
            ["ipfs", "ls", cid],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10
        )
        if probe.returncode != 0:
            # try a tiny cat to see if any bytes are returned
            cat = subprocess.run(
                ["bash", "-lc", f"ipfs cat {cid} | head -c 1 >/dev/null 2>&1"],
                timeout=10
            )
            if cat.returncode != 0:
                return (False, f"cid not reachable: {probe.stderr.decode().strip()}")
        return (True, "ok")
    except subprocess.TimeoutExpired:
        return (False, "ipfs probe timed out")
    except Exception as e:
        return (False, f"verify error: {e}")

def send_json_line(conn, obj):
    data = (json.dumps(obj) + "\n").encode()
    conn.sendall(data)

def approve_response(conn: ssl.SSLSocket, addr):
    peername = f"{addr[0]}:{addr[1]}"
    with conn:
        try:

            # Register this client
            with clients_lock:
                clients.add((conn, addr))
            # Welcome
            send_json_line(conn, {"type":"WELCOME","ts":int(time.time())})

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
                    except Exception:
                        send_json_line(conn, {"type":"ERROR","error":"invalid json"})
                        continue

                    mtype = msg.get("type","").upper()
                    if mtype == "PING":
                        send_json_line(conn, {"type":"PONG","ts":int(time.time())})
                    elif mtype == "ANNOUNCE":
                        # Expected fields: {type:"ANNOUNCE", branch, commit, cid, source}
                        ok, reason = verify_update(msg)
                        if ok:
                            approved = {
                                "type":"APPROVED",
                                "branch": msg.get("branch"),
                                "commit": msg.get("commit"),
                                "cid":    msg.get("cid"),
                                "source": msg.get("source"),
                                "ts": int(time.time())
                            }
                            broadcast_q.put(approved)
                            send_json_line(conn, {"type":"ACK","status":"approved","detail":reason})
                        else:
                            send_json_line(conn, {"type":"NACK","status":"rejected","detail":reason})
                    else:
                        send_json_line(conn, {"type":"ERROR","error":"unknown type"})
        finally:
            with clients_lock:
                clients.discard((conn, addr))

def broadcaster():
    while True:
        msg = broadcast_q.get()
        with clients_lock:
            dead = []
            for (c, a) in clients:
                try:
                    send_json_line(c, msg)
                except Exception:
                    dead.append((c, a))
            for x in dead:
                clients.discard(x)
