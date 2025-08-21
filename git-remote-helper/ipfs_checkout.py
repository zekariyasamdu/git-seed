# ipfs_checkout.py
import os, json, time
from typing import Dict, List, Optional, Tuple, Iterable
import ipfshttpclient

client = ipfshttpclient.connect()

def _cat(cid: str) -> bytes:
    return client.cat(cid)

def _cat_json(cid: str) -> Optional[Dict]:
    b = _cat(cid)
    try:
        return json.loads(b.decode())
    except Exception:
        return None

def is_tree(cid: str) -> bool:
    j = _cat_json(cid)
    return bool(j and j.get("type") == "tree")

def is_commit(cid: str) -> bool:
    j = _cat_json(cid)
    return bool(j and j.get("type") == "commit")

def walk_tree(tree_cid: str, base: str = "") -> Iterable[Tuple[str, str]]:
    """
    Yield (path, blob_cid) for every file in the tree recursively.
    """
    node = _cat_json(tree_cid)
    if not node or node.get("type") != "tree":
        raise ValueError(f"{tree_cid} is not a tree")
    for name, child_cid in node["entries"].items():
        path = f"{base}{name}" if not base else f"{base}/{name}"
        child = _cat_json(child_cid)
        if child and child.get("type") == "tree":
            yield from walk_tree(child_cid, path)
        else:
            # treat as blob
            yield (path, child_cid)

def materialize_commit(commit_cid: str, dest_dir: str) -> None:
    """
    Write the files of commit_cid into dest_dir (plain working tree).
    """
    commit = _cat_json(commit_cid)
    if not commit or commit.get("type") != "commit":
        raise ValueError(f"{commit_cid} is not a commit")
    os.makedirs(dest_dir, exist_ok=True)
    for relpath, blob_cid in walk_tree(commit["tree"]):
        abs_path = os.path.join(dest_dir, relpath)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "wb") as f:
            f.write(_cat(blob_cid))
    # Drop small metadata
    with open(os.path.join(dest_dir, ".ipfs-commit-cid"), "w") as f:
        f.write(commit_cid + "\n")
    with open(os.path.join(dest_dir, ".ipfs-commit-message"), "w") as f:
        f.write(commit.get("message", "") + "\n")

def walk_history_from(head_cid: str) -> List[Dict]:
    """
    Return a linear history list following first-parent chain:
    [ {cid, message, parents[], tree, author, timestamp}, ... ] from HEAD→root
    """
    out = []
    cur = head_cid
    seen = set()
    while cur and cur not in seen:
        seen.add(cur)
        c = _cat_json(cur)
        if not c or c.get("type") != "commit":
            raise ValueError(f"{cur} is not a commit")
        out.append({
            "cid": cur,
            "message": c.get("message", ""),
            "parents": c.get("parents", []),
            "tree": c["tree"],
            "author": c.get("author", "ipfs <ipfs@local>"),
            "timestamp": int(c.get("timestamp", time.time())),
        })
        parents = c.get("parents", [])
        cur = parents[0] if parents else None   # first-parent walk
    return out

if __name__ == "__main__":
    # Example quick test:
    # python ipfs_checkout.py <commitCID> <outdir>
    import sys
    if len(sys.argv) == 3:
        head = sys.argv[1]
        out = sys.argv[2]
        materialize_commit(head, out)
        print(f"Checked out {head} to {out}")
    else:
        print("Usage: python ipfs_checkout.py <commitCID> <outdir>")
