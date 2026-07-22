import tempfile
import unittest
from pathlib import Path

from local_executor.errors import PolicyError
from local_executor.policy_engine import detect_naming_conflicts, enforce_task_policy
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


if __name__ == "__main__":
    unittest.main()
