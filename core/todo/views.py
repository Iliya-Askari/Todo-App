from django.shortcuts import render
from django.views.generic import ListView , UpdateView, DeleteView,CreateView , View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
# Create your views here.
class TaskList(ListView):
    template_name = 'index.html'
    model = Task
class TaskCreate(CreateView):
    template_name = 'index.html'
    model = Task
class TaskUpdate(UpdateView):
    template_name = 'index.html'
    model = Task

class TaskComplete(View):
    template_name = 'index.html'
    model = Task
class TaskDeleteView(DeleteView):
    template_name = 'index.html'
    model = Task