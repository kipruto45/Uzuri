from rest_framework import viewsets, permissions
from .models import ClearanceDepartment, ClearanceRequest, ClearanceApproval, ClearanceDocument
from .serializers import (
    ClearanceDepartmentSerializer,
    ClearanceRequestSerializer,
    ClearanceApprovalSerializer,
    ClearanceDocumentSerializer,
)
from .models import (
    ClearanceWorkflowLog, ClearanceNotification, ClearanceComment, ClearanceDigitalSignature, ClearanceAuditTrail
)
from .serializers import (
    ClearanceWorkflowLogSerializer, ClearanceNotificationSerializer, ClearanceCommentSerializer, ClearanceDigitalSignatureSerializer, ClearanceAuditTrailSerializer
)

class ClearanceDepartmentViewSet(viewsets.ModelViewSet):
    queryset = ClearanceDepartment.objects.all()
    serializer_class = ClearanceDepartmentSerializer
    permission_classes = [permissions.IsAdminUser]

class ClearanceWorkflowLogViewSet(viewsets.ModelViewSet):
    queryset = ClearanceWorkflowLog.objects.all()
    serializer_class = ClearanceWorkflowLogSerializer

class ClearanceNotificationViewSet(viewsets.ModelViewSet):
    queryset = ClearanceNotification.objects.all()
    serializer_class = ClearanceNotificationSerializer

class ClearanceCommentViewSet(viewsets.ModelViewSet):
    queryset = ClearanceComment.objects.all()
    serializer_class = ClearanceCommentSerializer

class ClearanceDigitalSignatureViewSet(viewsets.ModelViewSet):
    queryset = ClearanceDigitalSignature.objects.all()
    serializer_class = ClearanceDigitalSignatureSerializer

class ClearanceAuditTrailViewSet(viewsets.ModelViewSet):
    queryset = ClearanceAuditTrail.objects.all()
    serializer_class = ClearanceAuditTrailSerializer

class ClearanceRequestViewSet(viewsets.ModelViewSet):
    queryset = ClearanceRequest.objects.all()
    serializer_class = ClearanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClearanceApprovalViewSet(viewsets.ModelViewSet):
    queryset = ClearanceApproval.objects.all()
    serializer_class = ClearanceApprovalSerializer
    permission_classes = [permissions.IsAdminUser]

class ClearanceDocumentViewSet(viewsets.ModelViewSet):
    queryset = ClearanceDocument.objects.all()
    serializer_class = ClearanceDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
