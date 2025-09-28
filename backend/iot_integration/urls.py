from rest_framework.routers import DefaultRouter
from .views import IoTDeviceViewSet, AttendanceRecordViewSet

router = DefaultRouter()
router.register(r'iot-devices', IoTDeviceViewSet)
router.register(r'attendance-records', AttendanceRecordViewSet)

urlpatterns = router.urls
