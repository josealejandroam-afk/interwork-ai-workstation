import unittest
import json
import tempfile
from pathlib import Path

from local_executor.errors import TaskValidationError
from local_executor.task_schema import Task
from local_executor.task_loader import load_task


def valid_task(**overrides):
    data = {
        "task_id": "test-7556", "project_number": "7556",
        "client_slug": "marsh_mclennan", "project_slug": "7556_mma_art_work_dallas",
        "action": "apply_project_update", "allowed_paths": [
            "memory/clients/marsh_mclennan/projects/7556_mma_art_work_dallas/"
        ],
    }
    data.update(overrides)
    return data


class TaskSchemaTests(unittest.TestCase):
    def test_valid_task(self):
        self.assertEqual(Task.from_dict(valid_task()).project_number, "7556")

    def test_missing_project_number_rejected(self):
        data = valid_task()
        del data["project_number"]
        with self.assertRaisesRegex(TaskValidationError, "project_number"):
            Task.from_dict(data)

    def test_conflicting_folder_number_rejected(self):
        with self.assertRaisesRegex(TaskValidationError, "conflicts"):
            Task.from_dict(valid_task(project_slug="9999_wrong"))

    def test_prohibited_requested_action_rejected(self):
        with self.assertRaisesRegex(TaskValidationError, "prohibited"):
            Task.from_dict(valid_task(requested_actions=["git_push"], prohibited_actions=["git_push"]))

    def test_placeholder_rejected(self):
        with self.assertRaisesRegex(TaskValidationError, "placeholder"):
            Task.from_dict(valid_task(notes_to_add=["TBD"]))

    def test_malformed_json_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "task.json"
            path.write_text("{not-json", encoding="utf-8")
            with self.assertRaisesRegex(TaskValidationError, "invalid task JSON"):
                load_task(path)


if __name__ == "__main__":
    unittest.main()
