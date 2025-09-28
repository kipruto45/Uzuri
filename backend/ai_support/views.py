from rest_framework import viewsets, permissions
from .models import ChatbotConversation, StudyRecommendation, Alert
from .serializers import ChatbotConversationSerializer, StudyRecommendationSerializer, AlertSerializer

class ChatbotConversationViewSet(viewsets.ModelViewSet):
    queryset = ChatbotConversation.objects.all()
    serializer_class = ChatbotConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudyRecommendationViewSet(viewsets.ModelViewSet):
    queryset = StudyRecommendation.objects.all()
    serializer_class = StudyRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
