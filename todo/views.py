from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    View,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .tasks import delete_task
from .forms import UpdateTask
from .models import Task


# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    context_object_name = "tasks"
    model = Task

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = [
        "title",
    ]
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskComplete(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)


class TaskEdittView(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("todo:task_list")
    form_class = UpdateTask
    template_name = "todo/update_task.html"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def deleted_task(request):
    delete_task.delay()
    return HttpResponse("<h1>Delete Task successfully</h1>")