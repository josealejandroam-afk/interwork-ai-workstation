import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from local_executor.executor import execute
from tests.test_task_schema import valid_task


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


class EndToEnd7556Tests(unittest.TestCase):
    def test_task_backs_up_validates_commits_reports_and_rolls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = root / "repo", root / "runtime"
            project = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
            project.mkdir(parents=True)
            (project / "PROJECT_CARD.md").write_text("# Project 7556 - MMA\n\nLegacy label: MMC RES.\n", encoding="utf-8")
            (project / "OPEN_LOOPS.md").write_text("# Open Loops\n\n| # | Item | Status |\n|---|---|---|\n| 1 | Confirm closeout | Open |\n", encoding="utf-8")
            git(repo, "init", "-b", "codex/test")
            git(repo, "config", "user.email", "test@example.invalid")
            git(repo, "config", "user.name", "Test")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "fixture")
            start = git(repo, "rev-parse", "HEAD")
            task_data = valid_task(
                task_id="e2e-7556", confirmed_facts=[{"field": "Confirmed item", "value": "Example only"}],
                open_loops_to_add=["Review generated diff"], open_loops_to_resolve=["Confirm closeout"],
                notes_to_add=["Deterministic test note"], drafts_to_save=[],
                prohibited_actions=["git_push", "supabase_write", "send_email", "send_teams", "delete_files"],
            )
            task_path = root / "task.json"
            task_path.write_text(json.dumps(task_data), encoding="utf-8")
            result = execute(task_path, repo, runtime)
            self.assertNotEqual(result["ending_commit"], start)
            self.assertFalse(result["push_performed"])
            self.assertTrue(Path(result["diff_path"]).exists())
            self.assertTrue(Path(result["report_path"]).exists())
            self.assertTrue((runtime / "backups/e2e-7556/attempt-1/manifest.json").exists())
            self.assertEqual(len(result["conflicts"]), 1)
            (repo / "unrelated.txt").write_text("preserve me\n", encoding="utf-8")
            git(repo, "add", "unrelated.txt")
            git(repo, "commit", "-m", "unrelated later work")
            git(repo, "revert", "--no-edit", result["ending_commit"])
            self.assertEqual((project / "PROJECT_CARD.md").read_text(encoding="utf-8"), "# Project 7556 - MMA\n\nLegacy label: MMC RES.\n")
            self.assertEqual((repo / "unrelated.txt").read_text(encoding="utf-8"), "preserve me\n")


if __name__ == "__main__":
    unittest.main()
