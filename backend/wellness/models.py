from django.db import models
from django.conf import settings

class WellnessResource(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CounselingAppointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='counseling_appointments')
    scheduled_for = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='pending')
