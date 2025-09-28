from rest_framework import serializers
from .models import IoTDevice, AttendanceRecord

class IoTDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTDevice
        fields = '__all__'

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'
