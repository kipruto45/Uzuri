from django.db import models
from django.conf import settings

class Workflow(models.Model):
    name = models.CharField(max_length=128)
    definition = models.JSONField(default=dict)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workflows_created')
    created_at = models.DateTimeField(auto_now_add=True)
