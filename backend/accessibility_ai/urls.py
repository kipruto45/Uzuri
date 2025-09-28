from rest_framework.routers import DefaultRouter
from .views import AccessibilityFeatureViewSet

router = DefaultRouter()
router.register(r'accessibility-features', AccessibilityFeatureViewSet)

urlpatterns = router.urls
