from rest_framework import serializers
from .models import GraduationEvent, GraduationApplication, GraduationClearance, GraduationCertificate

class GraduationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationEvent
        fields = '__all__'

class GraduationApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationApplication
        fields = '__all__'

class GraduationClearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationClearance
        fields = '__all__'

class GraduationCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationCertificate
        fields = '__all__'
