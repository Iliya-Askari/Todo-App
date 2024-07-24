from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string

from .forms import SignUpForm
from django.core.mail import send_mail
from core import settings
from accounts.api.utils import EmailThread
# Create your views here.


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
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
            email = form.cleaned_data["email"]
            token = self.get_tokens_for_user(user)
            subject = "Account Activation"
            message = render_to_string("email/activision_email.tpl", {"token": token})
            recipient_list = [email]
            email_thread = EmailThread(subject, message, recipient_list)
            email_thread.start()
        return super(RegisterPage, self).form_valid(form)
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo:task_list")
        return super(RegisterPage, self).get(*args, **kwargs)

        