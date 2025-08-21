import json

def write_in_json_file(data, filename="objects.json"):
    try:
        with open(filename, "a") as f:
            f.write(data + "\n")  # append JSON per line
        print(f"Appended objects to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def accept_new_objects(sock):
    try:
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk

        if data:
            decoded = data.decode()
            write_in_json_file(decoded)
            print("Received and saved new objects JSON.")

    except Exception as e:
        print(f"Error receiving objects: {e}")
