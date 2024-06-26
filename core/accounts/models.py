from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission)
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
from accounts.api.utils import EmailThread
class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password , **extra_fields):
        """
        Create and save a user with the given email and password. and extera data
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password. and extera data
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class Users(AbstractBaseUser,PermissionsMixin):
    """
    coustoum user model for our app
    """
    email = models.EmailField(max_length=255,unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # related_name سفارشی برای جلوگیری از تداخل
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # related_name سفارشی برای جلوگیری از تداخل
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )



    objects = UserManager()
    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image =  models.ImageField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

@receiver(post_save,sender=Users)
def save_profile(sender,created,instance,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(reset_password_token_created)
def reset_password_token(sender, instance, reset_password_token, **kwargs):
    subject = 'Reset your password'
    message = f'''Click the link below to reset your password: {reset_password_token.key}
    http://127.0.0.1:8000/accounts/api/v1/api/password_reset/confirm/'''
    recipient_list = [reset_password_token.user.email]
    EmailThread(subject, message, recipient_list).start()