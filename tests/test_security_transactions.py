import json
import subprocess
import tempfile
import unittest
import os
from pathlib import Path
from unittest.mock import patch

from local_executor.errors import ExecutorError, ExecutionError, PolicyError
from local_executor.executor import execute
from local_executor.policy_engine import scan_for_secrets
from local_executor.report_generator import write_report
from local_executor.runtime_state import ProjectLock, finalize_recovery, inspect_lock
from local_executor.git_manager import verify_expected_changes as real_verify_expected_changes
from local_executor.atomic_io import atomic_write_bytes
from local_executor.markdown_editor import apply_updates as real_apply_updates
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

            def fail_after_stage(repo_path, message, paths, expected, hooks_dir):
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

    def test_externally_created_optional_file_is_not_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, project, card, task = fixture(root)
            task.write_text(json.dumps(valid_task(task_id="external-optional", notes_to_add=["Approved note"])), encoding="utf-8")
            notes = project / "NOTES.md"

            def external_then_apply(project_path, task_value, on_write=None, originally_absent=None):
                notes.write_text("external content\n", encoding="utf-8")
                return real_apply_updates(project_path, task_value, on_write=on_write, originally_absent=originally_absent)

            with patch("local_executor.executor.apply_updates", side_effect=external_then_apply):
                with self.assertRaisesRegex(ExecutorError, "appeared externally"):
                    execute(task, repo, runtime)
            self.assertEqual(notes.read_text(encoding="utf-8"), "external content\n")
            self.assertEqual(card.read_text(encoding="utf-8"), "# Project 7556\n")

    def test_external_edit_after_executor_write_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, project, card, task = fixture(root)
            notes = project / "NOTES.md"

            def external_edit_then_fail(*args, **kwargs):
                notes.write_text("external replacement\n", encoding="utf-8")
                raise ExecutionError("simulated validation failure")

            with patch("local_executor.executor.validate", side_effect=external_edit_then_fail):
                with self.assertRaisesRegex(ExecutionError, "manual recovery"):
                    execute(task, repo, runtime)
            self.assertEqual(notes.read_text(encoding="utf-8"), "external replacement\n")
            self.assertEqual(card.read_text(encoding="utf-8"), "# Project 7556\n")
            records = list((runtime / "queue/manual_recovery/security-7556").glob("*.json"))
            self.assertEqual(len(records), 1)
            self.assertNotIn("external replacement", records[0].read_text(encoding="utf-8"))

    def test_external_edit_between_validation_and_staging_refuses_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, _, card, task = fixture(root)

            def edit_before_verify(repo_path, expected):
                card.write_text(card.read_text(encoding="utf-8") + "external edit\n", encoding="utf-8")
                return real_verify_expected_changes(repo_path, expected)

            with patch("local_executor.executor.verify_expected_changes", side_effect=edit_before_verify):
                with self.assertRaisesRegex(ExecutionError, "changed after validation"):
                    execute(task, repo, runtime)
            self.assertIn("external edit", card.read_text(encoding="utf-8"))
            self.assertEqual(git(repo, "log", "--format=%s", "-1"), "fixture")

    def test_atomic_write_interruption_preserves_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "PROJECT_CARD.md"
            path.write_bytes(b"original\n")
            with patch("local_executor.atomic_io.os.replace", side_effect=OSError("simulated interruption")):
                with self.assertRaises(OSError):
                    atomic_write_bytes(path, b"replacement\n")
            self.assertEqual(path.read_bytes(), b"original\n")
            self.assertEqual(list(path.parent.glob(".local-executor-*.tmp")), [])

    def test_git_hooks_and_signing_are_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, _, _, task = fixture(root)
            sentinel = root / "hook-ran.txt"
            hook = repo / ".git/hooks/pre-commit"
            hook.write_text(f"#!/bin/sh\necho ran > '{sentinel.as_posix()}'\nexit 1\n", encoding="utf-8", newline="\n")
            os.chmod(hook, 0o755)
            git(repo, "config", "commit.gpgSign", "true")
            result = execute(task, repo, runtime)
            self.assertEqual(result["status"], "completed")
            self.assertFalse(sentinel.exists())

    def test_keyboard_interrupt_creates_recoverable_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime, project, _, task = fixture(root)
            with patch("local_executor.executor.apply_updates", side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    execute(task, repo, runtime)
            self.assertFalse((runtime / "queue/running/security-7556.json").exists())
            self.assertTrue((runtime / "queue/interrupted/security-7556/attempt-1.json").exists())
            self.assertFalse(inspect_lock(runtime, project)["locked"])


if __name__ == "__main__":
    unittest.main()
