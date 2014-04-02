from django.db import models
from django.conf import settings

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
                                      related_name='assigned_tasks')
    type = models.PositiveIntegerField(choices=TYPE_CHOICES,
                                       default=TYPE_CHOICES.task)
    done = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return self.title
