from django.db import models
from django.conf import settings

class CallSession(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='call_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_video = models.BooleanField(default=True)
