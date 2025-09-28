from rest_framework import viewsets, permissions
from .models import MarketplaceItem, Purchase
from .serializers import MarketplaceItemSerializer, PurchaseSerializer
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

class MarketplaceItemViewSet(viewsets.ModelViewSet):
    queryset = MarketplaceItem.objects.all()
    serializer_class = MarketplaceItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]
