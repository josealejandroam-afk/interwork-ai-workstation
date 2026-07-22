import tempfile
import unittest
from pathlib import Path

from local_executor.errors import PolicyError
from local_executor.path_guard import resolve_project
from local_executor.task_schema import Task
from tests.test_task_schema import valid_task


class PathGuardTests(unittest.TestCase):
    def test_allowed_project_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            project = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
            project.mkdir(parents=True)
            self.assertEqual(resolve_project(repo, Task.from_dict(valid_task())), project.resolve())

    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = Task.from_dict(valid_task(allowed_paths=["../outside/"]))
            with self.assertRaisesRegex(PolicyError, "unsafe"):
                resolve_project(Path(tmp), task)

    def test_unauthorized_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = Task.from_dict(valid_task(allowed_paths=["memory/clients/other/projects/7556_x/"]))
            with self.assertRaisesRegex(PolicyError, "outside"):
                resolve_project(Path(tmp), task)


if __name__ == "__main__":
    unittest.main()
