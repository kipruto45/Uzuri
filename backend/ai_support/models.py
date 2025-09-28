from django.db import models
from django.conf import settings

class ChatbotConversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_support_chatbot_conversations')
    message = models.TextField()
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class StudyRecommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_support_study_recommendations')
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Alert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_support_alerts')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
