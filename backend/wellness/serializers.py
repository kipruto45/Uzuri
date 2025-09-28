from rest_framework import serializers
from .models import WellnessResource, CounselingAppointment

class WellnessResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessResource
        fields = '__all__'

class CounselingAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselingAppointment
        fields = '__all__'
