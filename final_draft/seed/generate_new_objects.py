import subprocess
import json

def run_git_command(args):
    """Run git command and return output as string."""
    result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def generate_cid():
    # Placeholder for now
    return "CID_PLACEHOLDER"

def generate_new_objects(old_sha, new_sha):
    """
    Generate JSON for all commits between old_sha and new_sha (inclusive of new_sha).
    """
    dag = {"objects": []}

    # List all commits in the push range, newest last
    commits = run_git_command(["rev-list", f"{old_sha}..{new_sha}"]).splitlines()

    for commit_sha in reversed(commits):  # process in chronological order
        # Commit info
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

        # Add commit object
        dag["objects"].append({
            "type": "commit",
            "sha": commit_sha,
            "cid": generate_cid(),
            "message": commit_message,
            "parents": parents
        })

        # Tree object
        dag["objects"].append({
            "type": "tree",
            "sha": tree_sha,
            "cid": generate_cid()
        })

        # Blobs
        tree_entries = run_git_command(["ls-tree", "-r", tree_sha]).splitlines()
        for entry in tree_entries:
            parts = entry.split()
            if len(parts) >= 4 and parts[1] == "blob":
                sha = parts[2]
                path = entry.split("\t", 1)[1]
                dag["objects"].append({
                    "type": "blob",
                    "sha": sha,
                    "cid": generate_cid(),
                    "path": path
                })

    return json.dumps(dag, indent=2)


if __name__ == "__main__":
    old_sha = "HEAD~2"   # two commits back
    new_sha = "HEAD"
    print(generate_new_objects(old_sha, new_sha))
