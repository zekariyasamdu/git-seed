import argparse
from modes.main_mode import main_mode
from modes.peer_mode import peer_mode

def start_peer(mode):
    if mode == "main":
        main_mode()
    elif mode == "peer":
        peer_mode()
    else:
        print("Unknown mode")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, help="Choose 'main' or 'peer'")
    args = parser.parse_args()
    start_peer(args.mode)
