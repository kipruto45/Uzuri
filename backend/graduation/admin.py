
from django.contrib import admin
from .models import GraduationEvent, GraduationApplication, GraduationClearance, GraduationCertificate

@admin.register(GraduationEvent)
class GraduationEventAdmin(admin.ModelAdmin):
	list_display = ("name", "date", "location", "is_active")
	search_fields = ("name", "location")
	list_filter = ("is_active", "date")

@admin.register(GraduationApplication)
class GraduationApplicationAdmin(admin.ModelAdmin):
	list_display = ("student", "event", "status", "is_eligible", "is_cleared", "submitted_at")
	search_fields = ("student__username", "event__name")
	list_filter = ("status", "is_eligible", "is_cleared", "event")

@admin.register(GraduationClearance)
class GraduationClearanceAdmin(admin.ModelAdmin):
	list_display = ("application", "department", "is_cleared", "cleared_by", "cleared_at")
	search_fields = ("application__student__username", "department")
	list_filter = ("is_cleared", "department")

@admin.register(GraduationCertificate)
class GraduationCertificateAdmin(admin.ModelAdmin):
	list_display = ("application", "serial_number", "issued_at", "issued_by")
	search_fields = ("application__student__username", "serial_number")
