from rest_framework import serializers
from .models import AlumniMentor, MentorshipMatch

class AlumniMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniMentor
        fields = '__all__'

class MentorshipMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipMatch
        fields = '__all__'
