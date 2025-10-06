from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    DisciplinaryCase, Evidence, Hearing,
    DisciplinaryAction, Appeal, AuditTrail,
    DisciplinaryNotification,
)

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class StudentProfileRefSerializer(serializers.Serializer):
    # minimal representation to avoid importing whole profile serializer
    id = serializers.IntegerField(read_only=True)
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        # obj may be a StudentProfile instance or a dict
        try:
            return obj.user.email
        except Exception:
            return None


class DisciplinaryCaseSerializer(serializers.ModelSerializer):
    student = StudentProfileRefSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = DisciplinaryCase
        fields = ('id', 'student', 'student_id', 'reported_by', 'assigned_to', 'case_type', 'description', 'status', 'confidential', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        student_id = validated_data.pop('student_id', None)
        if student_id:
            # lazy import to avoid circulars
            from my_profile.models import StudentProfile
            validated_data['student'] = StudentProfile.objects.get(id=student_id)
        return super().create(validated_data)


class EvidenceSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    case = serializers.PrimaryKeyRelatedField(read_only=True)
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Evidence
        fields = ('id', 'case', 'uploaded_by', 'file', 'description', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_by', 'uploaded_at')

    def validate_file(self, value):
        # basic validation: max 10MB
        max_mb = 10
        if value.size > max_mb * 1024 * 1024:
            raise serializers.ValidationError(f'File too large. Max size is {max_mb}MB.')
        return value


class HearingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hearing
        fields = '__all__'


class DisciplinaryActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryAction
        fields = '__all__'


class AppealSerializer(serializers.ModelSerializer):
    # case and submitted_by are supplied by the view, not by client payload
    case = serializers.PrimaryKeyRelatedField(read_only=True)
    submitted_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Appeal
        fields = ('id', 'case', 'submitted_by', 'reason', 'status', 'submitted_at', 'reviewed_at', 'reviewed_by')
        read_only_fields = ('id', 'case', 'submitted_by', 'status', 'submitted_at', 'reviewed_at', 'reviewed_by')


class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryNotification
        fields = '__all__'
