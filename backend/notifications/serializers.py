from rest_framework import serializers
from .models import (
    Notification, NotificationPreference, NotificationAuditLog, NotificationAnalytics, NotificationSchedule, NotificationGroup, NotificationActionResponse
)

class NotificationSerializer(serializers.ModelSerializer):
    push_token = serializers.CharField(read_only=True)
    push_status = serializers.CharField(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = '__all__'

class NotificationAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationAuditLog
        fields = '__all__'

class NotificationAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationAnalytics
        fields = '__all__'

class NotificationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSchedule
        fields = '__all__'

class NotificationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationGroup
        fields = '__all__'

class NotificationActionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationActionResponse
        fields = '__all__'
