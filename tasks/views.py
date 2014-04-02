from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin
from django_tables2.views import SingleTableMixin, SingleTableView

from .models import Task
from .tables import TaskTable


class ListTasksView(LoginRequiredMixin, SingleTableView):
    """
    View to list all tasks.
    """
    model = Task
    table_class = TaskTable


class CreateTaskView(LoginRequiredMixin, CreateView):
    """
    View to create new tasks.
    """
    model = Task
    success_url = reverse_lazy('list_tasks')

    def post(self, request, *args, **kwargs):
        """
        Overriding default method to add support of cancel button.
        """
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse_lazy('list_tasks'))
        return super(CreateTaskView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overriding default functionality for saving the user who created the
        task.
        """
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('list_tasks'))

class DetailTaskView(LoginRequiredMixin, DetailView):
    """
    View to show the details of a task.
    """
    model = Task
