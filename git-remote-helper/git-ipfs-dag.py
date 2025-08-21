import ipfshttpclient
import json
from typing import List, Dict, Optional

# Connect to local IPFS node
client = ipfshttpclient.connect()

class Blob:
    def __init__(self, content: str):
        self.content = content
        # Store content in IPFS
        res = client.add_bytes(content.encode())
        self.cid = res

class Tree:
    def __init__(self):
        self.entries: Dict[str, str] = {}  # filename → CID
        self.cid = None

    def add(self, name: str, cid: str):
        self.entries[name] = cid

    def save(self):
        data = json.dumps({"type": "tree", "entries": self.entries}).encode()
        self.cid = client.add_bytes(data)
        return self.cid

class Commit:
    def __init__(self, tree_cid: str, parents: Optional[List[str]] = None, message: str = ""):
        self.tree_cid = tree_cid
        self.parents = parents or []
        self.message = message
        self.cid = None

    def save(self):
        data = {
            "type": "commit",
            "tree": self.tree_cid,
            "parents": self.parents,
            "message": self.message
        }
        self.cid = client.add_bytes(json.dumps(data).encode())
        return self.cid

"""

# 1. Create blobs (files)
b1 = Blob("print('Hello World')")
b2 = Blob("# README file")

print("Blob1 CID:", b1.cid)
print("Blob2 CID:", b2.cid)

# 2. Create a tree (directory)
t1 = Tree()
t1.add("main.py", b1.cid)
t1.add("README.md", b2.cid)
tree_cid = t1.save()

print("Tree CID:", tree_cid)

# 3. First commit
c1 = Commit(tree_cid=tree_cid, message="Initial commit")
c1_cid = c1.save()

print("Commit 1 CID:", c1_cid)

# 4. Modify file -> new blob + new tree + new commit
b3 = Blob("print('Hello Zach!')")
t2 = Tree()
t2.add("main.py", b3.cid)
t2.add("README.md", b2.cid)
tree2_cid = t2.save()

c2 = Commit(tree_cid=tree2_cid, parents=[c1_cid], message="Update main.py")
c2_cid = c2.save()

print("Commit 2 CID:", c2_cid, "Parent:", c1_cid)


"""
