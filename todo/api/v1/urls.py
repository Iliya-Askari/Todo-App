from rest_framework import routers
from django.urls import path
from .views import TaskViewSet
from todo.api.v1.wather.views import get_weather_mashhad

app_name = "api-v1"

router = routers.DefaultRouter()
router.register("Tasklist", TaskViewSet, basename="tasklist")

urlpatterns = [
    path('weather/mashhad/', get_weather_mashhad, name='weather-mashhad'),
] + router.urls
