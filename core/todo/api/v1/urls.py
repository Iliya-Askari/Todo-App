from rest_framework import routers
from .views import *

"""
Create api  URL with the router
"""

app_name = "api-v1"

router = routers.DefaultRouter()
router.register("Tasklist", TaskViewSet, basename="tasklist")

urlpatterns = router.urls
