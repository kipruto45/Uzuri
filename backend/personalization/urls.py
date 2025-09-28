from rest_framework.routers import DefaultRouter
from .views import PersonalizationProfileViewSet

router = DefaultRouter()
router.register(r'personalization-profiles', PersonalizationProfileViewSet)

urlpatterns = router.urls
