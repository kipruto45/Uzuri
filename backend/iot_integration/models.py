from django.db import models
from django.conf import settings

class IoTDevice(models.Model):
    name = models.CharField(max_length=128)
    device_type = models.CharField(max_length=64)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='iot_devices')
    status = models.CharField(max_length=32, default='active')

class AttendanceRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE, related_name='attendance_records')
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=32)
