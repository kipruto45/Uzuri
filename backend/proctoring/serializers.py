from rest_framework import serializers
from .models import ProctoringSession, PlagiarismReport

class ProctoringSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProctoringSession
        fields = '__all__'

class PlagiarismReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlagiarismReport
        fields = '__all__'
