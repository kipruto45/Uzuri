from rest_framework import viewsets, permissions
from .models import PersonalizationProfile
from .serializers import PersonalizationProfileSerializer

class PersonalizationProfileViewSet(viewsets.ModelViewSet):
    queryset = PersonalizationProfile.objects.all()
    serializer_class = PersonalizationProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
