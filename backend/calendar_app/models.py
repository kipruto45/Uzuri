"""Thin shim: re-export models from uzuri_calendar.models.

This avoids creating duplicate Django model classes under two app labels.
The real models live in `uzuri_calendar` and are registered in
`INSTALLED_APPS` as that app.
"""
from importlib import import_module

try:
    src = import_module('uzuri_calendar.models')
    globals().update({k: v for k, v in vars(src).items() if not k.startswith('_')})
except Exception:
    # If import fails, expose no symbols — Django checks will catch the
    # import error earlier during startup.
    pass

# Backwards-compatible alias expected by other modules
if 'CalendarEvent' in globals() and 'Event' not in globals():
    Event = globals()['CalendarEvent']

__all__ = [n for n in globals().keys() if not n.startswith('_')]
