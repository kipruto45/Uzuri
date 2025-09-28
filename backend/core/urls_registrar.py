from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_registrar import *

router = DefaultRouter()
router.register(r'registrar-profiles', RegistrarProfileViewSet)
router.register(r'disabilities', DisabilityViewSet)
router.register(r'study-modes', StudyModeViewSet)
router.register(r'student-admissions', StudentAdmissionViewSet)
router.register(r'leave-of-absence', LeaveOfAbsenceViewSet)
router.register(r'transfer-requests', TransferRequestViewSet)
router.register(r'graduation-clearance', GraduationClearanceViewSet)
router.register(r'registrar-audit-logs', RegistrarAuditLogViewSet)

urlpatterns = [
    path('api/registrar/', include(router.urls)),
]
