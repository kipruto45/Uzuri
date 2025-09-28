from django.db import models
from django.conf import settings

class PersonalizationProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personalization_profile')
    preferences = models.JSONField(default=dict)
    last_updated = models.DateTimeField(auto_now=True)
