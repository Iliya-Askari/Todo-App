from django.urls import path
from accounts.api.v1 import view

app_name = 'profiles-urls'
urlpatterns = [
    path("", view.ProfileApiView.as_view(), name="profile-detail"),
]
