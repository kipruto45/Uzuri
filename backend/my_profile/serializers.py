
from rest_framework import serializers
from .models import StudentProfile, IDCardReplacementRequest, Notification, NotificationDeliveryLog, NotificationPreference, LoginActivity

class LoginActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginActivity
        fields = ['id', 'timestamp', 'ip_address', 'user_agent', 'session_key']

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['email', 'sms', 'in_app']

class NotificationDeliveryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationDeliveryLog
        fields = [
            'id', 'notification', 'attempt_time', 'status', 'channel', 'error_message', 'user_agent', 'ip_address'
        ]

class StudentProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'program', 'year_of_study', 'dob', 'gender', 'phone', 'address', 'emergency_contact',
            'profile_photo', 'id_card_downloaded', 'created_at', 'updated_at',
            'registration_date', 'last_login', 'account_status',
            'two_factor_enabled', 'two_factor_secret'
        ]
        read_only_fields = ['id', 'user', 'id_card_downloaded', 'created_at', 'updated_at', 'registration_date', 'last_login', 'two_factor_secret']

class IDCardReplacementRequestSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = IDCardReplacementRequest
        fields = ['id', 'student', 'reason', 'status', 'admin_comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'student', 'status', 'admin_comment', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'message', 'type', 'link', 'is_read', 'created_at', 'updated_at',
            'delivery_status', 'last_attempt', 'error_message'
        ]
