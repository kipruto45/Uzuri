from rest_framework import serializers
from .models import AcademicLeaveRequest, AcademicLeaveApproval, AcademicLeaveDocument, AcademicLeaveAudit

class AcademicLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicLeaveRequest
        fields = '__all__'

class AcademicLeaveApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicLeaveApproval
        fields = '__all__'

class AcademicLeaveDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicLeaveDocument
        fields = '__all__'

class AcademicLeaveAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicLeaveAudit
        fields = '__all__'
