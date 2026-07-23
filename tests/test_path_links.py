import json
import os
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

from local_executor.errors import PolicyError
from local_executor.executor import execute
from local_executor.path_guard import resolve_project
from local_executor.task_schema import Task
from tests.test_task_schema import valid_task


def make_link(link: Path, target: Path, directory=False):
    try:
        os.symlink(target, link, target_is_directory=directory)
    except OSError as exc:
        raise unittest.SkipTest(f"platform cannot create required symbolic link: {exc}")


def make_junction(link: Path, target: Path):
    if sys.platform != "win32":
        raise unittest.SkipTest("Windows junction test is not applicable on this platform")
    result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise unittest.SkipTest(f"platform cannot create required junction: {result.stderr.strip()}")


class LinkSecurityTests(unittest.TestCase):
    def test_project_link_escaping_repository_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, outside = root / "repo", root / "outside"
            parent = repo / "memory/clients/marsh_mclennan/projects"
            parent.mkdir(parents=True)
            outside.mkdir()
            make_link(parent / "7556_mma_art_work_dallas", outside, directory=True)
            with self.assertRaisesRegex(PolicyError, "escaped"):
                resolve_project(repo, Task.from_dict(valid_task()))

    def test_project_junction_escaping_repository_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, outside = root / "repo", root / "outside"
            parent = repo / "memory/clients/marsh_mclennan/projects"
            parent.mkdir(parents=True)
            outside.mkdir()
            make_junction(parent / "7556_mma_art_work_dallas", outside)
            with self.assertRaisesRegex(PolicyError, "escaped"):
                resolve_project(repo, Task.from_dict(valid_task()))

    def test_approved_file_link_escaping_project_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = root / "repo", root / "runtime"
            project = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
            project.mkdir(parents=True)
            outside = root / "outside.md"
            outside.write_text("# Project 7556\n", encoding="utf-8")
            make_link(project / "PROJECT_CARD.md", outside)
            subprocess.run(["git", "init", "-b", "codex/test"], cwd=repo, check=True, stdout=subprocess.PIPE)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, check=True, stdout=subprocess.PIPE)
            task = root / "task.json"
            task.write_text(json.dumps(valid_task(task_id="link-7556")), encoding="utf-8")
            with self.assertRaises(PolicyError):
                execute(task, repo, runtime)
            self.assertEqual(outside.read_text(encoding="utf-8"), "# Project 7556\n")

    def test_optional_file_link_escaping_project_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            (project / "PROJECT_CARD.md").write_text("# Project 7556\n", encoding="utf-8")
            outside = root / "outside-notes.md"
            outside.write_text("outside\n", encoding="utf-8")
            make_link(project / "NOTES.md", outside)
            from local_executor.markdown_editor import apply_updates

            with self.assertRaises(PolicyError):
                apply_updates(project, Task.from_dict(valid_task(notes_to_add=["Approved note"])))
            self.assertEqual(outside.read_text(encoding="utf-8"), "outside\n")

    def test_path_replacement_detected_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            card = project / "PROJECT_CARD.md"
            card.write_text("# Project 7556\n", encoding="utf-8")
            outside = root / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            card.unlink()
            make_link(card, outside)
            from local_executor.markdown_editor import apply_updates

            with self.assertRaises(PolicyError):
                apply_updates(project, Task.from_dict(valid_task(confirmed_facts=["Approved fact"])))
            self.assertEqual(outside.read_text(encoding="utf-8"), "outside\n")


if __name__ == "__main__":
    unittest.main()
