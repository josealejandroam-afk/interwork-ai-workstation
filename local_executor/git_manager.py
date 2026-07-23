import hashlib
import subprocess
from pathlib import Path

from .errors import ExecutionError


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    if check and result.returncode:
        raise ExecutionError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def require_safe_branch(repo: Path) -> str:
    branch = git(repo, "branch", "--show-current").strip()
    if not branch or branch in {"main", "master"}:
        raise ExecutionError("executor refuses to run on main/master or detached HEAD")
    return branch


def starting_commit(repo: Path) -> str:
    return git(repo, "rev-parse", "HEAD").strip()


def changed_paths(repo: Path) -> list[str]:
    output = git(repo, "status", "--porcelain", "--untracked-files=all")
    return [line[3:].replace("\\", "/") for line in output.splitlines() if len(line) >= 4]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_expected_changes(repo: Path, expected: dict[str, str]) -> None:
    current = set(changed_paths(repo))
    if current != set(expected):
        raise ExecutionError("repository changed after validation; commit refused")
    for relative, expected_hash in expected.items():
        path = repo / relative
        if not path.is_file() or sha256_file(path) != expected_hash:
            raise ExecutionError(f"approved file changed externally before staging: {relative}")


def make_local_commit(repo: Path, message: str, paths: list[str], expected: dict[str, str], hooks_dir: Path) -> str:
    if not paths:
        return starting_commit(repo)
    verify_expected_changes(repo, expected)
    hooks_dir.mkdir(parents=True, exist_ok=False)
    git(repo, "add", "--", *paths)
    for relative in expected:
        expected_blob = git(repo, "hash-object", "--path", relative, "--", relative).strip()
        staged_blob = git(repo, "rev-parse", f":{relative}").strip()
        if expected_blob != staged_blob:
            raise ExecutionError(f"staged content hash mismatch: {relative}")
    staged_paths = set(git(repo, "diff", "--cached", "--name-only").splitlines())
    if staged_paths != set(expected):
        raise ExecutionError("Git index changed unexpectedly; commit refused")
    verify_expected_changes(repo, expected)
    git(
        repo, "-c", f"core.hooksPath={hooks_dir.resolve()}", "-c", "commit.gpgSign=false",
        "commit", "--no-gpg-sign", "--only", "-m", message, "--", *paths,
    )
    return starting_commit(repo)


def unstage_paths(repo: Path, paths: list[str]) -> None:
    if paths:
        git(repo, "restore", "--staged", "--", *paths, check=False)
