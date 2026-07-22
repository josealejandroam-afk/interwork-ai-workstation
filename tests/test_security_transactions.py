import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from local_executor.errors import ExecutionError, PolicyError
from local_executor.executor import execute
from local_executor.policy_engine import scan_for_secrets
from local_executor.report_generator import write_report
from local_executor.runtime_state import ProjectLock, finalize_recovery, inspect_lock
from tests.test_task_schema import valid_task


def git(repo: Path, *args: str, check=True) -> str:
    result = subprocess.run(["git", *args], cwd=repo, check=check, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip()


def fixture(root: Path, *, content="# Project 7556\n"):
    repo, runtime = root / "repo", root / "runtime"
    project = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
    project.mkdir(parents=True)
    card = project / "PROJECT_CARD.md"
    card.write_text(content, encoding="utf-8")
    git(repo, "init", "-b", "codex/test")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "Test")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "fixture")
    task_path = root / "task.json"
    task_path.write_text(json.dumps(valid_task(task_id="security-7556", notes_to_add=["Safe note"])), encoding="utf-8")
    return repo, runtime, project, card, task_path


class SecurityTransactionTests(unittest.TestCase):
    def test_secret_source_stops_before_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = "-----BEGIN PRIVATE KEY-----"
            repo, runtime, _, _, task = fixture(root, content=f"# Project 7556\n{secret}\n")
            with self.assertRaisesRegex(PolicyError, "Potential secret"):
                execute(task, repo, runtime)
            self.assertFalse((runtime / "backups/security-7556").exists())
            error = (runtime / "reports/security-7556/attempt-1-error.json").read_text(encoding="utf-8")
            self.assertNotIn(secret, error)

    def test_dirty_and_prestaged_trees_are_refused_without_changes(self):
        for staged in (False, True):
            with self.subTest(staged=staged), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                repo, runtime, _, card, task = fixture(root)
                card.write_text("# Project 7556\nuser change\n", encoding="utf-8")
                if staged:
                    git(repo, "add", str(card.relative_to(repo)))
                before = git(repo, "status", "--porcelain")
                with self.assertRaisesRegex(ExecutionError, "clean"):
                    execute(task, repo, runtime)
                self.assertEqual(git(repo, "status", "--porcelain"), before)

    def test_failed_commit_unstages_executor_paths_and_restores_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, _, card, task = fixture(root)
            original = card.read_bytes()

            def fail_after_stage(repo_path, message, paths):
                git(repo_path, "add", "--", *paths)
                (repo_path / "unrelated.txt").write_text("outside change", encoding="utf-8")
                raise ExecutionError("simulated commit failure")

            with patch("local_executor.executor.make_local_commit", side_effect=fail_after_stage):
                with self.assertRaisesRegex(ExecutionError, "simulated"):
                    execute(task, repo, runtime)
            self.assertEqual(card.read_bytes(), original)
            self.assertEqual(git(repo, "diff", "--cached", "--name-only"), "")
            self.assertEqual((repo / "unrelated.txt").read_text(encoding="utf-8"), "outside change")

    def test_report_failure_after_commit_records_recovery_without_reverse_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, _, _, task = fixture(root)
            with patch("local_executor.executor.write_report", side_effect=OSError("simulated report failure")):
                result = execute(task, repo, runtime)
            self.assertEqual(result["status"], "committed_needs_recovery")
            self.assertEqual(git(repo, "status", "--porcelain"), "")
            self.assertEqual(git(repo, "rev-parse", "HEAD"), result["ending_commit"])
            recovery = json.loads(Path(result["recovery_record"]).read_text(encoding="utf-8"))
            self.assertEqual(recovery["commit_sha"], result["ending_commit"])
            completed = finalize_recovery(runtime, repo, result["task_id"], write_report)
            self.assertEqual(completed["status"], "completed")
            self.assertTrue((runtime / "queue/completed/security-7556.json").exists())

    def test_secret_patterns_and_business_phone(self):
        self.assertTrue(scan_for_secrets("Authorization: Bearer abcdefghijklmnopqrstuvwxyz"))
        self.assertTrue(scan_for_secrets("postgresql://user:password@example.invalid/db"))
        self.assertFalse(scan_for_secrets("Call Alejandro at 555-123-4567 for project 7556"))

    def test_two_task_ids_cannot_enter_same_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, project, _, _ = fixture(root)
            held = ProjectLock(runtime, project, "first-task").acquire()
            second = root / "second.json"
            second.write_text(json.dumps(valid_task(task_id="second-7556", notes_to_add=["Safe note"])), encoding="utf-8")
            try:
                with self.assertRaisesRegex(ExecutionError, "locked"):
                    execute(second, repo, runtime)
                self.assertEqual(inspect_lock(runtime, project)["task_id"], "first-task")
            finally:
                held.release()

    def test_lock_released_after_success_and_precommit_failure(self):
        for should_fail in (False, True):
            with self.subTest(should_fail=should_fail), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                repo, runtime, project, _, task = fixture(root)
                if should_fail:
                    with patch("local_executor.executor.apply_updates", side_effect=ExecutionError("simulated edit failure")):
                        with self.assertRaises(ExecutionError):
                            execute(task, repo, runtime)
                else:
                    execute(task, repo, runtime, commit=False)
                self.assertFalse(inspect_lock(runtime, project)["locked"])

    def test_failed_validation_restores_files_and_creates_no_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, _, card, task = fixture(root)
            original = card.read_bytes()
            start = git(repo, "rev-parse", "HEAD")
            with patch("local_executor.executor.validate", side_effect=ExecutionError("simulated validation failure")):
                with self.assertRaisesRegex(ExecutionError, "validation"):
                    execute(task, repo, runtime)
            self.assertEqual(card.read_bytes(), original)
            self.assertEqual(git(repo, "rev-parse", "HEAD"), start)
            self.assertEqual(git(repo, "diff", "--cached", "--name-only"), "")


if __name__ == "__main__":
    unittest.main()
