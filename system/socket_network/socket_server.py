import socket
import requests
import ssl
import threading

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
        while True:
            data = ssl_conn.recv(1024)
            if not data:
                break
            cid = data.decode().strip()
            print(f"[+] Received CID: {cid}")
            try:
                url = LOCAL_GATEWAY + cid
                resp = requests.get(url, stream=True)
                resp.raise_for_status()
                for chunk in resp.iter_content(8192):
                    ssl_conn.sendall(chunk)
                print(f"[+] File {cid} sent successfully!")
                break;
            except Exception as e:
                error_msg = f"ERROR: {e}"
                ssl_conn.sendall(error_msg.encode())
                print(f"[-] Failed to send {cid}: {e}")

# Main server loop
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"[+] Socket server listening on {HOST}:{PORT}")


        while True:
          conn, addr = sock.accept()

          threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
