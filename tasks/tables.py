import django_tables2 as tables
from django_tables2.utils import A

from .models import Task

class TaskTable(tables.Table):
    id = tables.LinkColumn('task_detail', args=[A('pk')])
    created = tables.Column(visible=False)

    def render_assigned_user(self, value):
        """
        Show full name if available.
        """
        return value.get_full_name() or value

    class Meta:
        model = Task
        attrs = {'class': 'table table-condensed rowlink', }
        fields = ('id', 'title', 'due_date', 'module', 'priority', 'assigned_user', 'type', 'status')
        order_by = '-created'
        per_page = 15
