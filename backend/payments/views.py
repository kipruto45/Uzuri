from rest_framework import viewsets, permissions, filters, status
from django.db import models as dj_models
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from .models import (
    PaymentMethod, PaymentGateway, Payment, PaymentReceipt, PaymentAuditTrail, Refund,
    PaymentNotification, PaymentReversal, PaymentDispute, PaymentSchedule, PaymentIntegrationLog,
    PaymentComment, PaymentAttachment
)
from . import serializers
from notifications.models import Notification
from notifications.utils import get_unread_count, get_notification_types, get_delivery_status

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = serializers.PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class PaymentGatewayViewSet(viewsets.ModelViewSet):
    queryset = PaymentGateway.objects.all()
    serializer_class = serializers.PaymentGatewaySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class PaymentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["reference", "transaction_id", "user__email"]
    ordering_fields = ["created_at", "amount", "status"]

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request):
        user = request.user
        # Outstanding balance: sum of all pending payments
        outstanding = Payment.objects.filter(user=user, status="pending").aggregate(dj_models.Sum("amount"))["amount__sum"] or 0
        # Payment history: last 10 payments
        history = Payment.objects.filter(user=user).order_by("-created_at")[:10]
        # Next due payment: earliest pending payment
        next_due = Payment.objects.filter(user=user, status="pending").order_by("created_at").first()
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        unread_count = get_unread_count(user)
        notification_types = get_notification_types(user)
        delivery_status = get_delivery_status(user)
        return Response({
            "outstanding_balance": outstanding,
            "payment_history": serializers.PaymentSerializer(history, many=True).data,
            "next_due": serializers.PaymentSerializer(next_due).data if next_due else None,
            "notifications": notifications,
            "unread_notification_count": unread_count,
            "notification_types": notification_types,
            "notification_delivery_status": delivery_status,
        })

    @action(detail=False, methods=["get"], url_path="fee-statement")
    def fee_statement(self, request):
        user = request.user
        payments = Payment.objects.filter(user=user)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Fee Statement for {user.email}")
        y = 780
        for payment in payments:
            p.drawString(100, y, f"{payment.created_at.date()} - {payment.reference} - {payment.amount} {payment.currency} - {payment.status}")
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="fee_statement.pdf")

    def perform_create(self, serializer):
        payment = serializer.save()
        # Create notification for new payment
        PaymentNotification.objects.create(
            payment=payment,
            recipient=payment.user,
            message=f"Payment of {payment.amount} {payment.currency} received. Status: {payment.status}",
            channel="system"
        )

    @action(detail=False, methods=["post"], url_path="mpesa-stk-push/initiate")
    def mpesa_stk_push_initiate(self, request):
        """
        Initiate MPESA STK Push payment.
        Expects: phone_number, amount, reference
        """
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")
        reference = request.data.get("reference")
        if not all([phone_number, amount, reference]):
            return Response({"detail": "phone_number, amount, and reference are required."}, status=400)
        # Simulate MPESA STK push request (replace with real integration)
        # Log request
        from .models import PaymentIntegrationLog, Payment, PaymentMethod
        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found for reference."}, status=404)
        # Here, integrate with MPESA API (placeholder)
        # For demo, assume success and update payment
        payment.status = "processing"
        payment.save()
        PaymentIntegrationLog.objects.create(
            payment=payment,
            gateway=payment.gateway,
            request_payload={"phone_number": phone_number, "amount": amount, "reference": reference},
            response_payload={"message": "STK push initiated (simulated)"},
            status_code="200"
        )
        return Response({"detail": "MPESA STK push initiated.", "reference": reference}, status=200)

    @action(detail=False, methods=["post"], url_path="mpesa-stk-push/callback")
    def mpesa_stk_push_callback(self, request):
        """
        Handle MPESA STK Push callback.
        Expects: reference, status, transaction_id
        """
        reference = request.data.get("reference")
        status_val = request.data.get("status")
        transaction_id = request.data.get("transaction_id")
        if not all([reference, status_val, transaction_id]):
            return Response({"detail": "reference, status, and transaction_id are required."}, status=400)
        from .models import Payment
        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found for reference."}, status=404)
        payment.status = status_val
        payment.transaction_id = transaction_id
        payment.is_verified = status_val == "successful"
        payment.save()
        return Response({"detail": f"MPESA payment updated to {status_val}."}, status=200)

    @action(detail=False, methods=["post"], url_path="airtelmoney-stk-push/initiate")
    def airtelmoney_stk_push_initiate(self, request):
        """
        Initiate Airtel Money STK Push payment.
        Expects: phone_number, amount, reference
        """
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")
        reference = request.data.get("reference")
        if not all([phone_number, amount, reference]):
            return Response({"detail": "phone_number, amount, and reference are required."}, status=400)
        # Simulate Airtel Money STK push request (replace with real integration)
        from .models import PaymentIntegrationLog, Payment, PaymentMethod
        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found for reference."}, status=404)
        # Here, integrate with Airtel Money API (placeholder)
        payment.status = "processing"
        payment.save()
        PaymentIntegrationLog.objects.create(
            payment=payment,
            gateway=payment.gateway,
            request_payload={"phone_number": phone_number, "amount": amount, "reference": reference},
            response_payload={"message": "Airtel Money STK push initiated (simulated)"},
            status_code="200"
        )
        return Response({"detail": "Airtel Money STK push initiated.", "reference": reference}, status=200)

    @action(detail=False, methods=["post"], url_path="airtelmoney-stk-push/callback")
    def airtelmoney_stk_push_callback(self, request):
        """
        Handle Airtel Money STK Push callback.
        Expects: reference, status, transaction_id
        """
        reference = request.data.get("reference")
        status_val = request.data.get("status")
        transaction_id = request.data.get("transaction_id")
        if not all([reference, status_val, transaction_id]):
            return Response({"detail": "reference, status, and transaction_id are required."}, status=400)
        from .models import Payment
        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found for reference."}, status=404)
        payment.status = status_val
        payment.transaction_id = transaction_id
        payment.is_verified = status_val == "successful"
        payment.save()
        return Response({"detail": f"Airtel Money payment updated to {status_val}."}, status=200)

