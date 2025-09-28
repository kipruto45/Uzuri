from rest_framework import serializers
from .models import AccessibilityFeature

class AccessibilityFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessibilityFeature
        fields = '__all__'
