import json
import socket
import tempfile
import unittest
from pathlib import Path

from local_executor.errors import ExecutionError
from local_executor.runtime_state import (
    ProjectLock, begin_attempt, fail_attempt, finish_attempt, inspect_lock, project_lock_path,
    recover_stale_lock,
)
from local_executor.task_schema import Task
from tests.test_task_schema import valid_task


class RuntimeStateTests(unittest.TestCase):
    def test_atomic_pending_to_running_and_duplicate_running(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime, project = root / "runtime", root / "project"
            project.mkdir()
            task = Task.from_dict(valid_task(task_id="queue-7556"))
            attempt, running = begin_attempt(runtime, task, project)
            self.assertEqual(attempt, 1)
            self.assertTrue(running.exists())
            self.assertFalse((runtime / "queue/pending/queue-7556.json").exists())
            record = json.loads(running.read_text(encoding="utf-8"))
            self.assertEqual(record["canonical_project_path"], str(project.resolve()))
            with self.assertRaisesRegex(ExecutionError, "running"):
                begin_attempt(runtime, task, project)

    def test_completed_id_is_durable_and_cannot_repeat(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime, project = root / "runtime", root / "project"
            project.mkdir()
            task = Task.from_dict(valid_task(task_id="complete-7556"))
            _, running = begin_attempt(runtime, task, project)
            finish_attempt(runtime, task.task_id, running, {"task_id": task.task_id, "status": "completed"})
            with self.assertRaisesRegex(ExecutionError, "completed"):
                begin_attempt(runtime, task, project)

    def test_lock_refusal_release_and_stale_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime, project = root / "runtime", root / "project"
            project.mkdir()
            first = ProjectLock(runtime, project, "first").acquire()
            info = inspect_lock(runtime, project)
            self.assertTrue(info["locked"])
            self.assertTrue(info["process_alive"])
            with self.assertRaisesRegex(ExecutionError, "locked"):
                ProjectLock(runtime, project, "second").acquire()
            with self.assertRaisesRegex(ExecutionError, "still live"):
                recover_stale_lock(runtime, project)
            first.release()
            self.assertFalse(inspect_lock(runtime, project)["locked"])

            stale = project_lock_path(runtime, project)
            stale.mkdir(parents=True)
            (stale / "lock.json").write_text(json.dumps({
                "task_id": "interrupted", "process_id": 99999999,
                "hostname": socket.gethostname(), "canonical_project_path": str(project.resolve()),
                "acquired_at": "2000-01-01T00:00:00+00:00", "executor_version": "0.1.0",
            }), encoding="utf-8")
            recovered = recover_stale_lock(runtime, project)
            self.assertTrue(recovered["recovered"])
            self.assertFalse(stale.exists())

    def test_failed_attempt_history_retry_and_maximum(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime, project = root / "runtime", root / "project"
            project.mkdir()
            task = Task.from_dict(valid_task(task_id="retry-7556", maximum_attempts=2))
            attempt, running = begin_attempt(runtime, task, project)
            first = fail_attempt(runtime, task.task_id, running, attempt, {"status": "failed", "attempt": attempt})
            original = first.read_text(encoding="utf-8")
            with self.assertRaisesRegex(ExecutionError, "explicit retry"):
                begin_attempt(runtime, task, project)
            attempt, running = begin_attempt(runtime, task, project, retry=True)
            self.assertEqual(attempt, 2)
            fail_attempt(runtime, task.task_id, running, attempt, {"status": "failed", "attempt": attempt})
            self.assertEqual(first.read_text(encoding="utf-8"), original)
            with self.assertRaisesRegex(ExecutionError, "maximum_attempts"):
                begin_attempt(runtime, task, project, retry=True)


if __name__ == "__main__":
    unittest.main()
