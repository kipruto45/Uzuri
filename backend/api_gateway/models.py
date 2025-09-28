from django.db import models
from django.conf import settings

class APIToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='api_tokens')
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

class APIUsageLog(models.Model):
    token = models.ForeignKey(APIToken, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField()
    request_data = models.JSONField(default=dict)
