from .models import Task

def task_count(request):
    """
    To make the count of unreviewed tasks available in menu navbar.
    """
    unreviewed_tasks = Task.objects.filter(
                            status=Task.STATUS_CHOICES.ready_for_review)
    return {'unreviewed_task_count': unreviewed_tasks.count()}
