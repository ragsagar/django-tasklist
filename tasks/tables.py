from django.utils.safestring import mark_safe

import django_tables2 as tables
from django_tables2.utils import A

from .models import Task


STATUS_SYMBOL_MAP = {
        Task.STATUS_CHOICES.complete: 'ok',
        Task.STATUS_CHOICES.incomplete: 'minus-sign',
        Task.STATUS_CHOICES.ready_for_review: 'thumbs-up'
        }

PRIORTY_BADGE_MAP = {
        Task.PRIORITY_CHOICES.low: '',
        Task.PRIORITY_CHOICES.medium: 'alert-warning',
        Task.PRIORITY_CHOICES.high: 'alert-danger'
        }

class TaskTable(tables.Table):
    id = tables.LinkColumn('task_detail', args=[A('pk')])
    created = tables.Column(visible=False)

    def render_due_date(self, value, record):
        """
        Render thumbs down symbol if the task crossed due date.
        """
        if record.is_due():
            symbol = " <span class='glyphicon glyphicon-thumbs-down'></span>"
        else:
            symbol = ""
        return mark_safe(value.strftime("%b %d, %Y") + symbol)

    def render_assigned_user(self, value):
        """
        Show full name if available.
        """
        return value.get_full_name() or value

    def render_priority(self, value, record):
        """
        Give different coloured badges to different priority.
        """
        badge = PRIORTY_BADGE_MAP.get(record.priority)
        return mark_safe("<span class='badge {}'>{}</span>".format(badge, value))

    def render_status(self, value, record):
        """
        Show icons instead of show status display text.
        """
        symbol_html = "<span class='glyphicon glyphicon-{}'></span>"
        # Using record.status as `value` will contain the get_status_display()
        # result.
        symbol_html = symbol_html.format(STATUS_SYMBOL_MAP[record.status])
        return mark_safe(symbol_html)

    class Meta:
        model = Task
        attrs = {'class': 'table table-condensed rowlink', }
        fields = ('id', 'title', 'due_date', 'module', 'priority', 'assigned_user', 'type', 'status')
        order_by = '-created'
        per_page = 15
