from django.shortcuts import render
from django.views.generic import ListView , UpdateView, DeleteView,CreateView , View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Task
class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = 'index.html'
    model = Task

class TaskComplete(LoginRequiredMixin, View):
    template_name = 'index.html'
    model = Task
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'index.html'
    model = Task