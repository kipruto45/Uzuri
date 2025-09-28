from rest_framework import serializers
from .models import (
    ClearanceDepartment, ClearanceRequest, ClearanceApproval, ClearanceDocument,
    ClearanceWorkflowLog, ClearanceNotification, ClearanceComment, ClearanceDigitalSignature, ClearanceAuditTrail
)

class ClearanceDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceDepartment
        fields = '__all__'

class ClearanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceRequest
        fields = '__all__'

class ClearanceApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceApproval
        fields = '__all__'

class ClearanceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceDocument
        fields = '__all__'

class ClearanceWorkflowLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceWorkflowLog
        fields = '__all__'

class ClearanceNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceNotification
        fields = '__all__'

class ClearanceCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceComment
        fields = '__all__'

class ClearanceDigitalSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceDigitalSignature
        fields = '__all__'

class ClearanceAuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceAuditTrail
        fields = '__all__'
