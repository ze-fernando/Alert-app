from django.test import TestCase
from .models import User, Task
from datetime import datetime

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User(name="Test User", email="test@example.com", password="password123")
        self.assertTrue(isinstance(user, User))
        self.assertEqual("password123", user.password)

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User(name="Test User", email="test@example.com", password="password123")

    def test_create_task(self):
        task = Task(task="Test Task", user=self.user, hourSend="12:30:00")
        self.assertTrue(isinstance(task, Task))

    def test_task_created_date(self):
        task = Task(task="Test Task", user=self.user, hourSend="12:30:00")
        self.assertTrue(isinstance(task.created, datetime))

    def test_task_hour_send(self):
        task = Task(task="Test Task", user=self.user, hourSend="12:30:00")
        self.assertEqual(str(task.hourSend), "12:30:00")
