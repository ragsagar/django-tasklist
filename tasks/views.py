from django.shortcuts import render
from django.views.generic import ListView, CreateView
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

    def form_valid(self, form):
        """
        Overriding default functionality for saving the user who created the
        task.
        """
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
