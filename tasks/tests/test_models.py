import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ..models import Task


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = self.create_user()
        #self.client.login(username='ragsagar', password='password')
        #self.task = self.create_task()
        #self.create_task(title="Completed Task",
                         #status=Task.STATUS_CHOICES.complete)
        #self.create_task(title="Task Ready for Review",
                         #status=Task.STATUS_CHOICES.ready_for_review)

    def create_task(self, title="Test task", status=1, priority=1):
        data =  {
                'created_by': self.user,
                'title': title,
                'priority': priority,
                'module': 'CRM',
                'due_date': datetime.date(2014, 4, 2),
                'type': 3,
                'description': 'testing task',
                'assigned_user': self.user,
                'status': status,
                }
        return Task.objects.create(**data)

    def create_user(self, **kwargs):
        user_data = {}
        user_data['username'] = 'ragsagar'
        user_data['password'] = 'password'
        user_data.update(kwargs)
        user = User.objects.create_user(**user_data)
        return user

    def test_task_creation(self):
        """
        Test the process of creation of tasks.
        """
        task = self.create_task()
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.__str__(), task.title)
