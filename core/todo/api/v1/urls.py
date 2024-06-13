from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('Tasklist', TaskViewSet,basename="tasklist")

urlpatterns = router.urls