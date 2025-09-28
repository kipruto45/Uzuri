from rest_framework import serializers
from .models import FinanceCategory, FinanceRegistration, FinanceRegistrationItem, FinanceInvoice

class FinanceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceCategory
        fields = '__all__'

class FinanceRegistrationItemSerializer(serializers.ModelSerializer):
    category = FinanceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=FinanceCategory.objects.all(), source='category', write_only=True)
    class Meta:
        model = FinanceRegistrationItem
        fields = ['id', 'category', 'category_id', 'amount', 'selected']

class FinanceRegistrationSerializer(serializers.ModelSerializer):
    items = FinanceRegistrationItemSerializer(many=True)
    class Meta:
        model = FinanceRegistration
        fields = ['id', 'student', 'semester', 'status', 'items', 'created_at', 'updated_at', 'approved_by', 'approved_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        registration = FinanceRegistration.objects.create(**validated_data)
        for item_data in items_data:
            FinanceRegistrationItem.objects.create(registration=registration, **item_data)
        return registration

class FinanceInvoiceSerializer(serializers.ModelSerializer):
    registration = FinanceRegistrationSerializer(read_only=True)
    class Meta:
        model = FinanceInvoice
        fields = ['id', 'registration', 'total_amount', 'paid_amount', 'status', 'due_date', 'updated_at']
