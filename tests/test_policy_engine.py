import tempfile
import unittest
from pathlib import Path

from local_executor.errors import PolicyError
from local_executor.policy_engine import detect_naming_conflicts, enforce_task_policy
from local_executor.policy_engine import scan_for_secrets
from local_executor.task_schema import Task
from tests.test_task_schema import valid_task


class PolicyTests(unittest.TestCase):
    def test_protected_field_rejected(self):
        task = Task.from_dict(valid_task(confirmed_facts=[{"field": "vendor_confirmed", "value": True}]))
        with self.assertRaisesRegex(PolicyError, "protected"):
            enforce_task_policy(task)

    def test_naming_conflict_reported_without_edit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "PROJECT_CARD.md"
            original = "# MMA project\nLegacy source calls this MMC RES.\n"
            path.write_text(original, encoding="utf-8")
            conflicts = detect_naming_conflicts([path])
            self.assertEqual(len(conflicts), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_high_confidence_secret_formats(self):
        samples = [
            "-----BEGIN RSA PRIVATE KEY-----",
            "eyJabcdefghijk.eyJabcdefghijkl.mnopqrstuvwxyz",
            "https://user:password@example.invalid/path",
            "ghp_abcdefghijklmnopqrstuvwxyz123456",
            "sk-proj-abcdefghijklmnopqrstuvwxyz",
            "AKIAABCDEFGHIJKLMNOP",
            "AccountKey=abcdefghijklmnopqrstuvwxyz",
            "https://example.invalid/hook?token=abcdefghijklmnopqrstuvwxyz",
        ]
        for sample in samples:
            with self.subTest(sample=sample[:12]):
                self.assertTrue(scan_for_secrets(sample))
        self.assertFalse(scan_for_secrets("Project 7556 - phone 706-555-0199"))


if __name__ == "__main__":
    unittest.main()
