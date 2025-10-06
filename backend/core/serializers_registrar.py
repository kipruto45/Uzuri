from rest_framework import serializers
from .models_registrar import *

class RegistrarProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrarProfile
        fields = ['user', 'role']

class DisabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Disability
        fields = ['student', 'category', 'support_needs', 'tagged_for_reporting']

class StudyModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMode
        fields = ['name']

class StudentAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = ['student', 'intake_year', 'program', 'campus', 'department', 'kcse_certificate', 'result_slip', 'id_passport', 'admission_letter', 'study_mode', 'disability']

class LeaveOfAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveOfAbsence
        fields = ['student', 'reason', 'status', 'requested_at', 'approved_at', 'approved_by']

class TransferRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferRequest
        fields = ['student', 'from_program', 'to_program', 'status', 'requested_at', 'approved_at', 'approved_by']

class GraduationClearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationClearance
        fields = ['student', 'status', 'checked_at', 'checked_by']

class RegistrarAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrarAuditLog
        fields = ['user', 'action', 'timestamp', 'details', 'encrypted']
