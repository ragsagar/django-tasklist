import datetime
import json

from django.db.models import Count

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ..models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = self.create_user()
        self.client.login(username='ragsagar', password='password')
        self.task = self.create_task()
        self.create_task(title="Completed Task",
                         status=Task.STATUS_CHOICES.complete)
        self.create_task(title="Task Ready for Review",
                         status=Task.STATUS_CHOICES.ready_for_review)

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

    def test_list_tasks_view(self):
        """
        Tests for the view to list all tasks.
        """
        list_tasks_url = reverse('list_tasks')
        response = self.client.get(list_tasks_url)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all().exclude(status=Task.STATUS_CHOICES.complete)
        self.assertEqual(len(response.context_data['task_list']), tasks.count())
        self.assertNotIn(
            Task.STATUS_CHOICES.complete,
            response.context_data['task_list'].values_list('status', flat=True))
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertIn(str(self.task.get_absolute_url()),
                      response.rendered_content)

    def test_list_incomplete_tasks_view(self):
        """
        Tests for the view to list all tasks.
        """
        list_tasks_url = reverse('list_incomplete_tasks')
        response = self.client.get(list_tasks_url)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.filter(status=Task.STATUS_CHOICES.incomplete)
        self.assertEqual(len(response.context_data['task_list']), tasks.count())
        status_of_all_tasks = response.context_data['task_list'].values_list(
                                                            'status',
                                                            flat=True)
        self.assertNotIn(Task.STATUS_CHOICES.complete, status_of_all_tasks)
        self.assertNotIn(Task.STATUS_CHOICES.ready_for_review,
                         status_of_all_tasks)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertIn(str(self.task.get_absolute_url()),
                      response.rendered_content)

    def test_list_unreviewed_tasks_view(self):
        """
        Tests for the view to list all tasks.
        """
        list_tasks_url = reverse('list_unreviewed_tasks')
        response = self.client.get(list_tasks_url)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.filter(status=Task.STATUS_CHOICES.ready_for_review)
        self.assertEqual(len(response.context_data['task_list']), tasks.count())
        status_of_all_tasks = response.context_data['task_list'].values_list(
                                                            'status',
                                                            flat=True)
        self.assertNotIn(Task.STATUS_CHOICES.complete, status_of_all_tasks)
        self.assertNotIn(Task.STATUS_CHOICES.incomplete, status_of_all_tasks)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertNotIn(str(self.task.get_absolute_url()),
                         response.rendered_content)

    def test_list_completed_tasks_view(self):
        """
        Tests for the view to list all tasks.
        """
        list_tasks_url = reverse('list_completed_tasks')
        response = self.client.get(list_tasks_url)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.filter(status=Task.STATUS_CHOICES.complete)
        self.assertEqual(len(response.context_data['task_list']), tasks.count())
        status_of_all_tasks = response.context_data['task_list'].values_list(
                                                            'status',
                                                            flat=True)
        self.assertNotIn(Task.STATUS_CHOICES.ready_for_review, status_of_all_tasks)
        self.assertNotIn(Task.STATUS_CHOICES.incomplete, status_of_all_tasks)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertNotIn(str(self.task.get_absolute_url()),
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


    def test_report_home_view(self):
        """
        Test the report home view
        """
        url = reverse('report_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        incomplete_tasks_count = tasks.filter(
                    status=Task.STATUS_CHOICES.incomplete).count()
        unreviewed_tasks_count = tasks.filter(
                    status=Task.STATUS_CHOICES.ready_for_review).count()
        completed_tasks_count = tasks.filter(
                    status=Task.STATUS_CHOICES.complete).count()
        self.assertEqual(response.context_data['incomplete_task_count'],
                         incomplete_tasks_count)
        self.assertEqual(response.context_data['unreviewed_tasks_count'],
                         unreviewed_tasks_count)
        self.assertEqual(response.context_data['unreviewed_tasks_count'],
                         completed_tasks_count)

    def test_tasks_json_view(self):
        """
        Test the json view of tasks by status and module.
        """
        url = reverse('task_by_status_json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        tasks_by_status = [
            {'data': 1, 'label': 'Incomplete'},
            {'data': 1, 'label': 'Ready for Review'},
            {'data': 1, 'label': 'Complete'}
        ]
        tasks_by_module = [{'data': 3, 'label': u'CRM'}]
        
        json_string = response.content
        data = json.loads(json_string)
        self.assertEqual(data.get('task_by_status'), tasks_by_status)
        self.assertEqual(data.get('task_by_module'), tasks_by_module)
        
