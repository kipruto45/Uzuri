from celery import shared_task
from django.utils import timezone
from .models import CalendarEvent
from notifications.models import Notification
from django.contrib.auth import get_user_model

@shared_task
def send_event_reminder(event_id, user_id, reminder_time):
    User = get_user_model()
    try:
        event = CalendarEvent.objects.get(id=event_id)
        user = User.objects.get(id=user_id)
        Notification.objects.create(
            user=user,
            category=event.category,
            type='reminder',
            title=f"Reminder: {event.title}",
            message=f"You have an upcoming event: {event.title} at {event.start_time:%Y-%m-%d %H:%M}",
            urgency='info',
            channels=["in_app", "email"],
            personalized_context={"event_id": event.id},
            scheduled_for=reminder_time,
        )
    except (CalendarEvent.DoesNotExist, User.DoesNotExist):
        pass
