from rest_framework import viewsets, permissions
from .models import SmartEvent
from .serializers import SmartEventSerializer

class SmartEventViewSet(viewsets.ModelViewSet):
    queryset = SmartEvent.objects.all()
    serializer_class = SmartEventSerializer
    permission_classes = [permissions.IsAuthenticated]
