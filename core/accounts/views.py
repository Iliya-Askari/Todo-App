from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect

from .forms import SignUpForm

# Create your views here.


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get(
            "next"
        )
        if next_url:
            return next_url
        return reverse_lazy("todo:task_list")


class RegisterPage(FormView):
    template_name = "accounts/register.html"
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo:task_list")
        return super(RegisterPage, self).get(*args, **kwargs)
