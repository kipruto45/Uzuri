from rest_framework import serializers
from .models import ComplianceRecord, AuditTrail

class ComplianceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceRecord
        fields = '__all__'

class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'
