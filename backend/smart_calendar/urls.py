from rest_framework.routers import DefaultRouter
from .views import SmartEventViewSet

router = DefaultRouter()
router.register(r'smart-events', SmartEventViewSet)

urlpatterns = router.urls
