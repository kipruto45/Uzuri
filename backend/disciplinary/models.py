from django.db import models
from django.conf import settings
from django.utils import timezone

class DisciplinaryCase(models.Model):
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('hearing', 'Hearing Scheduled'),
        ('resolved', 'Resolved'),
        ('appealed', 'Appealed'),
        ('closed', 'Closed'),
    ]
    student = models.ForeignKey('my_profile.StudentProfile', on_delete=models.CASCADE, related_name='disciplinary_cases', db_index=True)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_cases', db_index=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cases', db_index=True)
    case_type = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    confidential = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"Case #{self.id} - {self.student} ({self.status})"

class Evidence(models.Model):
    case = models.ForeignKey(DisciplinaryCase, on_delete=models.CASCADE, related_name='evidence')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='disciplinary/evidence/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Hearing(models.Model):
    case = models.ForeignKey(DisciplinaryCase, on_delete=models.CASCADE, related_name='hearings')
    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    panel = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='hearing_panel')
    notes = models.TextField(blank=True)
    outcome = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DisciplinaryAction(models.Model):
    case = models.ForeignKey(DisciplinaryCase, on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=64)
    description = models.TextField()
    decided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    decided_at = models.DateTimeField(auto_now_add=True)
    effective_from = models.DateTimeField(null=True, blank=True)
    effective_to = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Appeal(models.Model):
    case = models.ForeignKey(DisciplinaryCase, on_delete=models.CASCADE, related_name='appeals')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=32, choices=[('pending','Pending'),('accepted','Accepted'),('rejected','Rejected')], default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='appeal_reviews')

class AuditTrail(models.Model):
    case = models.ForeignKey(DisciplinaryCase, on_delete=models.CASCADE, related_name='audit_trail')
    action = models.CharField(max_length=255)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='disciplinary_audittrail')
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

class DisciplinaryNotification(models.Model):
    case = models.ForeignKey(DisciplinaryCase, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='disciplinary_notifications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=32, choices=[('email','Email'),('sms','SMS'),('in_app','In-App')], default='in_app')
    read = models.BooleanField(default=False)

# Analytics and dashboard logic can be implemented in views/services.
