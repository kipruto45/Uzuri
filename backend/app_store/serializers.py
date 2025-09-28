from rest_framework import serializers
from .models import AppStoreApp

class AppStoreAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppStoreApp
        fields = '__all__'
