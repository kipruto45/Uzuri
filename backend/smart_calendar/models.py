from django.db import models
from django.conf import settings

class SmartEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='smart_events')
    title = models.CharField(max_length=128)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ai_suggestion = models.TextField(blank=True)
    conflict = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
