from django.db import models
from django.conf import settings

class Incident(models.Model):
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incident_management_incidents_reported')
    description = models.TextField()
    status = models.CharField(max_length=32, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

class DisciplinaryAction(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='disciplinary_actions')
    action_taken = models.TextField()
    taken_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incident_management_disciplinary_actions')
    taken_at = models.DateTimeField(auto_now_add=True)
