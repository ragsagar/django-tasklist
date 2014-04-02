from django.conf.urls import patterns, include, url

from .views import ListTasksView, CreateTaskView

urlpatterns = patterns('',
    url(r'^$', ListTasksView.as_view(), name='list_tasks'),
    url(r'^create/$', CreateTaskView.as_view(), name='create_task'),
)
