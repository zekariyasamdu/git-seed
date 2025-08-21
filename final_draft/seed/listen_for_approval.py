import socket
from generate_new_objects import generate_new_objects

TEST_HOST = "0.0.0.0"
TEST_PORT = 6001

def listen_for_approval():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TEST_HOST, TEST_PORT))
        s.listen()
        print(f"Pusher listening on {TEST_HOST}:{TEST_PORT}")

        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")

                    data = conn.recv(4096).decode()
                    print(f"Received: {data}")

                    if data == "Approved":
                        new_objects = generate_new_objects()
                        conn.sendall(new_objects.encode())
                        print("Sent new objects JSON back to GitLab.")

                    elif data == "Denied":
                        print("Vulnerabilities found. Rejecting push.")
                    else:
                        print("Unexpected response.")

            except Exception as e:
                print(f"Connection error: {e}")

if __name__ == "__main__":
    listen_for_approval()
