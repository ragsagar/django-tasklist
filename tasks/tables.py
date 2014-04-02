import django_tables2 as tables

from .models import Task

class TaskTable(tables.Table):
    class Meta:
        model = Task
        attrs = {'class': 'table '}
        exclude = ('last_modified',)
        order_by = '-created'
        per_page = 20
