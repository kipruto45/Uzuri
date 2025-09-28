from django.db import models
from django.conf import settings

class Report(models.Model):
    title = models.CharField(max_length=128)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_created')
    created_at = models.DateTimeField(auto_now_add=True)
    filters = models.JSONField(default=dict)
    export_format = models.CharField(max_length=16, default='pdf')
    scheduled = models.BooleanField(default=False)
    schedule_time = models.DateTimeField(null=True, blank=True)
