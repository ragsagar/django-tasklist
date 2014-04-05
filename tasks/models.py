from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone

from model_utils import Choices

class TimeStampedModel(models.Model):
    """
    An abstract model for the common fields 'created' and 'last_modified'.
    """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(TimeStampedModel):
    """
    Model that represent a task.
    """
    PRIORITY_CHOICES = Choices((1, 'low', 'Low'),
                               (2, 'medium', 'Medium'),
                               (3, 'high', 'High'))
    TYPE_CHOICES = Choices((1, 'bug', 'Bug'),
                           (2, 'enhancement', 'Enhancement'),
                           (3, 'task', 'Task'),
                           (4, 'proposal', 'Proposal'))
    STATUS_CHOICES = Choices((1, 'incomplete', 'Incomplete'),
                             (2, 'read_for_review', 'Ready for Review'),
                             (3, 'complete', 'Complete'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True,
                                   blank=True,
                                   editable=False,
                                   related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True)
    module = models.CharField(max_length=100, blank=True)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES,
                                           default=PRIORITY_CHOICES.low)
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      null=True,
                                      blank=True,
                                      verbose_name="Assigned To",
                                      related_name='assigned_tasks')
    type = models.PositiveIntegerField(choices=TYPE_CHOICES,
                                       default=TYPE_CHOICES.task)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES,
                                         default=STATUS_CHOICES.incomplete,
                                         editable=False)
    done = models.BooleanField(editable=False, default=False)

    class Meta:
        ordering = ['-created']

    def is_due(self):
        """
        Return True if this task crossed due date, otherwise false.
        """
        if self.due_date < timezone.now().date():
            return True
        else:
            return False

    def is_due_today(self):
        """
        Check if the task due date is today
        """
        if self.due_date == timezone.now().date():
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
