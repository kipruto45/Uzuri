from django.core.cache import cache
from django.utils import timezone
from django.db.models import Q, Count

from rest_framework import viewsets, permissions, status, serializers
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Q, Count

from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import (
    Notification,
    NotificationPreference,
    NotificationAuditLog,
    NotificationAnalytics,
    NotificationSchedule,
    NotificationGroup,
    NotificationActionResponse,
    NotificationDeliveryLog,
    UserPreferences,
)
from .serializers import (
    NotificationSerializer,
    NotificationPreferenceSerializer,
    NotificationAuditLogSerializer,
    NotificationAnalyticsSerializer,
    NotificationScheduleSerializer,
    NotificationGroupSerializer,
    NotificationActionResponseSerializer,
)
from notifications.tasks import send_notification_task


class UserPreferencesViewSet(viewsets.ModelViewSet):
    queryset = UserPreferences.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="export-data")
    def export_data(self, request):
        user = request.user
        prefs = UserPreferences.objects.filter(user=user).first()
        notifications = Notification.objects.filter(user=user)
        data = {
            "preferences": NotificationPreferenceSerializer(prefs).data if prefs else {},
            "notifications": NotificationSerializer(notifications, many=True).data,
        }
        return Response(data)

    @action(detail=False, methods=["delete"], url_path="delete-data")
    def delete_data(self, request):
        user = request.user
        UserPreferences.objects.filter(user=user).delete()
        Notification.objects.filter(user=user).delete()
        return Response({"detail": "User data deleted."})

    def get_queryset(self):
        return UserPreferences.objects.filter(user=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f"notifications_{user.id}"
        qs = cache.get(cache_key)
        if qs is None:
            qs = Notification.objects.filter(user=user)
            category = self.request.query_params.get("category")
            unread = self.request.query_params.get("unread")
            if category:
                qs = qs.filter(category=category)
            if unread == "1":
                qs = qs.filter(is_read=False)
            cache.set(cache_key, qs, 60)  # Cache for 60 seconds
        return qs

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        # Analytics
        NotificationAnalytics.objects.create(notification=notification, opened=True, opened_at=timezone.now())
        return Response({"detail": "Notification marked as read."})

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        user = request.user
        count = Notification.objects.filter(user=user, is_read=False).count()
        return Response({"unread_count": count})

    @action(detail=False, methods=["post"])
    def bulk_send(self, request):
        # Admins only
        if not request.user.is_staff:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        users = request.data.get("users", [])
        title = request.data.get("title")
        message = request.data.get("message")
        category = request.data.get("category", "general")
        urgency = request.data.get("urgency", "info")
        channels = request.data.get("channels", ["in_app"])
        for user_id in users:
            Notification.objects.create(
                user_id=user_id,
                title=title,
                message=message,
                category=category,
                urgency=urgency,
                channels=channels,
                type="bulk",
                timestamp=timezone.now(),
            )
        return Response({"detail": "Bulk notifications sent."})

    @action(detail=False, methods=["post"])
    def schedule(self, request):
        # Schedule a notification for future delivery
        user = request.user
        title = request.data.get("title")
        message = request.data.get("message")
        category = request.data.get("category", "general")
        urgency = request.data.get("urgency", "info")
        channels = request.data.get("channels", ["in_app"])
        scheduled_for = request.data.get("scheduled_for")
        notif = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            category=category,
            urgency=urgency,
            channels=channels,
            type="scheduled",
            scheduled_for=scheduled_for,
        )
        NotificationSchedule.objects.create(notification=notif, scheduled_for=scheduled_for)
        return Response({"detail": "Notification scheduled."})

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def analytics(self, request):
        user = request.user
        opened = NotificationAnalytics.objects.filter(notification__user=user, opened=True).count()
        ignored = NotificationAnalytics.objects.filter(notification__user=user, ignored=True).count()
        total = Notification.objects.filter(user=user).count()
        return Response({"opened": opened, "ignored": ignored, "total": total})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_analytics(request):
    """A simple analytics endpoint registered explicitly so tests hit a DRF view
    where authentication/permission classes behave as expected for APIClient.
    """
    user = request.user
    opened = NotificationAnalytics.objects.filter(notification__user=user, opened=True).count()
    ignored = NotificationAnalytics.objects.filter(notification__user=user, ignored=True).count()
    total = Notification.objects.filter(user=user).count()
    return Response({"opened": opened, "ignored": ignored, "total": total})

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        notification = self.get_object()
        notification.acknowledged = True
        notification.save()
        NotificationActionResponse.objects.create(notification=notification, user=request.user, response="acknowledged")
        return Response({"detail": "Notification acknowledged."})


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)


class NotificationGroupViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]
    serializer_class = NotificationScheduleSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=["get"])
    def analytics(self, request):
        # ...existing code...
        return Response({})

    @action(detail=False, methods=["get"])
    def audit_logs(self, request):
        # ...existing code...
        return Response({})

    @action(detail=False, methods=["get"])
    def delivery_status(self, request):
        # ...existing code...
        return Response({})

    @action(detail=False, methods=["post"])
    def bulk_send(self, request):
        # ...existing code...
        return Response({})


class NotificationActionResponseViewSet(viewsets.ModelViewSet):
    queryset = NotificationActionResponse.objects.all()
    serializer_class = NotificationActionResponseSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationAuditLogViewSet(viewsets.ModelViewSet):
    queryset = NotificationAuditLog.objects.all()
    serializer_class = NotificationAuditLogSerializer
    permission_classes = [permissions.IsAdminUser]


class NotificationAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = NotificationAnalytics.objects.all()
    serializer_class = NotificationAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationScheduleViewSet(viewsets.ModelViewSet):
    queryset = NotificationSchedule.objects.all()
    serializer_class = NotificationScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationAdminViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        total = Notification.objects.count()
        delivered = NotificationAuditLog.objects.filter(status="success").count()
        failed = NotificationAuditLog.objects.filter(status="failed").count()
        by_channel = NotificationAuditLog.objects.values("channel").annotate(count=Count("id"))
        by_type = Notification.objects.values("category").annotate(count=Count("id"))
        webhook_events = NotificationAuditLog.objects.filter(channel="webhook").order_by("-timestamp")[:50]
        webhook_logs = [
            {
                "notification_id": log.notification_id,
                "status": log.status,
                "response": log.response,
                "timestamp": log.timestamp,
            }
            for log in webhook_events
        ]
        return Response({
            "total": total,
            "delivered": delivered,
            "failed": failed,
            "by_channel": list(by_channel),
            "by_type": list(by_type),
            "webhook_logs": webhook_logs,
        })

    @action(detail=False, methods=["post"])
    def bulk_action(self, request):
        action_name = request.data.get("action")
        ids = request.data.get("ids", [])
        if action_name == "archive":
            Notification.objects.filter(id__in=ids).update(sent=True)
        elif action_name == "delete":
            Notification.objects.filter(id__in=ids).delete()
        elif action_name == "send":
            for nid in ids:
                send_notification_task.delay(nid)
        return Response({"detail": f"Bulk {action_name} completed."})

    def get_queryset(self):
        return Notification.objects.all().select_related("user")

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if hasattr(serializer, "fields"):
            serializer.fields["push_token"] = serializers.CharField(source="push_token", read_only=True)
            serializer.fields["push_status"] = serializers.CharField(source="push_status", read_only=True)
        return serializer

    @action(detail=False, methods=["get"])
    def analytics(self, request):
        total = Notification.objects.count()
        unread = Notification.objects.filter(is_read=False).count()
        by_type = Notification.objects.values("category").annotate(count=Count("id"))
        delivery_status = NotificationDeliveryLog.objects.values("status").annotate(count=Count("id"))
        return Response({"total": total, "unread": unread, "by_type": list(by_type), "delivery_status": list(delivery_status)})

    @action(detail=False, methods=["get"])
    def audit_logs(self, request):
        logs = NotificationAuditLog.objects.all().order_by("-created_at")[:100]
        serializer = NotificationAuditLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def delivery_status(self, request):
        status_list = NotificationDeliveryLog.objects.values("status").annotate(count=Count("id"))
        return Response(list(status_list))

    @action(detail=False, methods=["post"])
    def bulk_send(self, request):
        users = request.data.get("users", [])
        title = request.data.get("title")
        message = request.data.get("message")
        category = request.data.get("category", "general")
        urgency = request.data.get("urgency", "info")
        channels = request.data.get("channels", ["in_app"])
        for user_id in users:
            Notification.objects.create(
                user_id=user_id,
                title=title,
                message=message,
                category=category,
                urgency=urgency,
                channels=channels,
            )
        return Response({"detail": "Bulk notifications sent."})
