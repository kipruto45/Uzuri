from django.db import models
from django.conf import settings

class AccessibilityFeature(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accessibility_features')
    feature_type = models.CharField(max_length=64)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
