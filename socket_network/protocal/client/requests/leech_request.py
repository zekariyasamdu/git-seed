import socket, json, sys

NODE_ONE_HOST = "127.0.0.1"
NODE_ONE_PORT = 6000



def send_json_line(conn, obj):
    data = (json.dumps(obj) + "\n").encode()
    conn.sendall(data)



def leech_request(CID, context):

    try:

        # wrapping the SSL with the socket
        with socket.create_connection((NODE_ONE_HOST, NODE_ONE_PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=NODE_ONE_HOST) as ssock:

            # Send an ANNOUNCE message
                leech_request_msg = {
                    "type": "LEECH",
                    "cid": CID,
                    "ip": "127....",
                    "seed": "swarm"
                }

                send_json_line(ssock, leech_request_msg)

                # Receive file
                with open("pulled", "wb") as f:

                    print("leeching....")
                    while True:
                        data = ssock.recv(8192)
                        if not data:

                            print("leech doesn't exist")
                            break
                        f.write(data)

        print("File leeched!")
    except Exception as e:
        print(f"[client] error: {e}")
        sys.exit(1)




