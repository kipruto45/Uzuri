from rest_framework.routers import DefaultRouter
from .views import (
    NotificationViewSet, NotificationPreferenceViewSet, NotificationGroupViewSet,
    NotificationAuditLogViewSet, NotificationAnalyticsViewSet, NotificationScheduleViewSet, NotificationActionResponseViewSet
)

from django.urls import path
from .views import public_analytics

# Explicit route for analytics on notifications must come before the router URLs so that
# the path '/api/notifications/analytics/' is not captured by the router's detail regex.
extra_urls = [
    path('analytics/', public_analytics, name='notification-analytics-endpoint'),
]

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'notification-preferences', NotificationPreferenceViewSet, basename='notification-preference')
router.register(r'notification-groups', NotificationGroupViewSet, basename='notification-group')
router.register(r'notification-audit-logs', NotificationAuditLogViewSet, basename='notification-audit-log')
router.register(r'notification-analytics', NotificationAnalyticsViewSet, basename='notification-analytics')
router.register(r'notification-schedules', NotificationScheduleViewSet, basename='notification-schedule')
router.register(r'notification-action-responses', NotificationActionResponseViewSet, basename='notification-action-response')

# Prepend extra_urls so they take precedence over router-generated patterns that could
# mistakenly interpret the segment 'analytics' as a detail lookup (pk).
urlpatterns = extra_urls + router.urls

