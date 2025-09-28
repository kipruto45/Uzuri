from rest_framework import serializers
from .models import BlockchainCredential

class BlockchainCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockchainCredential
        fields = '__all__'
