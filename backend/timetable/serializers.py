from rest_framework import serializers
from .models import Timetable, TimetableEntry, TimetableChangeRequest, TimetableAudit

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'

class TimetableEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableEntry
        fields = '__all__'

class TimetableChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableChangeRequest
        fields = '__all__'

class TimetableAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableAudit
        fields = '__all__'
