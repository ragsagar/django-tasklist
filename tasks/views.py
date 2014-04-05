import json

from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, CreateView, DetailView, UpdateView,
    View)
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

    def get_queryset(self):
        """
        To filter for complete and incomplete tasks.
        """
        queryset = super(ListTasksView, self).get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


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
        return HttpResponseRedirect(reverse_lazy('list_tasks'))


class DetailTaskView(LoginRequiredMixin, DetailView):
    """
    View to show the details of a task.
    """
    model = Task


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    """
    View to update existing task.
    """
    model = Task

    def post(self, request, *args, **kwargs):
        """
        Overriding to handle cancel button.
        """
        if 'cancel' in request.POST:
            self.object = self.get_object()
            return HttpResponseRedirect(self.get_success_url())
        return super(UpdateTaskView, self).post(request, *args, **kwargs)


class ToggleTaskDoneView(LoginRequiredMixin, View):
    """
    View to toggle mark a task as done or not done.
    """
    def post(self, request, *args, **kwargs):
        """
        Get the task object and toggle the done flag.
        """
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.done = not task.done
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


class SetTaskReadyView(LoginRequiredMixin, View):
    """
    View to set a task ready for review.
    """
    def post(self, request, *args, **kwargs):
        """
        Set the task as ready for review.
        """
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.status = Task.STATUS_CHOICES.ready_for_review
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())


class SetTaskIncompleteView(LoginRequiredMixin, View):
    """
    View to set a task back to incomplete
    """
    def post(self, request, *args, **kwargs):
        """
        View to set a task as not ready for review.
        """
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.status = Task.STATUS_CHOICES.incomplete
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())
