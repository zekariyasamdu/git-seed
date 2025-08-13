import socket

HOST = "127.0.0.1"  # Server IP
PORT = 6000         # Server port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello server!")
    data = s.recv(1024)
    print(f"Received from server: {data.decode()}")
