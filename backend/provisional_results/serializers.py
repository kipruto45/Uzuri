from rest_framework import serializers
from .models import Result, GradingScale, Recommendation

class GradingScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingScale
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'
