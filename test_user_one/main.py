import socket

HOST = "127.0.0.1"
PORT = 6000

try:
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        message = "updated repo"
        sock.sendall(message.encode())

except Exception as e:
    print(f"Hook warning: {e}", flush=True)