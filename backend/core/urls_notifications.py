from django.urls import path
from .views_notifications import (
    NotificationListView,
    NotificationSendView,
    NotificationStatusView,
)

urlpatterns = [
    path('api/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('api/notifications/send/', NotificationSendView.as_view(), name='notification-send'),
    path('api/notifications/status/', NotificationStatusView.as_view(), name='notification-status'),
]
