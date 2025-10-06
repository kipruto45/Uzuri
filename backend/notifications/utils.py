from django.db import models
from django.db.models import F
from .models import Notification, NotificationDeliveryLog

def get_unread_count(user):
    return Notification.objects.filter(user=user, is_read=False).count()

def get_notification_types(user):
    return Notification.objects.filter(user=user).values_list('type', flat=True).distinct()

def get_delivery_status(user):
    # Aggregate by delivery log status (delivery_logs.status) because the
    # Notification model does not always keep a single delivery_status field
    # per channel. This returns a list of {'status': <status>, 'count': N}.
    # Use values('status') directly to avoid creating an annotation
    # that conflicts with existing model fields named 'status'.
    return (
        NotificationDeliveryLog.objects.filter(notification__user=user)
        .values('status')
        .annotate(count=models.Count('id'))
        .order_by('-count')
    )
