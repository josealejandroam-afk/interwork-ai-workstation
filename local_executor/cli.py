import argparse
import json
import sys
from pathlib import Path

from .errors import ExecutorError
from .executor import execute


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Apply a policy-bound project-memory JSON task")
    value.add_argument("task", type=Path)
    value.add_argument("--repo", type=Path, required=True)
    value.add_argument("--runtime", type=Path, required=True)
    value.add_argument("--no-commit", action="store_true", help="validate and report without a local commit")
    return value


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        result = execute(args.task.resolve(), args.repo.resolve(), args.runtime.resolve(), commit=not args.no_commit)
    except ExecutorError as exc:
        print(f"Task failed safely: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
