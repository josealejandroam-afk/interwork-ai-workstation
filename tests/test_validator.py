import subprocess
import tempfile
import unittest
from pathlib import Path

from local_executor.task_schema import Task
from local_executor.validator import validate
from local_executor.errors import ExecutionError
from tests.test_task_schema import valid_task


def run(repo, *args):
    subprocess.run(args, cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class ValidatorTests(unittest.TestCase):
    def test_allowed_change_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            project = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
            project.mkdir(parents=True)
            card = project / "PROJECT_CARD.md"
            card.write_text("# Project 7556\n", encoding="utf-8")
            run(repo, "git", "init", "-b", "test")
            run(repo, "git", "config", "user.email", "test@example.invalid")
            run(repo, "git", "config", "user.name", "Test")
            run(repo, "git", "add", ".")
            run(repo, "git", "commit", "-m", "fixture")
            original = {card: card.read_text(encoding="utf-8")}
            card.write_text("# Project 7556\n\n- Confirmed fact\n", encoding="utf-8")
            checks = validate(repo, project, Task.from_dict(valid_task()), original)
            self.assertTrue(all(value == "PASS" for value in checks.values()))

    def test_new_conflicting_project_number_rejected_but_existing_history_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            project = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
            project.mkdir(parents=True)
            card = project / "PROJECT_CARD.md"
            card.write_text("# Project 7556\n\nLinked historical Project 7000.\n", encoding="utf-8")
            run(repo, "git", "init", "-b", "test")
            run(repo, "git", "config", "user.email", "test@example.invalid")
            run(repo, "git", "config", "user.name", "Test")
            run(repo, "git", "add", ".")
            run(repo, "git", "commit", "-m", "fixture")
            original = {card: card.read_text(encoding="utf-8")}
            card.write_text(original[card] + "\nNo change to historical reference.\n", encoding="utf-8")
            checks = validate(repo, project, Task.from_dict(valid_task()), original)
            self.assertEqual(checks["Project number unchanged"], "PASS")
            card.write_text(original[card] + "\nProject number: 9999\n", encoding="utf-8")
            with self.assertRaisesRegex(ExecutionError, "Project number"):
                validate(repo, project, Task.from_dict(valid_task()), original)


if __name__ == "__main__":
    unittest.main()
