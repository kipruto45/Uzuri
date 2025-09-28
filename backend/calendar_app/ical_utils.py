from icalendar import Calendar, Event
from django.utils import timezone

def generate_ical_feed(events, user):
    cal = Calendar()
    cal.add('prodid', '-//Uzuri University//Calendar//EN')
    cal.add('version', '2.0')
    for e in events:
        ical_event = Event()
        ical_event.add('summary', e.title)
        ical_event.add('dtstart', e.start_time)
        ical_event.add('dtend', e.end_time)
        ical_event.add('description', e.description)
        ical_event.add('location', e.location)
        ical_event.add('status', e.status.upper())
        ical_event.add('uid', f"uzuri-{e.id}@uzuriuniversity.com")
        ical_event.add('created', e.created_at)
        ical_event.add('last-modified', e.updated_at)
        ical_event.add('categories', e.category)
        cal.add_component(ical_event)
    return cal.to_ical()
