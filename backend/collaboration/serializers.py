from rest_framework import serializers
from .models import CollaborationSession, DocumentEdit, Whiteboard

class CollaborationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaborationSession
        fields = '__all__'

class DocumentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentEdit
        fields = '__all__'

class WhiteboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Whiteboard
        fields = '__all__'
