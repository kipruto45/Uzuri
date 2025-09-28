from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CalendarEvent
from .tasks import send_event_reminder
from django.utils import timezone

@receiver(post_save, sender=CalendarEvent)
def schedule_event_reminders(sender, instance, created, **kwargs):
    if created and instance.notification_settings:
        for interval in instance.notification_settings:
            # interval expected as string, e.g., '24h', '1h', '10m'
            if interval.endswith('h'):
                delta = timezone.timedelta(hours=int(interval[:-1]))
            elif interval.endswith('m'):
                delta = timezone.timedelta(minutes=int(interval[:-1]))
            elif interval.endswith('d'):
                delta = timezone.timedelta(days=int(interval[:-1]))
            else:
                continue
            reminder_time = instance.start_time - delta
            if reminder_time > timezone.now():
                send_event_reminder.apply_async((instance.id, instance.created_by.id, str(reminder_time)), eta=reminder_time)
                for user in instance.shared_with.all():
                    send_event_reminder.apply_async((instance.id, user.id, str(reminder_time)), eta=reminder_time)
