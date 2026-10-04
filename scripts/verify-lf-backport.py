"""Verify Git blobs preserve the original PR content while enforcing LF."""
import subprocess
import sys

actual_ref, source_ref = sys.argv[1:]


def paths(ref):
    return set(subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", ref, "--", "src"]
    ).decode().splitlines())


def blob(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"])


expected_paths = {
    f"src/{style}_{name}.py"
    for style in ("crlf", "lf", "mixed")
    for name in ("arithmetic", "greeting")
}
if paths(actual_ref) != expected_paths or paths(source_ref) != expected_paths:
    raise SystemExit("FAIL: fixture paths differ from the six expected files")

for path in sorted(expected_paths):
    actual = blob(actual_ref, path)
    expected = blob(source_ref, path).replace(b"\r\n", b"\n")
    if actual != expected:
        raise SystemExit(f"FAIL: {path}: source content differs after LF conversion")
    if b"\r" in actual or actual.count(b"\n") != 11:
        raise SystemExit(f"FAIL: {path}: expected 11 LF endings and zero CR bytes")
    if any(marker in actual for marker in (b"<<<<<<<", b"=======", b">>>>>>>")):
        raise SystemExit(f"FAIL: {path}: conflict marker present")
    print(f"PASS {path}: 11 LF, 0 CRLF; original PR content preserved")

print("PASS: all six backported Git blobs match the original PR normalized to LF")
