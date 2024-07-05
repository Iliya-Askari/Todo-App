from django import forms
from .models import Task


class UpdateTask(forms.ModelForm):
    title = forms.CharField(max_length=255)

    class Meta:
        model = Task
        fields = ("title",)
