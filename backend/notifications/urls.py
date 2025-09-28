from rest_framework.routers import DefaultRouter
from .views import (
    NotificationViewSet, NotificationPreferenceViewSet, NotificationGroupViewSet,
    NotificationAuditLogViewSet, NotificationAnalyticsViewSet, NotificationScheduleViewSet, NotificationActionResponseViewSet
)

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'notification-preferences', NotificationPreferenceViewSet, basename='notification-preference')
router.register(r'notification-groups', NotificationGroupViewSet, basename='notification-group')
router.register(r'notification-audit-logs', NotificationAuditLogViewSet, basename='notification-audit-log')
router.register(r'notification-analytics', NotificationAnalyticsViewSet, basename='notification-analytics')
router.register(r'notification-schedules', NotificationScheduleViewSet, basename='notification-schedule')
router.register(r'notification-action-responses', NotificationActionResponseViewSet, basename='notification-action-response')

urlpatterns = router.urls
