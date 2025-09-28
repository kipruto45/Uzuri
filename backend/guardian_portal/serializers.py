from rest_framework import serializers
from .models import Guardian, StudentGuardianLink

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = '__all__'

class StudentGuardianLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGuardianLink
        fields = '__all__'
