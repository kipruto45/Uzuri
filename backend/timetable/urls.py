from rest_framework.routers import DefaultRouter
from .views import (
    TimetableViewSet, TimetableEntryViewSet,
    TimetableChangeRequestViewSet, TimetableAuditViewSet
)

router = DefaultRouter()
router.register(r'timetables', TimetableViewSet)
router.register(r'entries', TimetableEntryViewSet)
router.register(r'change-requests', TimetableChangeRequestViewSet)
router.register(r'audits', TimetableAuditViewSet)

urlpatterns = router.urls
