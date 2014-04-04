import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='ragsagar', password='password')
        data =  {
                'created_by': user,
                'title': 'Test task 2',
                'done': False,
                'priority': 1,
                'module': 'CRM',
                'due_date': datetime.date(2014, 4, 2),
                'type': 3,
                'description': 'testing task',
                'assigned_user': user,
                }
        Task.objects.create(**data)

    def test_list_tasks(self):
        """
        Tests for the view to list all tasks.
        """
        list_tasks_url = reverse('list_tasks')
        self.client.login(username='ragsagar', password='password')
        response = self.client.get(list_tasks_url)
        self.assertEqual(response.status_code, 200)

