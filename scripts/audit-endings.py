"""Count actual line endings in committed Git blobs, avoiding checkout conversion."""
import json
import subprocess
import sys

for ref in sys.argv[1:] or ["HEAD"]:
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", ref, "--", "src"]
    ).decode().splitlines()
    for path in paths:
        blob = subprocess.check_output(["git", "show", f"{ref}:{path}"])
        crlf = blob.count(b"\r\n")
        lf = blob.count(b"\n") - crlf
        print(json.dumps({
            "ref": ref, "path": path, "crlf": crlf, "lf": lf,
            "bare_cr": blob.count(b"\r") - crlf,
            "conflict_markers": b"<<<<<<<" in blob,
        }))
