from rest_framework import serializers
from .models import UnitRegistration, UnitRegistrationItem
from core.models import Unit

class UnitRegistrationItemSerializer(serializers.ModelSerializer):
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    class Meta:
        model = UnitRegistrationItem
        fields = ['id', 'unit', 'selected']

class UnitRegistrationSerializer(serializers.ModelSerializer):
    items = UnitRegistrationItemSerializer(many=True)
    class Meta:
        model = UnitRegistration
        fields = ['id', 'student', 'semester', 'status', 'items', 'created_at', 'updated_at', 'approved_by', 'approved_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        registration = UnitRegistration.objects.create(**validated_data)
        for item_data in items_data:
            UnitRegistrationItem.objects.create(registration=registration, **item_data)
        return registration
