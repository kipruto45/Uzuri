from rest_framework import viewsets, permissions
from .models import Guardian, StudentGuardianLink
from .serializers import GuardianSerializer, StudentGuardianLinkSerializer

class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentGuardianLinkViewSet(viewsets.ModelViewSet):
    queryset = StudentGuardianLink.objects.all()
    serializer_class = StudentGuardianLinkSerializer
    permission_classes = [permissions.IsAuthenticated]
