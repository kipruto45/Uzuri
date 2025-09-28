from rest_framework import serializers
from .models import Invoice, Transaction, Receipt, FeeStructure, Scholarship, AuditTrail
class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'issued_date']


class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
