from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[validate_email],
        error_messages={"invalid": "ایمیل وارد شده معتبر نمی‌باشد."},
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("رمزهای عبور با هم مطابقت ندارند.")
        if len(password1) < 8:
            raise ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد.")
        # شما می‌توانید قوانین بیشتری برای رمز عبور در اینجا اضافه کنید
        return password2
