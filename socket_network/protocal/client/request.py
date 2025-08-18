import argparse, ssl
from requests.leech_request import leech_request
from requests.announce_request import announce_request

# SSL context for proper verification
context = ssl.create_default_context(cafile="./client_keys/ca_cert.pem")
context.check_hostname = True
context.load_cert_chain(certfile="./client_keys/client_cert.pem", keyfile="./client_keys/client_key.pem")


"""
 Calling the appropriate request handle
 leech_request -> a request sent by a node peer to fetch a file
 announce_request -> a request sent by a node peer validate a push to main "git push origin main"
"""

def client_request(request, cdi=None):

    if request == "leech":
        if not cdi:
            print("Error: --cdi is required for leech mode")
            return
        leech_request(cdi, context)

    elif request == "approve":
        if not cdi:
            print("Error: --cdi is required for leech mode")
            return
        announce_request(cdi, context)

    else:

        print("unknown request")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, help="Choose 'leech' or 'approve'")
    parser.add_argument("--cdi", help="Content Identifier (CID) to fetch when using 'leech'")
    args = parser.parse_args()

    client_request(args.client, args.cdi)
