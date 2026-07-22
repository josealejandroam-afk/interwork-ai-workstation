import subprocess
from pathlib import Path

from .errors import ExecutionError


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
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


def make_local_commit(repo: Path, message: str, paths: list[str]) -> str:
    if not paths:
        return starting_commit(repo)
    git(repo, "add", "--", *paths)
    git(repo, "commit", "-m", message)
    return starting_commit(repo)
