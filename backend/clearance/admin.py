
from django.contrib import admin
from .models import (
	ClearanceDepartment, ClearanceRequest, ClearanceApproval, ClearanceDocument,
	ClearanceWorkflowLog, ClearanceNotification, ClearanceComment, ClearanceDigitalSignature, ClearanceAuditTrail
)

@admin.register(ClearanceDepartment)
class ClearanceDepartmentAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active")
	search_fields = ("name",)
	list_filter = ("is_active",)

@admin.register(ClearanceRequest)
class ClearanceRequestAdmin(admin.ModelAdmin):
	list_display = ("student", "status", "submitted_at")
	search_fields = ("student__email",)
	list_filter = ("status",)

@admin.register(ClearanceApproval)
class ClearanceApprovalAdmin(admin.ModelAdmin):
	list_display = ("request", "department", "approved", "approved_by", "approved_at")
	search_fields = ("request__student__email", "department__name")
	list_filter = ("approved", "department")

@admin.register(ClearanceDocument)
class ClearanceDocumentAdmin(admin.ModelAdmin):
	list_display = ("request", "uploaded_by", "uploaded_at")
	search_fields = ("request__student__email",)


@admin.register(ClearanceWorkflowLog)
class ClearanceWorkflowLogAdmin(admin.ModelAdmin):
	list_display = ("request", "status", "actor", "timestamp")
	search_fields = ("request__student__email", "status", "actor__email")
	list_filter = ("status",)

@admin.register(ClearanceNotification)
class ClearanceNotificationAdmin(admin.ModelAdmin):
	list_display = ("request", "recipient", "channel", "sent_at", "is_read")
	search_fields = ("request__student__email", "recipient__email", "channel")
	list_filter = ("channel", "is_read")

@admin.register(ClearanceComment)
class ClearanceCommentAdmin(admin.ModelAdmin):
	list_display = ("approval", "user", "created_at")
	search_fields = ("approval__request__student__email", "user__email")
	list_filter = ("created_at",)

@admin.register(ClearanceDigitalSignature)
class ClearanceDigitalSignatureAdmin(admin.ModelAdmin):
	list_display = ("approval", "signed_by", "signed_at")
	search_fields = ("approval__request__student__email", "signed_by__email")
	list_filter = ("signed_at",)

@admin.register(ClearanceAuditTrail)
class ClearanceAuditTrailAdmin(admin.ModelAdmin):
	list_display = ("request", "action", "actor", "timestamp")
	search_fields = ("request__student__email", "action", "actor__email")
	list_filter = ("action",)
