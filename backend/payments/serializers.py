from rest_framework import serializers
from .models import (
    PaymentMethod, PaymentGateway, Payment, PaymentReceipt, PaymentAuditTrail, Refund,
    PaymentNotification, PaymentReversal, PaymentDispute, PaymentSchedule, PaymentIntegrationLog,
    PaymentComment, PaymentAttachment
)

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReceipt
        fields = '__all__'

class PaymentAuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAuditTrail
        fields = '__all__'

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

class PaymentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentNotification
        fields = '__all__'

class PaymentReversalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReversal
        fields = '__all__'

class PaymentDisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDispute
        fields = '__all__'

class PaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSchedule
        fields = '__all__'

class PaymentIntegrationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntegrationLog
        fields = '__all__'

class PaymentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentComment
        fields = '__all__'

class PaymentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAttachment
        fields = '__all__'
