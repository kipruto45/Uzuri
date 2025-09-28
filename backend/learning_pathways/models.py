from django.db import models
from django.conf import settings

class LearningPathway(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_pathways_created')
    created_at = models.DateTimeField(auto_now_add=True)

class MicroCredential(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='micro_credentials')
    pathway = models.ForeignKey(LearningPathway, on_delete=models.CASCADE, related_name='micro_credentials')
    awarded_at = models.DateTimeField(auto_now_add=True)
