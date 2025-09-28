
from django.contrib import admin
from .models import AcademicLeaveRequest, AcademicLeaveApproval, AcademicLeaveDocument, AcademicLeaveAudit, NotificationDeliveryLog
@admin.register(NotificationDeliveryLog)
class NotificationDeliveryLogAdmin(admin.ModelAdmin):
	list_display = ('id', 'leave_request', 'user', 'channel', 'status', 'timestamp')
	list_filter = ('channel', 'status', 'timestamp')
	search_fields = ('leave_request__id', 'user__username', 'message', 'error_message')
	readonly_fields = ('timestamp',)

@admin.register(AcademicLeaveRequest)
class AcademicLeaveRequestAdmin(admin.ModelAdmin):
	list_display = ('id', 'student', 'leave_type', 'status', 'start_date', 'end_date', 'is_active')
	list_filter = ('status', 'is_active', 'leave_type', 'start_date', 'end_date')
	search_fields = ('student__user__username', 'leave_type', 'reason')
	readonly_fields = ('created_at', 'updated_at')

	actions = ['bulk_approve', 'bulk_reject']

	def bulk_approve(self, request, queryset):
		updated = queryset.update(status='approved')
		self.message_user(request, f"{updated} requests marked as approved.")
	bulk_approve.short_description = "Approve selected leave requests"

	def bulk_reject(self, request, queryset):
		updated = queryset.update(status='rejected')
		self.message_user(request, f"{updated} requests marked as rejected.")
	bulk_reject.short_description = "Reject selected leave requests"

@admin.register(AcademicLeaveApproval)
class AcademicLeaveApprovalAdmin(admin.ModelAdmin):
	list_display = ('id', 'leave_request', 'approver', 'decision', 'decided_at')
	list_filter = ('decision', 'decided_at')
	search_fields = ('leave_request__id', 'approver__username', 'comment')
	readonly_fields = ('decided_at',)

@admin.register(AcademicLeaveDocument)
class AcademicLeaveDocumentAdmin(admin.ModelAdmin):
	list_display = ('id', 'leave_request', 'uploaded_by', 'uploaded_at')
	search_fields = ('leave_request__id', 'uploaded_by__username', 'description')
	readonly_fields = ('uploaded_at',)

@admin.register(AcademicLeaveAudit)
class AcademicLeaveAuditAdmin(admin.ModelAdmin):
	list_display = ('id', 'leave_request', 'action', 'performed_by', 'timestamp')
	list_filter = ('action', 'timestamp')
	search_fields = ('leave_request__id', 'performed_by__username', 'action')
	readonly_fields = ('timestamp',)
