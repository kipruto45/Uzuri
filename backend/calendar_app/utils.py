import datetime
from django.utils import timezone
from .models import CalendarEvent

def check_event_conflicts(user, start, end, exclude_event_id=None):
    qs = CalendarEvent.objects.filter(
        shared_with=user,
        start_time__lt=end,
        end_time__gt=start
    )
    if exclude_event_id:
        qs = qs.exclude(id=exclude_event_id)
    return qs.exists()

def expand_recurring_events(event):
    # Example: expand weekly events for the next month
    rec = event.recurrence
    if not rec or rec.get('type') != 'weekly':
        return [event]
    occurrences = []
    start = event.start_time
    end = event.end_time
    days = rec.get('days', [])
    interval = rec.get('interval', 1)
    until = rec.get('end_date', (timezone.now() + datetime.timedelta(days=30)).date())
    current = start
    while current.date() <= until:
        if current.weekday() in days:
            occurrences.append((current, end + (current - start)))
        current += datetime.timedelta(days=1)
    return occurrences
