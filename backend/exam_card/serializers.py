from rest_framework import serializers
from .models import ExamCard

class ExamCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCard
        fields = '__all__'
