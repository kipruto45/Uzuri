from rest_framework import serializers
from .models import CalendarEvent, CalendarEventAuditLog

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'color')

class CalendarEventAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEventAuditLog
        fields = '__all__'
