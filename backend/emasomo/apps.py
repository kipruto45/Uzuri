from django.apps import AppConfig


class EmasomoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emasomo'

    def ready(self):
        import emasomo.signals
