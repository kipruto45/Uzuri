from django.contrib import admin
from .models import CalendarEvent, CalendarEventAuditLog

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_time", "end_time", "status", "created_by")
    list_filter = ("category", "status", "start_time", "end_time")
    search_fields = ("title", "description", "location")
    filter_horizontal = ("shared_with",)

@admin.register(CalendarEventAuditLog)
class CalendarEventAuditLogAdmin(admin.ModelAdmin):
    list_display = ("event", "action", "user", "timestamp")
    list_filter = ("action", "timestamp")
    search_fields = ("event__title", "user__username")
