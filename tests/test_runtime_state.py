import json
import socket
import tempfile
import unittest
from pathlib import Path

from local_executor.errors import ExecutionError
from local_executor.runtime_state import (
    ProjectLock, begin_attempt, fail_attempt, finish_attempt, inspect_lock, project_lock_path,
    inspect_running, recover_running, recover_stale_lock,
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

    def test_running_recovery_refuses_live_pid_and_archives_dead_pid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtime, project = root / "runtime", root / "project"
            project.mkdir()
            live_task = Task.from_dict(valid_task(task_id="live-7556"))
            _, live_running = begin_attempt(runtime, live_task, project)
            self.assertTrue(inspect_running(runtime, live_task.task_id)["process_alive"])
            with self.assertRaisesRegex(ExecutionError, "still live"):
                recover_running(runtime, live_task.task_id)
            live_running.unlink()

            dead_task = Task.from_dict(valid_task(task_id="dead-7556", maximum_attempts=2))
            _, dead_running = begin_attempt(runtime, dead_task, project)
            data = json.loads(dead_running.read_text(encoding="utf-8"))
            data["process_id"] = 99999999
            dead_running.write_text(json.dumps(data), encoding="utf-8")
            recovered = recover_running(runtime, dead_task.task_id)
            self.assertTrue(recovered["recovered"])
            self.assertTrue(Path(recovered["interrupted_record"]).exists())
            attempt, retry_running = begin_attempt(runtime, dead_task, project, retry=True)
            self.assertEqual(attempt, 2)
            retry_running.unlink()

    def test_running_recovery_handles_missing_and_malformed_lock_metadata(self):
        for malformed in (False, True):
            with self.subTest(malformed=malformed), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                runtime, project = root / "runtime", root / "project"
                project.mkdir()
                task = Task.from_dict(valid_task(task_id=f"broken-{int(malformed)}"))
                _, running = begin_attempt(runtime, task, project)
                record = json.loads(running.read_text(encoding="utf-8"))
                record["process_id"] = 99999999
                running.write_text(json.dumps(record), encoding="utf-8")
                lock_path = project_lock_path(runtime, project)
                lock_path.mkdir(parents=True)
                if malformed:
                    (lock_path / "lock.json").write_text("{bad-json", encoding="utf-8")
                with self.assertRaisesRegex(ExecutionError, "force"):
                    recover_running(runtime, task.task_id)
                recovered = recover_running(runtime, task.task_id, force=True)
                self.assertTrue(recovered["recovered"])
                self.assertFalse(lock_path.exists())

    def test_malformed_running_record_requires_explicit_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "runtime"
            running = runtime / "queue/running/malformed-7556.json"
            running.parent.mkdir(parents=True)
            running.write_text("{partial", encoding="utf-8")
            info = inspect_running(runtime, "malformed-7556")
            self.assertEqual(info["metadata_error"], "JSONDecodeError")
            with self.assertRaisesRegex(ExecutionError, "force"):
                recover_running(runtime, "malformed-7556")
            recovered = recover_running(runtime, "malformed-7556", force=True)
            self.assertTrue(recovered["recovered"])


if __name__ == "__main__":
    unittest.main()
