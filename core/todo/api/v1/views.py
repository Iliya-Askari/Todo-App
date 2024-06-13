from rest_framework import viewsets
from todo.models import Task
from .serializer import TaskSerializer

class TaskListViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer