from rest_framework.routers import DefaultRouter
from .views import ComplianceRecordViewSet, AuditTrailViewSet

router = DefaultRouter()
router.register(r'compliance-records', ComplianceRecordViewSet)
router.register(r'audit-trails', AuditTrailViewSet)

urlpatterns = router.urls
