from rest_framework import viewsets, permissions
from .models import AppStoreApp
from .serializers import AppStoreAppSerializer

class AppStoreAppViewSet(viewsets.ModelViewSet):
    queryset = AppStoreApp.objects.all()
    serializer_class = AppStoreAppSerializer
    permission_classes = [permissions.IsAuthenticated]
