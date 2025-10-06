from rest_framework import serializers
from .models import Hostel, Room, HostelApplication, RoomAllocation

class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ['id', 'name', 'location', 'description']

class RoomSerializer(serializers.ModelSerializer):
    hostel = HostelSerializer(read_only=True)
    available = serializers.BooleanField(read_only=True)
    class Meta:
        model = Room
        fields = ['id', 'hostel', 'number', 'capacity', 'current_occupants', 'available', 'is_active']

class HostelApplicationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = HostelApplication
        fields = ['id', 'room', 'semester', 'status', 'decline_reason', 'created_at', 'updated_at']

class RoomAllocationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = RoomAllocation
        fields = ['id', 'room', 'semester', 'allocated_at']
