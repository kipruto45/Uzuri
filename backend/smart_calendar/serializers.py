from rest_framework import serializers
from .models import SmartEvent

class SmartEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartEvent
        fields = '__all__'
