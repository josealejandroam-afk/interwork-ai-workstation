import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from local_executor.executor import execute
from tests.test_task_schema import valid_task


def hashes(folder: Path) -> dict[str, str]:
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in folder.iterdir() if path.is_file()}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


class CopiedProject7556Tests(unittest.TestCase):
    def test_proposal_only_run_uses_copy_and_real_files_remain_byte_identical(self):
        source = Path(__file__).resolve().parents[1] / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
        before = hashes(source)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, runtime = root / "repo", root / "runtime"
            copied = repo / "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas"
            copied.parent.mkdir(parents=True)
            shutil.copytree(source, copied)
            git(repo, "init", "-b", "codex/copied-7556")
            git(repo, "config", "user.email", "test@example.invalid")
            git(repo, "config", "user.name", "Test")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "copied fixture")
            task_path = root / "task.json"
            task_path.write_text(json.dumps(valid_task(
                task_id="copied-7556-proposal", maximum_attempts=1,
                notes_to_add=["Proposal-only copied-project validation note"],
            )), encoding="utf-8")
            result = execute(task_path, repo, runtime, commit=False)
            self.assertEqual(result["status"], "proposal_generated")
            self.assertEqual(git(repo, "status", "--porcelain"), "")
            self.assertTrue(result["source_byte_identical"])
            self.assertFalse(result["final_execution_task_id_consumed"])
            self.assertTrue(Path(result["diff_path"]).exists())
            final_result = execute(task_path, repo, runtime)
            self.assertEqual(final_result["status"], "completed")
        self.assertEqual(hashes(source), before)


if __name__ == "__main__":
    unittest.main()
