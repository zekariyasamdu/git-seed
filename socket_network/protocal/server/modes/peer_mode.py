import socket
import requests
import ssl
import threading
from responses.update_response import update_response
from responses.leech_response import leech_response

# Server configuration
HOST = "127.0.0.1"
PORT = 6000

# Local IPFS gateway
LOCAL_GATEWAY = "http://127.0.0.1:8080/ipfs/"

# SSL configuration
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="./test_keys/server_cert.pem", keyfile="./test_keys/server_key.pem")
context.verify_mode = ssl.CERT_REQUIRED  # Require a client certificate
context.load_verify_locations(cafile="./test_keys/ca_cert.pem") # CA that signed the client cert


# Function to handle each client connection
def handle_client(conn, addr):
    ssl_conn = context.wrap_socket(conn, server_side=True)  # wrap AFTER accept
    with ssl_conn:
        print(f"[+] Connected by {addr}")
        data = ssl_conn.recv(1024)
        leech_response(ssl_conn)

# Main server loop
def peer_mode():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"[+] Socket server listening on {HOST}:{PORT}")


        while True:
          conn, addr = sock.accept()

          threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    peer_mode()
