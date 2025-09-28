from django.db import models
from .models import Notification

def get_unread_count(user):
    return Notification.objects.filter(user=user, is_read=False).count()

def get_notification_types(user):
    return Notification.objects.filter(user=user).values_list('type', flat=True).distinct()

def get_delivery_status(user):
    return Notification.objects.filter(user=user).values('delivery_status').annotate(count=models.Count('id'))
