from django.contrib import admin
from .models import IoTDevice, AttendanceRecord

admin.site.register(IoTDevice)
admin.site.register(AttendanceRecord)
