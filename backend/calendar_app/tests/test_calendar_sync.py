from django.test import TestCase
from calendar_app.sync import sync_calendar
from calendar_app.models import CalendarEvent

class CalendarSyncTest(TestCase):
    def test_sync_calendar(self):
        sync_calendar()
        self.assertTrue(CalendarEvent.objects.exists())
