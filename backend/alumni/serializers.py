from rest_framework import serializers
from .models import AlumniProfile, JobPosting

class AlumniProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniProfile
        fields = '__all__'

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'
