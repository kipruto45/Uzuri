from rest_framework import viewsets, permissions
from .models import APIToken, APIUsageLog
from .serializers import APITokenSerializer, APIUsageLogSerializer

class APITokenViewSet(viewsets.ModelViewSet):
    queryset = APIToken.objects.all()
    serializer_class = APITokenSerializer
    permission_classes = [permissions.IsAuthenticated]

class APIUsageLogViewSet(viewsets.ModelViewSet):
    queryset = APIUsageLog.objects.all()
    serializer_class = APIUsageLogSerializer
    permission_classes = [permissions.IsAuthenticated]
