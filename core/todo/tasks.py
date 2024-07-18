from celery import shared_task
from todo.models import Task

@shared_task
def delete_task():
    oldest_task = Task.objects.order_by('created_date').first()
    if oldest_task:
        oldest_task.delete()
        return f"Task with ID {oldest_task.id} deleted successfully"
    elif Task.objects.count() == 0:
        return "No tasks to delete. No new tasks available."
    else:
        return "No tasks to delete"