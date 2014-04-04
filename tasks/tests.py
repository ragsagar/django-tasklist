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
                'title': 'Test task 1',
                'done': False,
                'priority': 1,
                'module': 'CRM',
                'due_date': datetime.date(2014, 4, 2),
                'type': 3,
                'description': 'testing task',
                'assigned_user': user,
                }
        self.task = Task.objects.create(**data)
        self.client.login(username='ragsagar', password='password')

    def test_list_tasks_view(self):
        """
        Tests for the view to list all tasks.
        """
        list_tasks_url = reverse('list_tasks')
        response = self.client.get(list_tasks_url)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(len(response.context_data['task_list']), tasks.count())

    def test_detail_task_view(self):
        """
        Test detail task view page.
        """
        detail_url = reverse('task_detail', kwargs={'pk': self.task.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['task'], self.task)

    def test_create_task_view(self):
        """
        Test view to create new task.
        """
        create_task_url = reverse('create_task')
        response = self.client.get(create_task_url)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='ragsagar')
        data =  {
                'title': 'Test task 2',
                'priority': 1,
                'module': 'HRMS',
                'due_date': datetime.date(2014, 4, 5),
                'type': 1,
                'description': 'This is a description',
                'assigned_user_id': user.pk,
                }
        response = self.client.post(create_task_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 2)
        
