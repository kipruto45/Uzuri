from rest_framework import viewsets, permissions
from .models import BlockchainCredential
from .serializers import BlockchainCredentialSerializer

class BlockchainCredentialViewSet(viewsets.ModelViewSet):
    queryset = BlockchainCredential.objects.all()
    serializer_class = BlockchainCredentialSerializer
    permission_classes = [permissions.IsAuthenticated]
