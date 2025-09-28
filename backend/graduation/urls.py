from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GraduationEventViewSet, GraduationApplicationViewSet, GraduationClearanceViewSet, GraduationCertificateViewSet

router = DefaultRouter()
router.register(r'events', GraduationEventViewSet)
router.register(r'applications', GraduationApplicationViewSet)
router.register(r'clearances', GraduationClearanceViewSet)
router.register(r'certificates', GraduationCertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
