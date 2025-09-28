from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
from notifications.models import Notification
from notifications.utils import get_unread_count, get_notification_types, get_delivery_status

def get_notification_context(user):
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    unread_count = get_unread_count(user)
    notification_types = get_notification_types(user)
    delivery_status = get_delivery_status(user)
    return {
        "notifications": notifications,
        "unread_notification_count": unread_count,
        "notification_types": notification_types,
        "notification_delivery_status": delivery_status,
    }

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data.update(get_notification_context(request.user))
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = {"results": serializer.data}
            data.update(get_notification_context(request.user))
            return self.get_paginated_response(data)
        serializer = self.get_serializer(queryset, many=True)
        data = {"results": serializer.data}
        data.update(get_notification_context(request.user))
        return Response(data)
