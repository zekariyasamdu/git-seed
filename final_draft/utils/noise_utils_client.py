import os
import struct
from typing import Tuple
from noise.connection import NoiseConnection, Keypair

from utils.config_loader import generate_keypair

# ---------------------------
# The folloing file is used as a collection of noise protocal helper funtions for the initiator
# ---------------------------

"""
Path were the keys live
"""
KEY_DIR = os.path.expanduser("~/.git_ipfs_keys/")
IPFS_STATIC_SK = os.path.join(KEY_DIR, "ipfs_static.sk")
IPFS_STATIC_PK = os.path.join(KEY_DIR, "ipfs_static.pk")


"""
Configrations for the noise ptotocal
"""
NOISE_PATTERN = "XX"
CIPHER = "ChaChaPoly"
DH = "25519"
HASH = "BLAKE2s"


# ---------------------------
# Key management
# ---------------------------
def ensure_key_dir():
    os.makedirs(KEY_DIR, exist_ok=True)

def read_binary(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def ensure_initiator_keys() -> Tuple[bytes, bytes]:
    ensure_key_dir()
    if os.path.exists(IPFS_STATIC_SK) and os.path.exists(IPFS_STATIC_PK):
        return read_binary(IPFS_STATIC_SK), read_binary(IPFS_STATIC_PK)

    generate_keypair(IPFS_STATIC_SK, IPFS_STATIC_PK)
    return ensure_initiator_keys()

# ---------------------------
# Frame helpers
# ---------------------------

def send_frame(sock, data: bytes, timeout: float | None = None):
    length = struct.pack(">I", len(data))
    sock.settimeout(timeout)
    sock.sendall(length + data)

def recv_exact(sock, n: int, timeout: float | None = None) -> bytes:
    sock.settimeout(timeout)
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError(f"Connection closed (read {len(buf)}/{n} bytes)")
        buf += chunk
    return buf

def recv_frame(sock, timeout: float | None = None) -> bytes:
    header = recv_exact(sock, 4, timeout)
    (length,) = struct.unpack(">I", header)
    return recv_exact(sock, length, timeout) if length else b""



# ---------------------------
# Noise handshake (initiator)
# ---------------------------
def noise_initiator_handshake(sock, initiator_static_priv: bytes, timeout: float = 20.0):
    proto = f"Noise_{NOISE_PATTERN}_{DH}_{CIPHER}_{HASH}".encode()
    nc = NoiseConnection.from_name(proto)
    nc.set_as_initiator()
    nc.set_keypair_from_private_bytes(Keypair.STATIC, initiator_static_priv)

    nc.start_handshake()

# e = responder’s ephemeral key
# ee = DH shared secret from ephemeral keys
# s = responder’s static public key
# es = DH shared secret between initiator ephemeral & responder static key

     # -> e
    msg = nc.write_message()
    send_frame(sock, msg, timeout)

    # <- e, ee, s, es
    msg = recv_frame(sock, timeout)
    nc.read_message(msg)

    # -> s, se
    msg = nc.write_message()
    send_frame(sock, msg, timeout)

    if not nc.handshake_finished:
        raise RuntimeError("Handshake did not finish")

    return nc
