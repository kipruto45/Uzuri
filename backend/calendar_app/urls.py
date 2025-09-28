from rest_framework.routers import DefaultRouter
from .views import CalendarEventViewSet, CalendarEventAuditLogViewSet

router = DefaultRouter()
router.register(r'events', CalendarEventViewSet, basename='calendar-event')
router.register(r'audit-logs', CalendarEventAuditLogViewSet, basename='calendar-event-audit-log')

urlpatterns = router.urls
