import django_tables2 as tables
from django_tables2.utils import A

from .models import Task

class TaskTable(tables.Table):
    id = tables.LinkColumn('task_detail', args=[A('pk')])

    class Meta:
        model = Task
        attrs = {'class': 'table table-condensed rowlink', }
        exclude = ('last_modified', 'created_by')
        order_by = '-created'
        per_page = 20
