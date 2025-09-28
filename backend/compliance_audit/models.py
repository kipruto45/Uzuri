from django.db import models
from django.conf import settings

class ComplianceRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='compliance_records')
    regulation = models.CharField(max_length=128)
    status = models.CharField(max_length=32)
    checked_at = models.DateTimeField(auto_now_add=True)

class AuditTrail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='audit_trails')
    action = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
