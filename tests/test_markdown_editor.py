import tempfile
import unittest
from pathlib import Path

from local_executor.markdown_editor import apply_updates
from local_executor.task_schema import Task
from tests.test_task_schema import valid_task


class MarkdownEditorTests(unittest.TestCase):
    def test_updates_and_resolution_preserve_existing_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "PROJECT_CARD.md").write_text("# Project 7556\n\nOriginal fact.\n", encoding="utf-8")
            (project / "OPEN_LOOPS.md").write_text(
                "# Loops\n\n| # | Item | Status |\n|---|---|---|\n| 1 | Confirm closeout | Open |\n", encoding="utf-8"
            )
            task = Task.from_dict(valid_task(
                confirmed_facts=[{"field": "Date", "value": "2026-07-22"}],
                open_loops_to_add=["Review diff"], open_loops_to_resolve=["Confirm closeout"],
            ))
            result = apply_updates(project, task)
            self.assertIn("Original fact.", (project / "PROJECT_CARD.md").read_text(encoding="utf-8"))
            self.assertIn("| 1 | Confirm closeout | Resolved |", (project / "OPEN_LOOPS.md").read_text(encoding="utf-8"))
            self.assertEqual(result["loops_resolved"], ["Confirm closeout"])


if __name__ == "__main__":
    unittest.main()
