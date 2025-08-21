# ipfs_fastimport.py
import sys, json, time
from typing import Dict, List, Optional, Iterable, Tuple
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

def is_commit(cid: str) -> bool:
    j = _cat_json(cid)
    return bool(j and j.get("type") == "commit")

def walk_tree(tree_cid: str, base: str = "") -> Iterable[Tuple[str, bytes]]:
    node = _cat_json(tree_cid)
    if not node or node.get("type") != "tree":
        raise ValueError(f"{tree_cid} is not a tree")
    for name, child_cid in node["entries"].items():
        path = f"{base}{name}" if not base else f"{base}/{name}"
        child = _cat_json(child_cid)
        if child and child.get("type") == "tree":
            yield from walk_tree(child_cid, path)
        else:
            yield (path, _cat(child_cid))  # blob bytes

def build_history_first_parent(head_cid: str) -> List[Dict]:
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
        cur = parents[0] if parents else None
    out.reverse()  # oldest -> newest
    return out

def emit_fast_import(head_cid: str, branch: str = "refs/heads/main", out = None):
    """
    Write a complete fast-import stream for the history ending at head_cid.
    """
    out = out or sys.stdout

    hist = build_history_first_parent(head_cid)  # oldest..newest
    marks = {}  # commitCID -> :mark
    next_mark = 1

    print("feature done", file=out)

    for commit in hist:
        mark = f":{next_mark}"; next_mark += 1
        marks[commit["cid"]] = mark

        # Commit header
        print(f"commit {branch}", file=out)
        print(f"mark {mark}", file=out)
        print(f"author {commit['author']} {commit['timestamp']} +0000", file=out)
        print(f"committer {commit['author']} {commit['timestamp']} +0000", file=out)
        msg = commit["message"] or ""
        print(f"data {len(msg.encode())}\n{msg}", file=out)

        # Parents
        parents = commit["parents"]
        if parents:
            # 'from' first parent if we already emitted it, else fall back to deleteall
            p0 = parents[0]
            if p0 in marks:
                print(f"from {marks[p0]}", file=out)
            else:
                print("deleteall", file=out)
            # Additional parents as merges, if present & known
            for p in parents[1:]:
                if p in marks:
                    print(f"merge {marks[p]}", file=out)
        else:
            print("deleteall", file=out)

        # Files: rebuild full snapshot for this commit
        for path, blob in walk_tree(commit["tree"]):
            print(f"M 100644 inline {path}", file=out)
            print(f"data {len(blob)}", file=out)
            out.buffer.write(blob) if hasattr(out, "buffer") else out.write(blob.decode(errors="ignore"))
            print(file=out)  # newline after data

        print(file=out)  # blank line after commit

    print("done", file=out)

if __name__ == "__main__":
    # Usage:
    #   python ipfs_fastimport.py <CommitCID> [branch]
    # Pipe to git:
    #   git init newrepo && cd newrepo
    #   python /path/ipfs_fastimport.py QmYourHeadCID refs/heads/main | git fast-import
    #   git checkout main
    if len(sys.argv) < 2:
        print("Usage: python ipfs_fastimport.py <CommitCID> [branch]", file=sys.stderr)
        sys.exit(1)
    head = sys.argv[1]
    branch = sys.argv[2] if len(sys.argv) > 2 else "refs/heads/main"
    emit_fast_import(head, branch)


"""

git init restored && cd restored
python /path/to/ipfs_fastimport.py QmYourHeadCID refs/heads/main | git fast-import
git checkout main


"""