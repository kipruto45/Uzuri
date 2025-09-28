from rest_framework.routers import DefaultRouter
from .views import APITokenViewSet, APIUsageLogViewSet

router = DefaultRouter()
router.register(r'api-tokens', APITokenViewSet)
router.register(r'api-usage-logs', APIUsageLogViewSet)

urlpatterns = router.urls
