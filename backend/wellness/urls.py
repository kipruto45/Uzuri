from rest_framework.routers import DefaultRouter
from .views import WellnessResourceViewSet, CounselingAppointmentViewSet

router = DefaultRouter()
router.register(r'wellness-resources', WellnessResourceViewSet)
router.register(r'counseling-appointments', CounselingAppointmentViewSet)

urlpatterns = router.urls
