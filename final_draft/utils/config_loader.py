import os
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

#-----------------------------------
# The following program is used to generate private and public keys if the user doesn't have any
#-----------------------------------

"""
Path were the keys live
"""
KEY_DIR = os.path.expanduser("~/.git_ipfs_keys/")
IPFS_STATIC_SK = os.path.join(KEY_DIR, "ipfs_static.sk")
IPFS_STATIC_PK = os.path.join(KEY_DIR, "ipfs_static.pk")

"""
Generation of the keys
"""
def generate_keypair(sk_path, pk_path):
    """Generate a Noise X25519 keypair if missing."""
    if os.path.exists(sk_path) and os.path.exists(pk_path):
        return

    # Generate private key using X25519 elliptic curve used for Diffie–Hellman key exchange.
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Ensure directory exists
    os.makedirs(os.path.dirname(sk_path), exist_ok=True)

    # Save private key
    with open(sk_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ))
    os.chmod(sk_path, 0o600)

    # Save public key
    with open(pk_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ))
    os.chmod(pk_path, 0o644)

    print(f"Generated new keypair: {sk_path}, {pk_path}")

if __name__ == "__main__":
    os.makedirs(KEY_DIR, exist_ok=True)
    print("Key directory:", KEY_DIR)
    generate_keypair(IPFS_STATIC_SK, IPFS_STATIC_PK)
