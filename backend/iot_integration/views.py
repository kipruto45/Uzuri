from rest_framework import viewsets, permissions
from .models import IoTDevice, AttendanceRecord
from .serializers import IoTDeviceSerializer, AttendanceRecordSerializer

class IoTDeviceViewSet(viewsets.ModelViewSet):
    queryset = IoTDevice.objects.all()
    serializer_class = IoTDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
