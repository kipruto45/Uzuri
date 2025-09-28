from rest_framework import serializers
from .models import MarketplaceItem, Purchase

class MarketplaceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceItem
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
