import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from local_executor.errors import ExecutionError
from local_executor.watcher import ensure_branch, run_cycle
from tests.test_task_schema import valid_task


def git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()


class WatcherTests(unittest.TestCase):
    def _make_repo(self, root):
        repo = root / "repo"
        project = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
        project.mkdir(parents=True)
        (project / "PROJECT_CARD.md").write_text("# Project 7556 - MMA\n", encoding="utf-8")
        (project / "OPEN_LOOPS.md").write_text(
            "# Open Loops\n\n| # | Item | Status |\n|---|---|---|\n", encoding="utf-8",
        )
        git(repo, "init", "-b", "main")
        git(repo, "config", "user.email", "test@example.invalid")
        git(repo, "config", "user.name", "Test")
        git(repo, "add", ".")
        git(repo, "commit", "-m", "fixture")
        return repo

    def _drop_task(self, runtime, **overrides):
        pending = runtime / "inbox/pending"
        pending.mkdir(parents=True, exist_ok=True)
        data = valid_task(**overrides)
        path = pending / f"{data['task_id']}.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_valid_task_is_picked_up_committed_and_archived(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            start = git(repo, "rev-parse", "HEAD")
            self._drop_task(runtime, task_id="watch-1", confirmed_facts=["Confirmed via watcher test"])
            results = run_cycle(repo, runtime)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["status"], "completed")
            self.assertNotEqual(git(repo, "rev-parse", "HEAD"), start)
            self.assertEqual(git(repo, "branch", "--show-current"), "executor/auto")
            self.assertTrue((runtime / "inbox/submitted/watch-1.json").exists())
            self.assertFalse((runtime / "inbox/pending/watch-1.json").exists())

    def test_prohibited_task_is_rejected_and_archived_with_no_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            start = git(repo, "rev-parse", "HEAD")
            self._drop_task(
                runtime, task_id="watch-bad", requested_actions=["git_push"], prohibited_actions=["git_push"],
            )
            results = run_cycle(repo, runtime)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["status"], "rejected")
            self.assertEqual(git(repo, "rev-parse", "HEAD"), start)
            self.assertTrue((runtime / "inbox/rejected/watch-bad.json").exists())
            self.assertTrue((runtime / "inbox/rejected/watch-bad.error.txt").exists())

    def test_dirty_repo_skips_cycle_without_consuming_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            (repo / "untracked-scratch.txt").write_text("dirty\n", encoding="utf-8")
            self._drop_task(runtime, task_id="watch-skip")
            results = run_cycle(repo, runtime)
            self.assertEqual(results, [])
            self.assertTrue((runtime / "inbox/pending/watch-skip.json").exists())
            self.assertEqual(git(repo, "branch", "--show-current"), "main")

    def test_malformed_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            pending = runtime / "inbox/pending"
            pending.mkdir(parents=True)
            (pending / "broken.json").write_text("{not-json", encoding="utf-8")
            results = run_cycle(repo, runtime)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["status"], "rejected")
            self.assertTrue((runtime / "inbox/rejected/broken.json").exists())
            self.assertTrue((runtime / "inbox/rejected/broken.error.txt").exists())

    def test_multiple_tasks_processed_in_one_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            self._drop_task(runtime, task_id="watch-multi-1", notes_to_add=["First"])
            self._drop_task(runtime, task_id="watch-multi-2", notes_to_add=["Second"])
            results = run_cycle(repo, runtime)
            self.assertEqual(len(results), 2)
            self.assertTrue(all(r["status"] == "completed" for r in results))
            self.assertTrue((runtime / "inbox/submitted/watch-multi-1.json").exists())
            self.assertTrue((runtime / "inbox/submitted/watch-multi-2.json").exists())

    def test_branch_is_created_from_main_not_current_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = self._make_repo(root)
            main_head = git(repo, "rev-parse", "main")
            git(repo, "switch", "-c", "unrelated")
            (repo / "unrelated.txt").write_text("other branch\n", encoding="utf-8")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "unrelated")
            ensure_branch(repo, "executor/auto")
            self.assertEqual(git(repo, "rev-parse", "HEAD"), main_head)

    def test_main_cannot_be_configured_as_watcher_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self._make_repo(Path(tmp))
            with self.assertRaises(ExecutionError):
                ensure_branch(repo, "main")

    def test_archive_collision_does_not_overwrite_prior_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            self._drop_task(runtime, task_id="watch-repeat")
            run_cycle(repo, runtime)
            first = runtime / "inbox/submitted/watch-repeat.json"
            first_content = first.read_text(encoding="utf-8")
            git(repo, "switch", "main")
            self._drop_task(runtime, task_id="watch-repeat", notes_to_add=["Repeated"])
            results = run_cycle(repo, runtime)
            self.assertEqual(results[0]["status"], "rejected")
            self.assertEqual(first.read_text(encoding="utf-8"), first_content)
            self.assertEqual(len(list((runtime / "inbox/rejected").glob("watch-repeat*.json"))), 1)


if __name__ == "__main__":
    unittest.main()
