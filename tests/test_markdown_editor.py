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

    def test_crlf_and_no_final_newline_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            card = project / "PROJECT_CARD.md"
            original = b"# Project 7556\r\n\r\nOriginal trailing spaces.  "
            card.write_bytes(original)
            task = Task.from_dict(valid_task(confirmed_facts=["Approved fact"]))
            apply_updates(project, task)
            result = card.read_bytes()
            self.assertTrue(result.startswith(original))
            self.assertNotIn(b"\n", result.replace(b"\r\n", b""))
            self.assertFalse(result.endswith((b"\r", b"\n")))

    def test_lf_and_final_newline_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            card = project / "PROJECT_CARD.md"
            original = b"# Project 7556\n\nUnrelated section.\n"
            card.write_bytes(original)
            task = Task.from_dict(valid_task(confirmed_facts=["Approved fact"]))
            apply_updates(project, task)
            result = card.read_bytes()
            self.assertTrue(result.startswith(original))
            self.assertNotIn(b"\r\n", result)
            self.assertTrue(result.endswith(b"\n"))

    def test_missing_optional_file_receives_only_approved_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "PROJECT_CARD.md").write_text("# Project 7556\n", encoding="utf-8")
            task = Task.from_dict(valid_task(notes_to_add=["Approved note"]))
            apply_updates(project, task)
            notes = (project / "NOTES.md").read_text(encoding="utf-8")
            self.assertIn("Approved note", notes)
            self.assertTrue(notes.startswith("# Notes\n"))


if __name__ == "__main__":
    unittest.main()
