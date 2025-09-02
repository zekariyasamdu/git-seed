import subprocess
import json
import os

'''

A file that holds functions that are used to generate the json file that containes
information about each git object ["commits", "trees", "blobs"] information such as
sha name and CID code in the ipfs network, which is later used to generate a whole repo off of a peer.

'''

"""
Run git command and return output as string.
"""
def run_git_command(args):
    result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
    return result.stdout.strip()

"""
Run ipfs command and return output as string.
"""
def run_ipfs_command(args, input_data=None):
    try:
        cmd = ["ipfs"] + args

        if input_data is not None:
            cmd = cmd + ["-"]
            if isinstance(input_data, bytes):
                result = subprocess.run(
                    cmd,
                    input=input_data,
                    capture_output=True,
                    check=True
                )
                return result.stdout.decode('utf-8').strip()
            else:
                result = subprocess.run(
                    cmd,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout.strip()
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"IPFS command failed: {' '.join(cmd)}")
        print(f"Error output: {e.stderr.decode('utf-8') if isinstance(e.stderr, bytes) else e.stderr}")
        print(f"Return code: {e.returncode}")
        raise



def read_git_object_compressed(sha: str) -> bytes:
    folder, fname = sha[:2], sha[2:]
    path = os.path.join(".git", "objects", folder, fname)
    with open(path, "rb") as f:
        return f.read()


'''
Generate cid for each object
'''
import subprocess

def generate_cid(sha: str) -> str:
    try:
        raw_compressed = read_git_object_compressed(sha)

        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(raw_compressed)
            tmp_path = tmp.name

        result = subprocess.run(
            ["ipfs", "add", "--quiet", tmp_path],
            capture_output=True,
            text=True,
            check=True
        )
        os.unlink(tmp_path)
        return result.stdout.strip()
    except Exception as e:
        print(f"Failed to generate CID for SHA {sha}: {e}")
        raise

"""
Split SHA into folder/file form, same as .git/objects storage.
"""
def split_sha(sha: str):
    """Return folder_name and file_name from a Git SHA."""
    return sha[:2], sha[2:]


"""
Generate JSON for all commits between old_sha and new_sha (inclusive of new_sha).
"""
def generate_new_objects(old_sha, new_sha):
    dag = {"objects": []}

    commits = run_git_command(["rev-list", f"{old_sha}..{new_sha}"]).splitlines()

    for commit_sha in reversed(commits): 
        commit_info = run_git_command(["cat-file", "-p", commit_sha]).splitlines()
        tree_sha = None
        parents = []
        message_lines = []
        in_message = False

        for line in commit_info:
            if line.startswith("tree "):
                tree_sha = line.split()[1]
            elif line.startswith("parent "):
                parents.append(line.split()[1])
            elif line.strip() == "" and not in_message:
                in_message = True
            elif in_message:
                message_lines.append(line)
        commit_message = "\n".join(message_lines).strip()

        folder, fname = split_sha(commit_sha)
        dag["objects"].append({
            "type": "commit",
            "sha": commit_sha,
            "cid": generate_cid(commit_sha),
            "folder_name": folder,
            "file_name": fname,
            "message": commit_message,
            "parents": parents
        })

        folder, fname = split_sha(tree_sha)
        dag["objects"].append({
            "type": "tree",
            "sha": tree_sha,
            "cid": generate_cid(tree_sha),
            "folder_name": folder,
            "file_name": fname
        })

        tree_entries = run_git_command(["ls-tree", "-r", tree_sha]).splitlines()
        for entry in tree_entries:
            parts = entry.split()
            if len(parts) >= 4 and parts[1] == "blob":
                sha = parts[2]
                path = entry.split("\t", 1)[1]
                folder, fname = split_sha(sha)
                dag["objects"].append({
                    "type": "blob",
                    "sha": sha,
                    "cid": generate_cid(sha),
                    "folder_name": folder,
                    "file_name": fname,
                    "path": path
                })

    return json.dumps(dag, indent=2)