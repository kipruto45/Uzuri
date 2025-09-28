from django.apps import AppConfig

class CalendarAppConfig(AppConfig):
    name = 'calendar_app'

    def ready(self):
        import calendar_app.signals
