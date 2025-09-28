from rest_framework import viewsets, permissions
from .models_registrar import *
from .serializers_registrar import *

class RegistrarProfileViewSet(viewsets.ModelViewSet):
    queryset = RegistrarProfile.objects.all()
    serializer_class = RegistrarProfileSerializer
    permission_classes = [permissions.IsAdminUser]

class DisabilityViewSet(viewsets.ModelViewSet):
    queryset = Disability.objects.all()
    serializer_class = DisabilitySerializer
    permission_classes = [permissions.IsAdminUser]

class StudyModeViewSet(viewsets.ModelViewSet):
    queryset = StudyMode.objects.all()
    serializer_class = StudyModeSerializer
    permission_classes = [permissions.IsAdminUser]

class StudentAdmissionViewSet(viewsets.ModelViewSet):
    queryset = StudentAdmission.objects.all()
    serializer_class = StudentAdmissionSerializer
    permission_classes = [permissions.IsAdminUser]

class LeaveOfAbsenceViewSet(viewsets.ModelViewSet):
    queryset = LeaveOfAbsence.objects.all()
    serializer_class = LeaveOfAbsenceSerializer
    permission_classes = [permissions.IsAdminUser]

class TransferRequestViewSet(viewsets.ModelViewSet):
    queryset = TransferRequest.objects.all()
    serializer_class = TransferRequestSerializer
    permission_classes = [permissions.IsAdminUser]

class GraduationClearanceViewSet(viewsets.ModelViewSet):
    queryset = GraduationClearance.objects.all()
    serializer_class = GraduationClearanceSerializer
    permission_classes = [permissions.IsAdminUser]

class RegistrarAuditLogViewSet(viewsets.ModelViewSet):
    queryset = RegistrarAuditLog.objects.all()
    serializer_class = RegistrarAuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
