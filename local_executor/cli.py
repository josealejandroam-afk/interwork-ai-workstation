import argparse
import json
import sys
from pathlib import Path

from .errors import ExecutorError
from .executor import execute
from .report_generator import write_report
from .runtime_state import finalize_recovery, inspect_lock, inspect_running, recover_running, recover_stale_lock
from .runtime_guard import validate_task_id


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Apply a policy-bound project-memory JSON task")
    value.add_argument("task", type=Path)
    value.add_argument("--repo", type=Path, required=True)
    value.add_argument("--runtime", type=Path, required=True)
    value.add_argument("--no-commit", action="store_true", help="validate and report without a local commit")
    value.add_argument("--retry", action="store_true", help="explicitly retry a prior failed task within maximum_attempts")
    return value


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        result = execute(args.task.resolve(), args.repo.resolve(), args.runtime.resolve(), commit=not args.no_commit, retry=args.retry)
    except ExecutorError as exc:
        print(f"Task failed safely: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


def _maintenance(argv: list[str]) -> int | None:
    if not argv or argv[0] not in {"inspect-lock", "recover-lock", "inspect-running", "recover-running", "recover-finalization"}:
        return None
    command = argv[0]
    maintenance = argparse.ArgumentParser(description=f"Local executor {command}")
    maintenance.add_argument("--runtime", type=Path, required=True)
    if command in {"inspect-lock", "recover-lock"}:
        maintenance.add_argument("--project", type=Path, required=True)
        maintenance.add_argument("--force", action="store_true")
    elif command in {"inspect-running", "recover-running"}:
        maintenance.add_argument("task_id")
        maintenance.add_argument("--force", action="store_true")
    else:
        maintenance.add_argument("task_id")
        maintenance.add_argument("--repo", type=Path, required=True)
    args = maintenance.parse_args(argv[1:])
    try:
        if command == "inspect-lock":
            result = inspect_lock(args.runtime.resolve(), args.project.resolve())
        elif command == "recover-lock":
            result = recover_stale_lock(args.runtime.resolve(), args.project.resolve(), force=args.force)
        elif command == "inspect-running":
            result = inspect_running(args.runtime.resolve(), validate_task_id(args.task_id))
        elif command == "recover-running":
            result = recover_running(args.runtime.resolve(), validate_task_id(args.task_id), force=args.force)
        else:
            result = finalize_recovery(args.runtime.resolve(), args.repo.resolve(), args.task_id, write_report)
    except ExecutorError as exc:
        print(f"Maintenance command failed safely: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    maintenance_result = _maintenance(sys.argv[1:])
    raise SystemExit(main() if maintenance_result is None else maintenance_result)
