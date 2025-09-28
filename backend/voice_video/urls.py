from rest_framework.routers import DefaultRouter
from .views import CallSessionViewSet

router = DefaultRouter()
router.register(r'call-sessions', CallSessionViewSet)

urlpatterns = router.urls
