import requests
LOCAL_GATEWAY = "http://127.0.0.1:8080/ipfs/"



def leech_response(ssl_conn):
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
