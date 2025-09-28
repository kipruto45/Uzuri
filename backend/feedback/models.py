from django.db import models
from django.conf import settings

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_entries')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Survey(models.Model):
    title = models.CharField(max_length=128)
    questions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey_responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_responses')
    answers = models.JSONField(default=dict)
    submitted_at = models.DateTimeField(auto_now_add=True)
