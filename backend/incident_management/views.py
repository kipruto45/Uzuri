from rest_framework import viewsets, permissions
from .models import Incident, DisciplinaryAction
from .serializers import IncidentSerializer, DisciplinaryActionSerializer

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DisciplinaryActionViewSet(viewsets.ModelViewSet):
    queryset = DisciplinaryAction.objects.all()
    serializer_class = DisciplinaryActionSerializer
    permission_classes = [permissions.IsAuthenticated]
