from rest_framework import serializers
from .models import APIToken, APIUsageLog

class APITokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIToken
        fields = '__all__'

class APIUsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIUsageLog
        fields = '__all__'
