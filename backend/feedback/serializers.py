from rest_framework import serializers
from .models import Feedback, Survey, SurveyResponse

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'
