from rest_framework.routers import DefaultRouter
from .views import AppStoreAppViewSet

router = DefaultRouter()
router.register(r'apps', AppStoreAppViewSet)

urlpatterns = router.urls
