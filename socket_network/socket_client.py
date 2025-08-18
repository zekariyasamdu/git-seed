import socket
import ssl

HOST = "127.0.0.1"
PORT = 6000
CID = "Qmf412jQZiuVUtdgnB36FXFX7xg5V6KEbSJ4dpQuhkLyfD"
out_file = "downloaded_from_ipfs"

# SSL context for proper verification
context = ssl.create_default_context(cafile="./test_keys/ca_cert.pem")  # CA cert that signed server certificate
context.check_hostname = True  # Verify server hostname matches certificate

# for mutual TLS (if server requires client certificate)
context.load_cert_chain(certfile="./test_keys/client_cert.pem", keyfile="./test_keys/client_key.pem")

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        # Send CID
        ssock.sendall(CID.encode())

        # Receive file
        with open(out_file, "wb") as f:
            while True:
                data = ssock.recv(8192)
                if not data:
                    break
                f.write(data)

print("File downloaded with verified SSL!")


