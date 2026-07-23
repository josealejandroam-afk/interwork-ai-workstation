import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from local_executor.remote_queue import RemoteClaim, run_remote_cycle
from tests.test_task_schema import valid_task


def git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()


class QueueClient:
    def __init__(self, task):
        self.claim_value = RemoteClaim("00000000-0000-0000-0000-000000000001", "claim-token", task)
        self.claim_calls = 0
        self.completions = []

    def claim(self, worker_id):
        self.claim_calls += 1
        value, self.claim_value = self.claim_value, None
        return value

    def complete(self, claim, result):
        self.completions.append((claim, result))
        return {"queue_id": claim.queue_id, "status": result["status"]}


class RemoteQueueTests(unittest.TestCase):
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

    def test_remote_task_is_claimed_committed_archived_and_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            client = QueueClient(valid_task(task_id="remote-1", notes_to_add=["Shared queue"]))
            results = run_remote_cycle(repo, runtime, client)
            self.assertEqual(results[-1]["status"], "completed")
            self.assertEqual(client.claim_calls, 1)
            self.assertEqual(client.completions[0][1]["task_id"], "remote-1")
            self.assertTrue((runtime / "inbox/submitted/remote-1.json").exists())
            self.assertEqual(git(repo, "branch", "--show-current"), "executor/auto")

    def test_dirty_repository_does_not_claim_remote_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            (repo / "scratch.txt").write_text("dirty\n", encoding="utf-8")
            client = QueueClient(valid_task(task_id="remote-dirty"))
            self.assertEqual(run_remote_cycle(repo, runtime, client), [])
            self.assertEqual(client.claim_calls, 0)
            self.assertEqual(client.completions, [])

    def test_expired_remote_claim_reconciles_local_completion_without_reexecution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            task = valid_task(task_id="remote-reconcile", notes_to_add=["Once"])
            first_client = QueueClient(task)
            first = run_remote_cycle(repo, runtime, first_client)
            ending_commit = git(repo, "rev-parse", "HEAD")
            completed = runtime / "queue/completed/remote-reconcile.json"
            self.assertTrue(completed.exists())

            second_client = QueueClient(task)
            second = run_remote_cycle(repo, runtime, second_client)
            self.assertEqual(second[-1]["status"], "completed")
            self.assertEqual(git(repo, "rev-parse", "HEAD"), ending_commit)
            self.assertEqual(len(second_client.completions), 1)
            self.assertEqual(second_client.completions[0][1]["ending_commit"], first[-1]["ending_commit"])

    def test_remote_policy_violation_is_rejected_and_completed_remotely(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            task = valid_task(
                task_id="remote-bad", requested_actions=["git_push"], prohibited_actions=["git_push"],
            )
            client = QueueClient(task)
            results = run_remote_cycle(repo, runtime, client)
            self.assertEqual(results[-1]["status"], "rejected")
            self.assertEqual(client.completions[0][1]["status"], "rejected")
            self.assertFalse((runtime / "inbox/pending/remote-bad.json").exists())

    def test_malformed_remote_payload_is_rejected_without_poisoning_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = self._make_repo(root), root / "runtime"
            client = QueueClient({"task_id": "remote-malformed"})
            results = run_remote_cycle(repo, runtime, client)
            self.assertEqual(results[-1]["status"], "rejected")
            self.assertIn("missing required field", results[-1]["error"])
            self.assertEqual(len(client.completions), 1)
            self.assertFalse((runtime / "inbox/pending/remote-malformed.json").exists())


if __name__ == "__main__":
    unittest.main()
