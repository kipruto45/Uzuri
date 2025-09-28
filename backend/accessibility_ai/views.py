from rest_framework import viewsets, permissions
from .models import AccessibilityFeature
from .serializers import AccessibilityFeatureSerializer

class AccessibilityFeatureViewSet(viewsets.ModelViewSet):
    queryset = AccessibilityFeature.objects.all()
    serializer_class = AccessibilityFeatureSerializer
    permission_classes = [permissions.IsAuthenticated]
