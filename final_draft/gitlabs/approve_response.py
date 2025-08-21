import socket
from accept_new_objects import accept_new_objects

TEST_HOST = "172.17.0.1"   # pusher’s server
TEST_PORT = 6001

def check_code():
    # Always approve for now
    return True

def approve_response():
    try:
        with socket.create_connection((TEST_HOST, TEST_PORT), timeout=10) as s:
            if check_code():
                message = "Approved"
            else:
                message = "Denied"

            s.sendall(message.encode())

            if message == "Approved":
                # Get the JSON response and write it
                accept_new_objects(s)

    except Exception as e:
        print(f"Approval error: {e}")

if __name__ == "__main__":
    approve_response()
