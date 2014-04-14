import json

from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, CreateView, DetailView, UpdateView,
    TemplateView, View)
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from braces.views import (LoginRequiredMixin, StaffuserRequiredMixin,
        StaticContextMixin, JSONResponseMixin)
from django_tables2.views import SingleTableMixin, SingleTableView

from .models import Task
from .tables import TaskTable


class BaseListTasksView(LoginRequiredMixin,  SingleTableView):
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
        return queryset.select_related('assigned_user')


class ListTasksView(BaseListTasksView):
    """
    View to list all tasks excluding 
    """
    exclude_filters = {'status': Task.STATUS_CHOICES.complete}


class ListIncompleteTasksView(StaticContextMixin, BaseListTasksView):
    """
    View to list just incomplete tasks.
    """
    filters = {'status': Task.STATUS_CHOICES.incomplete}
    static_context = {"incomplete_menu": True}


class ListUnReviewedTasksView(StaticContextMixin, BaseListTasksView):
    """
    View to list only the tasks that are ready to be reviewed
    """
    filters = {'status': Task.STATUS_CHOICES.ready_for_review}
    static_context = {"unreviewed_menu": True}


class ListCompletedTasksView(StaticContextMixin, BaseListTasksView):
    """
    View to list only the tasks that are completed.
    """
    filters = {'status': Task.STATUS_CHOICES.complete}
    static_context = {"completed_menu": True}
        
    
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

class ReportHomeView(LoginRequiredMixin, TemplateView):
    """
    View to render template for report home view
    """
    template_name = 'tasks/report.html'

    def get_context_data(self, **kwargs):
        """
        Adding some data to the context
        """
        context = super(ReportHomeView, self).get_context_data(**kwargs)
        tasks = Task.objects.all()
        incomplete_tasks = tasks.filter(status=Task.STATUS_CHOICES.incomplete)
        unreviewed_tasks = tasks.filter(status=Task.STATUS_CHOICES.ready_for_review)
        completed_tasks = tasks.filter(status=Task.STATUS_CHOICES.complete)
        context['incomplete_task_count'] = incomplete_tasks.count()
        context['unreviewed_tasks_count'] = unreviewed_tasks.count()
        context['completed_tasks'] = completed_tasks.count()
        return context

class TasksByStatusJsonView(LoginRequiredMixin, JSONResponseMixin, View):
    """
    Returns the task by its status
    """
    def get(self, request, *args, **kwargs):
        """
        Get all task and return a json data of tasks 
        by its status
        """
        return HttpResponse()


