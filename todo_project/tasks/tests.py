from django.test import TestCase
from tasks.models.task_model import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            due_date="2025-02-01T10:00:00Z"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertFalse(self.task.completed)
