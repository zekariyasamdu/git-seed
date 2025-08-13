import socket

HOST = "127.0.0.1"
PORT = 6000
CID = "QmWfVY9y3xjsixTgbd9AorQxH7VtMpzfx2HaWtsoUYecaX"
out_file = "downloaded_from_ipfs"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(CID.encode())  # Send the CID to server

    with open(out_file, "wb") as f:
        while True:
            data = s.recv(1024)
            if not data:
                break
            f.write(data)

print("File downloaded!")
