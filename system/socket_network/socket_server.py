import socket

HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 6000       # Port to listen on (choose any free port)

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))   # Bind to host and port
    s.listen()             # Start listening for incoming connections
    print(f"Socket server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()  # Accept a new client
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)  # Receive data from client
                if not data:
                    break
                print(f"Received: {data.decode()}")
                conn.sendall(b"Hello from server!")  # Send a response
