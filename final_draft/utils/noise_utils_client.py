# noise_utils_client.py
import os
import struct
import configparser, sys
from typing import Tuple
from noise.connection import NoiseConnection, Keypair

# ---------------------------
# Config (client loads its own keys)
# ---------------------------

KEY_DIR = os.path.expanduser("~/.git_ipfs_keys/client")
INITIATOR_STATIC_SK = os.path.join(KEY_DIR, "initiator_static.sk")
INITIATOR_STATIC_PK = os.path.join(KEY_DIR, "initiator_static.pk")

# Ensure key directory exists
os.makedirs(KEY_DIR, exist_ok=True)


NOISE_PATTERN = "XX"
CIPHER = "ChaChaPoly"
DH = "25519"
HASH = "BLAKE2s"

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
# Key management
# ---------------------------
def ensure_key_dir():
    os.makedirs(KEY_DIR, exist_ok=True)

def write_binary(path: str, data: bytes, mode=0o600):
    with open(path, "wb") as f:
        f.write(data)
    try:
        os.chmod(path, mode)
    except Exception:
        pass

def read_binary(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def ensure_initiator_keys() -> Tuple[bytes, bytes]:
    ensure_key_dir()
    if os.path.exists(INITIATOR_STATIC_SK) and os.path.exists(INITIATOR_STATIC_PK):
        return read_binary(INITIATOR_STATIC_SK), read_binary(INITIATOR_STATIC_PK)

    # Generate private key + derive public key
    priv = os.urandom(32)
    nc = NoiseConnection.from_name(f"Noise_{NOISE_PATTERN}_{DH}_{CIPHER}_{HASH}".encode())  # pass bytes
    nc.set_as_initiator()
    # use Keypair enum
    nc.set_keypair_from_private_bytes(Keypair.STATIC, priv)
    pub = nc.get_public_key(Keypair.STATIC)

    write_binary(INITIATOR_STATIC_SK, priv)
    write_binary(INITIATOR_STATIC_PK, pub)
    return priv, pub

# ---------------------------
# Noise handshake (initiator) -- XX pattern does not require pre-shared rs
# ---------------------------
def noise_initiator_handshake(sock, initiator_static_priv: bytes, timeout: float = 20.0):
    proto = f"Noise_{NOISE_PATTERN}_{DH}_{CIPHER}_{HASH}".encode()
    nc = NoiseConnection.from_name(proto)
    nc.set_as_initiator()
    nc.set_keypair_from_private_bytes(Keypair.STATIC, initiator_static_priv)

    nc.start_handshake()

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
