#!/usr/bin/env python3
"""
Check whether this machine is ready to run the Microsoft Graph read-only scripts.
Does NOT authenticate. Does NOT call Graph API. Safe to run any time.
"""

import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_GITIGNORE_PATTERNS = [
    "local_sources/",
    "*.token.json",
    "msal_cache",
    "graph_auth_cache",
]


def check(label, ok, detail=""):
    status = "OK  " if ok else "FAIL"
    line = f"  {status}  {label}"
    if detail:
        line += f"\n        -> {detail}"
    print(line)
    return ok


def check_python():
    major, minor = sys.version_info[:2]
    ok = major == 3 and minor >= 7
    return check(
        f"Python {major}.{minor}",
        ok,
        "" if ok else "Need Python 3.7 or later"
    )


def check_msal():
    try:
        import msal
        return check(f"msal {msal.__version__} installed", True)
    except ImportError:
        return check(
            "msal NOT installed",
            False,
            "Run: uv pip install msal  OR  pip install msal"
        )


def check_gitignore():
    gi = REPO_ROOT / ".gitignore"
    if not gi.exists():
        return check(".gitignore exists", False, "Create .gitignore before proceeding")
    content = gi.read_text(encoding="utf-8", errors="replace")
    all_ok = True
    for pattern in REQUIRED_GITIGNORE_PATTERNS:
        ok = pattern in content
        check(f".gitignore covers '{pattern}'", ok,
              "" if ok else "Add this pattern to .gitignore before running auth")
        if not ok:
            all_ok = False
    return all_ok


def check_local_dirs():
    dirs = [
        "local_sources/graph_cache",
        "local_sources/graph_mail",
        "local_sources/graph_calendar",
    ]
    print("  INFO  Local output dirs (created automatically on first run):")
    for d in dirs:
        p = REPO_ROOT / d
        status = "exists" if p.exists() else "will be created"
        print(f"        {d}: {status}")
    return True


def check_no_token_files_committed():
    result = subprocess.run(
        ["git", "ls-files", "*.token.json", "local_sources/graph_cache/"],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    tracked = result.stdout.strip()
    if tracked:
        return check(
            "No token files in git",
            False,
            f"DANGER: These files are tracked by git: {tracked}\nRun: git rm --cached <file>"
        )
    return check("No token files tracked by git", True)


def main():
    print("=" * 55)
    print("  Microsoft Graph Read-Only — Setup Check")
    print("=" * 55)
    print()

    results = []

    print("[ Python ]")
    results.append(check_python())
    print()

    print("[ Packages ]")
    results.append(check_msal())
    print()

    print("[ Security: .gitignore ]")
    results.append(check_gitignore())
    print()

    print("[ Security: no tokens in git ]")
    results.append(check_no_token_files_committed())
    print()

    print("[ Local output directories ]")
    results.append(check_local_dirs())
    print()

    print("=" * 55)
    if all(results):
        print("  READY. Run graph_mail_reader.py to authenticate.")
        print()
        print("  First run (dry-run only):")
        print("    python scripts/graph_mail_reader.py --dry-run --max-results 5")
    else:
        print("  NOT READY. Fix the items marked FAIL above first.")
    print("=" * 55)


if __name__ == "__main__":
    main()
