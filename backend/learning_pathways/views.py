from rest_framework import viewsets, permissions
from .models import LearningPathway, MicroCredential
from .serializers import LearningPathwaySerializer, MicroCredentialSerializer

class LearningPathwayViewSet(viewsets.ModelViewSet):
    queryset = LearningPathway.objects.all()
    serializer_class = LearningPathwaySerializer
    permission_classes = [permissions.IsAuthenticated]

class MicroCredentialViewSet(viewsets.ModelViewSet):
    queryset = MicroCredential.objects.all()
    serializer_class = MicroCredentialSerializer
    permission_classes = [permissions.IsAuthenticated]
