import socket
import requests

HOST = "0.0.0.0"
PORT = 6000

# Local IPFS gateway
LOCAL_GATEWAY = "http://127.0.0.1:8080/ipfs/"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Socket server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                cid = data.decode().strip()  # Expect the client to send the CID
                print(f"Received CID: {cid}")

                try:
                    url = LOCAL_GATEWAY + cid
                    resp = requests.get(url, stream=True)
                    resp.raise_for_status()
                    for chunk in resp.iter_content(1024):
                        conn.sendall(chunk)
                    print(f"File {cid} sent successfully!")
                except Exception as e:
                    conn.sendall(f"ERROR: {e}".encode())
