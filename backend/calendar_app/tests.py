from django.test import TestCase


class CalendarSmokeTests(TestCase):
    def test_model_aliases(self):
        """Ensure calendar_app.Event aliases the uzuri_calendar model."""
        from calendar_app.models import Event as EventAlias
        from uzuri_calendar.models import CalendarEvent

        # They should refer to the same class object
        self.assertIs(EventAlias, CalendarEvent)

    def test_urls_register_events(self):
        """Ensure the uzuri_calendar urls include registered 'events' routes."""
        from importlib import import_module

        urls = import_module('uzuri_calendar.urls')
        patterns = getattr(urls, 'urlpatterns', [])
        joined = ' '.join([str(p) for p in patterns])
        # The router registers viewset routes that include 'events'
        self.assertIn('events', joined)
