from rest_framework import serializers
from .models import PersonalizationProfile

class PersonalizationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalizationProfile
        fields = '__all__'
