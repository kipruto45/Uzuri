from django.contrib import admin
from .models import (
	Notification, NotificationPreference, NotificationAuditLog, NotificationAnalytics, NotificationSchedule, NotificationGroup, NotificationActionResponse
)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = ("user", "title", "category", "urgency", "is_read", "timestamp", "sent")
	search_fields = ("user__email", "title", "message")
	list_filter = ("category", "urgency", "is_read", "sent")

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
	list_display = ("user", "channels", "categories", "language")
	search_fields = ("user__email",)

@admin.register(NotificationAuditLog)
class NotificationAuditLogAdmin(admin.ModelAdmin):
	list_display = ("notification", "channel", "status", "attempt", "timestamp")
	list_filter = ("channel", "status")

@admin.register(NotificationAnalytics)
class NotificationAnalyticsAdmin(admin.ModelAdmin):
	list_display = ("notification", "opened", "opened_at", "ignored", "ignored_at")

@admin.register(NotificationSchedule)
class NotificationScheduleAdmin(admin.ModelAdmin):
	list_display = ("notification", "scheduled_for", "sent", "sent_at")

@admin.register(NotificationGroup)
class NotificationGroupAdmin(admin.ModelAdmin):
	list_display = ("name", "description")
	filter_horizontal = ("users",)

@admin.register(NotificationActionResponse)
class NotificationActionResponseAdmin(admin.ModelAdmin):
	list_display = ("notification", "user", "response", "responded_at")
