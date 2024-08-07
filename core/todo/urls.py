from django.urls import path, include
from .views import *

app_name = "todo"

urlpatterns = [
    path("", TaskList.as_view(), name="task_list"),
    path('delete-task/',deleted_task,name='delete-task'),
    path("create/", TaskCreate.as_view(), name="create_task"),
    path("complete/<int:pk>/", TaskComplete.as_view(), name="complete_task"),
    path("edit/<int:pk>/", TaskEdittView.as_view(), name="edit_task"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="delete_task"),
    path("api/v1/", include("todo.api.v1.urls")),
]
