from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, NotificationSchedule
from django.utils import timezone
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