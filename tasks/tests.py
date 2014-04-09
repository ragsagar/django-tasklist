import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = self.create_user()
        data =  {
                'created_by': self.user,
                'title': 'Test task 1',
                'priority': 1,
                'module': 'CRM',
                'due_date': datetime.date(2014, 4, 2),
                'type': 3,
                'description': 'testing task',
                'assigned_user': self.user,
                }
        self.task = Task.objects.create(**data)
        self.client.login(username='ragsagar', password='password')

    def create_user(self, **kwargs):
        user_data = {}
        user_data['username'] = 'ragsagar'
        user_data['password'] = 'password'
        user_data.update(kwargs)
        user = User.objects.create_user(**user_data)
        return user

    def test_list_tasks_view(self):
        """
        Tests for the view to list all tasks.
        """
        list_tasks_url = reverse('list_tasks')
        response = self.client.get(list_tasks_url)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(len(response.context_data['task_list']), tasks.count())
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertIn(str(self.task.get_absolute_url()),
                      response.rendered_content)

    def test_detail_task_view(self):
        """
        Test detail task view page.
        """
        detail_url = reverse('task_detail', kwargs={'pk': self.task.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['task'], self.task)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')

    def test_create_task_view(self):
        """
        Test view to create new task.
        """
        create_task_url = reverse('create_task')
        response = self.client.get(create_task_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
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
        old_count = Task.objects.all().count()
        response = self.client.post(create_task_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), old_count+1)
        
    def test_set_task_ready_view(self):
        """
        Test the view to set task status as ready to be reviewed.
        """
        self.task.status = Task.STATUS_CHOICES.incomplete
        self.task.save()
        pk = self.task.pk
        url = reverse('set_task_ready', kwargs={'pk': pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(pk=pk)
        self.assertEqual(task.status, Task.STATUS_CHOICES.ready_for_review)
        self.assertIsNotNone(task.completed_at)

    def test_set_task_incomplete_view(self):
        """
        Test the view to set task status as incomplete.
        """
        self.task.status = Task.STATUS_CHOICES.ready_for_review
        self.task.save()
        pk = self.task.pk
        url = reverse('set_task_incomplete', kwargs={'pk': pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(pk=pk)
        self.assertEqual(task.status, Task.STATUS_CHOICES.incomplete)

    def test_set_task_complete_view(self):
        """
        Test the view to set task status as complete
        """
        self.task.status = Task.STATUS_CHOICES.ready_for_review
        self.task.save()
        pk = self.task.pk
        url = reverse('set_task_complete', kwargs={'pk': pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        task = Task.objects.get(pk=pk)
        self.assertIsNone(task.reviewed_by)
        self.assertEqual(task.status, Task.STATUS_CHOICES.ready_for_review)
        # Create a staff user and login as staff user
        staff_user = self.create_user(username='staff_user',
                                      password='password',)
        staff_user.is_staff = True
        staff_user.save()
        self.client.login(username='staff_user', password='password')

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(pk=pk)
        self.assertEqual(task.reviewed_by, staff_user)
        self.assertEqual(task.status, Task.STATUS_CHOICES.complete)
