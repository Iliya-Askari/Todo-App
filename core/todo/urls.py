from django.urls import path
from .views import TaskList,TaskCreate,TaskComplete,TaskDeleteView

app_name = 'todo'

urlpatterns = [
    path("", TaskList.as_view(), name="task_list"),
    path("create/", TaskCreate.as_view(), name="create_task"),
    path("complete/<int:pk>/", TaskComplete.as_view(), name="complete_task"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="delete_task"),
]