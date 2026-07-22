from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path
from typing import Callable


TEMP_PREFIX = ".local-executor-"


def atomic_write_bytes(
    path: Path, data: bytes,
    before_replace: Callable[[Path, bytes], None] | None = None,
    after_replace: Callable[[Path], None] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=TEMP_PREFIX, suffix=".tmp", delete=False
        ) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if existing_mode is not None:
            os.chmod(temporary, existing_mode)
        if before_replace:
            before_replace(path, data)
        os.replace(temporary, path)
        temporary = None
        if after_replace:
            after_replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def cleanup_abandoned_temps(folder: Path) -> None:
    for path in folder.glob(f"{TEMP_PREFIX}*.tmp"):
        if path.is_file() and not path.is_symlink():
            path.unlink()
