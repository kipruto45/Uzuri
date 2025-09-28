from rest_framework import viewsets, permissions
from .models import ComplianceRecord, AuditTrail
from .serializers import ComplianceRecordSerializer, AuditTrailSerializer

class ComplianceRecordViewSet(viewsets.ModelViewSet):
    queryset = ComplianceRecord.objects.all()
    serializer_class = ComplianceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuditTrailViewSet(viewsets.ModelViewSet):
    queryset = AuditTrail.objects.all()
    serializer_class = AuditTrailSerializer
    permission_classes = [permissions.IsAuthenticated]
