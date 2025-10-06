from rest_framework import serializers
from .models import EvaluationForm, EvaluationResponse, EvaluationSummary

class EvaluationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationForm
        fields = '__all__'

class EvaluationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationResponse
        fields = '__all__'

class EvaluationSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationSummary
        fields = '__all__'
