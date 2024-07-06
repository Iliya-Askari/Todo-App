from rest_framework import viewsets
from todo.models import Task
from .serializer import TaskSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .pagination import LargeResultsSetPagination
from .permissions import IsUserOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    """
    In this class, permissions and filters are implemented to improve performance
    """

    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {"complete"}
    ordering_fields = ["created_date"]
    pagination_class = LargeResultsSetPagination
