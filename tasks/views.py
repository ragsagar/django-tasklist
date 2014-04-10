import json

from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, CreateView, DetailView, UpdateView,
    View)
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django_tables2.views import SingleTableMixin, SingleTableView

from .models import Task
from .tables import TaskTable


class BaseListTasksView(LoginRequiredMixin, SingleTableView):
    """
    The base view that can list all tasks. Other actual view will apply just
    filters on this.
    """
    model = Task
    table_class = TaskTable
    filters = {}
    exclude_filters = {}

    def get_queryset(self):
        """
        Exclude completed tasks from normal listing.
        """
        queryset = super(BaseListTasksView, self).get_queryset()
        if self.filters:
            queryset = queryset.filter(**self.filters)
        if self.exclude_filters:
            queryset = queryset.exclude(**self.exclude_filters)
        return queryset


class ListTasksView(BaseListTasksView):
    """
    View to list all tasks excluding 
    """
    exclude_filters = {'status': Task.STATUS_CHOICES.complete}


class ListIncompleteTasksView(BaseListTasksView):
    """
    View to list just incomplete tasks.
    """
    filters = {'status': Task.STATUS_CHOICES.incomplete}


class ListUnReviewedTasksView(BaseListTasksView):
    """
    View to list only the tasks that are ready to be reviewed
    """
    filters = {'status': Task.STATUS_CHOICES.ready_for_review}


class ListCompletedTasksView(BaseListTasksView):
    """
    View to list only the tasks that are completed.
    """
    filters = {'status': Task.STATUS_CHOICES.complete}
        
    
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
        task.completed_at = timezone.now()
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
   

class SetTaskCompletedView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    """
    View to set a task as completed
    """
    raise_exception = True

    def post(self, request, *args, **kwargs):
        """
        View to set a task as completed.
        """
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.status = Task.STATUS_CHOICES.complete
        task.reviewed_by = request.user
        task.save()
        return HttpResponseRedirect(task.get_absolute_url())
