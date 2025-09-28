from rest_framework import serializers
from .models import ChatbotConversation, StudyRecommendation, Alert

class ChatbotConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotConversation
        fields = '__all__'

class StudyRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyRecommendation
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