class PaymentReceiptViewSet(viewsets.ModelViewSet):
    queryset = PaymentReceipt.objects.all()
    serializer_class = serializers.PaymentReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentAuditTrailViewSet(viewsets.ModelViewSet):
    queryset = PaymentAuditTrail.objects.all()
    serializer_class = serializers.PaymentAuditTrailSerializer
    permission_classes = [permissions.IsAuthenticated]

class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = serializers.RefundSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentNotificationViewSet(viewsets.ModelViewSet):
    queryset = PaymentNotification.objects.all()
    serializer_class = serializers.PaymentNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentReversalViewSet(viewsets.ModelViewSet):
    queryset = PaymentReversal.objects.all()
    serializer_class = serializers.PaymentReversalSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentDisputeViewSet(viewsets.ModelViewSet):
    queryset = PaymentDispute.objects.all()
    serializer_class = serializers.PaymentDisputeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentScheduleViewSet(viewsets.ModelViewSet):
    queryset = PaymentSchedule.objects.all()
    serializer_class = serializers.PaymentScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentIntegrationLogViewSet(viewsets.ModelViewSet):
    queryset = PaymentIntegrationLog.objects.all()
    serializer_class = serializers.PaymentIntegrationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentCommentViewSet(viewsets.ModelViewSet):
    queryset = PaymentComment.objects.all()
    serializer_class = serializers.PaymentCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PaymentAttachment.objects.all()
    serializer_class = serializers.PaymentAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
from django.shortcuts import render

# Create your views here.

def get_notification_context(user):
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    unread_count = get_unread_count(user)
    notification_types = get_notification_types(user)
    delivery_status = get_delivery_status(user)
    return {
        "notifications": notifications,
        "unread_notification_count": unread_count,
        "notification_types": notification_types,
        "notification_delivery_status": delivery_status,
    }
