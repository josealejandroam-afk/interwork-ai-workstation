def rollback_command(commit: str) -> str:
    return f"git revert --no-edit {commit}"
