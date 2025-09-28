
from django.db import models
from django.conf import settings
from django.utils import timezone

# ...existing code...

# Place NotificationDeliveryLog at the end

class NotificationDeliveryLog(models.Model):
    leave_request = models.ForeignKey('AcademicLeaveRequest', on_delete=models.CASCADE, related_name='notification_logs', db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    channel = models.CharField(max_length=32, db_index=True)  # email, sms, in_app
    status = models.CharField(max_length=32, db_index=True)  # delivered, failed
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    error_message = models.TextField(blank=True, null=True)

from django.db import models
from django.conf import settings
from django.utils import timezone

class AcademicLeaveRequest(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('approved', 'Approved'),
		('rejected', 'Rejected'),
		('cancelled', 'Cancelled'),
		('expired', 'Expired'),
		('completed', 'Completed'),
	]
	student = models.ForeignKey('my_profile.StudentProfile', on_delete=models.CASCADE, related_name='academic_leaves', db_index=True)
	leave_type = models.CharField(max_length=64, db_index=True)
	reason = models.TextField()
	start_date = models.DateField(db_index=True)
	end_date = models.DateField(db_index=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True, db_index=True)
	confidential = models.BooleanField(default=True)
	analytics_data = models.JSONField(default=dict, blank=True)

	def __str__(self):
		return f"Leave #{self.id} - {self.student} ({self.status})"

class AcademicLeaveApproval(models.Model):
	leave_request = models.ForeignKey(AcademicLeaveRequest, on_delete=models.CASCADE, related_name='approvals')
	approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	decision = models.CharField(max_length=16, choices=[('approved','Approved'),('rejected','Rejected')], default='approved')
	comment = models.TextField(blank=True)
	decided_at = models.DateTimeField(auto_now_add=True)

class AcademicLeaveDocument(models.Model):
	leave_request = models.ForeignKey(AcademicLeaveRequest, on_delete=models.CASCADE, related_name='documents')
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	file = models.FileField(upload_to='academic_leave/documents/')
	description = models.TextField(blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)

class AcademicLeaveAudit(models.Model):
	leave_request = models.ForeignKey(AcademicLeaveRequest, on_delete=models.CASCADE, related_name='audit_trail')
	action = models.CharField(max_length=255)
	performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_leave_audittrail')
	timestamp = models.DateTimeField(auto_now_add=True)
	details = models.JSONField(default=dict, blank=True)
