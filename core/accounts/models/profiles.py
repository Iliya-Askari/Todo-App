from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from accounts.api.utils import EmailThread

from .users import Users


class Profile(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=Users)
def save_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(reset_password_token_created)
def reset_password_token(sender, instance, reset_password_token, **kwargs):
    subject = "Reset your password"
    message = f"""Click the link below to reset your password: {reset_password_token.key}
    http://127.0.0.1:8000/accounts/api/v1/api/password_reset/confirm/"""
    recipient_list = [reset_password_token.user.email]
    EmailThread(subject, message, recipient_list).start()
