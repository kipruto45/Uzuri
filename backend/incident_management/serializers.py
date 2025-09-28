from rest_framework import serializers
from .models import Incident, DisciplinaryAction

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'

class DisciplinaryActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryAction
        fields = '__all__'
