from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, NotificationSchedule
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
# Example: Trigger notification send on schedule
@receiver(post_save, sender=NotificationSchedule)
def send_scheduled_notification(sender, instance, created, **kwargs):
    if created and instance.scheduled_for <= timezone.now():
        notif = instance.notification
        # Here, trigger Celery task to send notification (pseudo-code)
        # send_notification_task.delay(notif.id)
        notif.sent = True
        notif.sent_at = timezone.now()
        notif.save()


@receiver(post_save, sender=Notification)
def push_notification_ws(sender, instance, created, **kwargs):
    """When a Notification is created or updated, push it to the user's websocket group."""
    try:
        channel_layer = get_channel_layer()
        group = f"notifications_{instance.user_id}"
        payload = {
            "id": instance.id,
            "title": instance.title,
            "message": instance.message,
            "category": instance.category,
            "urgency": instance.urgency,
            "timestamp": instance.timestamp.isoformat(),
        }
        async_to_sync(channel_layer.group_send)(group, {
            "type": "send_notification",
            "content": payload,
        })
    except Exception:
        # best-effort: do not raise errors at signal time
        pass