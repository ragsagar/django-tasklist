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

    def create_task(self,
                    title="Test task",
                    status=1,
                    priority=1,
                    due_date=None):
        if not due_date:
            due_date = datetime.date.today() + datetime.timedelta(days=1)
        data =  {
                'created_by': self.user,
                'title': title,
                'priority': priority,
                'module': 'CRM',
                'due_date': due_date,
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

    def tesk_task_url(self):
        """
        Test if the absolute url of task is the url to detail page.
        """
        task = self.create_task()
        url = reverse('task_detail', kwargs={'pk': task.pk})
        self.assertEqual(str(task.get_absolute_url()), url)

    def test_task_object_methods(self):
        """
        Test the helper methods in Task.
        """
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        yesterday = today - datetime.timedelta(days=1)
        completed_task = self.create_task(status=Task.STATUS_CHOICES.complete)
        incomplete_task = self.create_task(title="New task", due_date=tomorrow)
        self.create_task(status=Task.STATUS_CHOICES.incomplete)
        due_task = self.create_task(title='Incomplete due task',
                                    due_date=yesterday)
        self.assertEqual(completed_task.is_due(), False)
        self.assertEqual(due_task.is_due(), True)
        self.assertEqual(incomplete_task.is_due(), False)

