import tempfile
import unittest
from pathlib import Path

from local_executor.errors import PolicyError, TaskValidationError
from local_executor.runtime_guard import safe_runtime_path, validate_task_id


class RuntimeGuardTests(unittest.TestCase):
    def test_valid_identifier_characters(self):
        self.assertEqual(validate_task_id("2026.07_7556-fix"), "2026.07_7556-fix")

    def test_malicious_identifiers_rejected(self):
        values = ["..", "a..b", "../escape", "a/b", "a\\b", r"C:\escape", r"\\server\share", ".hidden", "name.", "CON", "con.txt", "PRN", "COM1", "LPT9", "a" * 129]
        for value in values:
            with self.subTest(value=value), self.assertRaises(TaskValidationError):
                validate_task_id(value)

    def test_canonical_runtime_containment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "runtime"
            inside = safe_runtime_path(root, "reports", "safe.json")
            self.assertEqual(inside, (root / "reports/safe.json").resolve())
            with self.assertRaises(PolicyError):
                safe_runtime_path(root, "..", "escape.json")


if __name__ == "__main__":
    unittest.main()
