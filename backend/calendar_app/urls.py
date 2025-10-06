from importlib import import_module


# Simple shim: import the project's uzuri_calendar.urls module and re-export its urlpatterns.
# This allows include('calendar_app.urls') to work while keeping the project's
# calendar implementation under the safe package name `uzuri_calendar`.
try:
    calendar_urls = import_module('uzuri_calendar.urls')
    urlpatterns = getattr(calendar_urls, 'urlpatterns', calendar_urls)
except Exception:  # pragma: no cover - defensive fallback
    # If anything goes wrong, provide an empty urlpatterns list so Django doesn't crash here.
    urlpatterns = []
