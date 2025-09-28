from django.db import models
from django.conf import settings

class ProctoringSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proctoring_sessions')
    quiz = models.CharField(max_length=128)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    webcam_snapshot = models.ImageField(upload_to='proctoring/', null=True, blank=True)
    flagged = models.BooleanField(default=False)

class PlagiarismReport(models.Model):
    submission_id = models.CharField(max_length=128)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    report_url = models.URLField()
    checked_at = models.DateTimeField(auto_now_add=True)
