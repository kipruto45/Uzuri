from django.contrib import admin
from .models import ChatbotConversation, StudyRecommendation, Alert

admin.site.register(ChatbotConversation)
admin.site.register(StudyRecommendation)
admin.site.register(Alert)
