from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'resources', ResourceViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = router.urls
