import tempfile
import unittest
from pathlib import Path

from local_executor.project_locator import locate_project
from local_executor.task_schema import Task
from tests.test_task_schema import valid_task


class ProjectLocatorTests(unittest.TestCase):
    def test_only_project_card_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            project = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
            project.mkdir(parents=True)
            (project / "PROJECT_CARD.md").write_text("# Project 7556\n", encoding="utf-8")
            found, files = locate_project(repo, Task.from_dict(valid_task()))
            self.assertEqual(found, project.resolve())
            self.assertEqual([p.name for p in files], ["PROJECT_CARD.md"])


if __name__ == "__main__":
    unittest.main()
