from rest_framework import serializers
from .models import CallSession

class CallSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallSession
        fields = '__all__'
