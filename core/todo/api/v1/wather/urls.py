# urls.py

from django.urls import path
from .views import get_weather_mashhad

urlpatterns = [
    path('', get_weather_mashhad, name='get_weather_mashhad'),
]
