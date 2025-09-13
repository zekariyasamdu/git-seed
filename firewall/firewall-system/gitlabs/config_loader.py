import os
import configparser
import argparse
import os
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

# ---------------------------
# Argument parsing
# ---------------------------
parser = argparse.ArgumentParser(description="Load client or server keys and generate if missing")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--client", action="store_true", help="Load client config")
group.add_argument("--server", action="store_true", help="Load server config")
args = parser.parse_args()

# Determine config file
if args.client:
    config_file = "client.config"
elif args.server:
    config_file = "server.config"

# ---------------------------
# Load config
# ---------------------------
config = configparser.ConfigParser()
config.read(config_file)

# Expand paths
KEY_DIR = os.path.expanduser(config["KEYS"]["KEY_DIR"])
RESPONDER_STATIC_SK = config["KEYS"].get("RESPONDER_STATIC_SK")
RESPONDER_STATIC_PK = config["KEYS"].get("RESPONDER_STATIC_PK")
INITIATOR_STATIC_SK = config["KEYS"].get("INITIATOR_STATIC_SK")
INITIATOR_STATIC_PK = config["KEYS"].get("INITIATOR_STATIC_PK")

if RESPONDER_STATIC_SK: RESPONDER_STATIC_SK = os.path.expanduser(RESPONDER_STATIC_SK)
if RESPONDER_STATIC_PK: RESPONDER_STATIC_PK = os.path.expanduser(RESPONDER_STATIC_PK)
if INITIATOR_STATIC_SK: INITIATOR_STATIC_SK = os.path.expanduser(INITIATOR_STATIC_SK)
if INITIATOR_STATIC_PK: INITIATOR_STATIC_PK = os.path.expanduser(INITIATOR_STATIC_PK)

# Ensure directory exists
os.makedirs(KEY_DIR, exist_ok=True)

# ---------------------------
# Key generation
# ---------------------------
def generate_keypair(sk_path, pk_path):
    if os.path.exists(sk_path) and os.path.exists(pk_path):
        return
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()
    os.makedirs(os.path.dirname(sk_path), exist_ok=True)
    with open(sk_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open(pk_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ))

if RESPONDER_STATIC_SK and RESPONDER_STATIC_PK:
    generate_keypair(RESPONDER_STATIC_SK, RESPONDER_STATIC_PK)
if INITIATOR_STATIC_SK and INITIATOR_STATIC_PK:
    generate_keypair(INITIATOR_STATIC_SK, INITIATOR_STATIC_PK)

# ---------------------------
# Info
# ---------------------------
if __name__ == "__main__":
    print("Key directory:", KEY_DIR)
    if RESPONDER_STATIC_SK: print("Responder private key:", RESPONDER_STATIC_SK)
    if RESPONDER_STATIC_PK: print("Responder public key:", RESPONDER_STATIC_PK)
    if INITIATOR_STATIC_SK: print("Initiator private key:", INITIATOR_STATIC_SK)
    if INITIATOR_STATIC_PK: print("Initiator public key:", INITIATOR_STATIC_PK)
