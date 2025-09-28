from django.db import models
from django.conf import settings

class CollaborationSession(models.Model):
    name = models.CharField(max_length=128)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collaboration_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentEdit(models.Model):
    session = models.ForeignKey(CollaborationSession, on_delete=models.CASCADE, related_name='edits')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='document_edits')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Whiteboard(models.Model):
    session = models.ForeignKey(CollaborationSession, on_delete=models.CASCADE, related_name='whiteboards')
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
