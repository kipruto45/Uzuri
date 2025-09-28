from rest_framework import serializers
from .models import LearningPathway, MicroCredential

class LearningPathwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPathway
        fields = '__all__'

class MicroCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroCredential
        fields = '__all__'
