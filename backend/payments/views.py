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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import uuid
import os
import json
import base64
import requests
from django.conf import settings
from django.utils import timezone

try:
    import stripe
except Exception:
    stripe = None

def _mpesa_get_token(mpesa_env, key, secret, timeout=10):
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials' if mpesa_env == 'sandbox' else 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(auth_url, auth=(key, secret), timeout=timeout)
    if r is not None and r.status_code == 200:
        return r.json().get('access_token')
    return None

def _mpesa_stk_push(mpesa_env, shortcode, passkey, amount, phone, reference, callback_url, token, timeout=10):
    from datetime import datetime
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()
    stk_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest' if mpesa_env == 'sandbox' else 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    payload = {
        'BusinessShortCode': shortcode,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': str(amount),
        'PartyA': phone,
        'PartyB': shortcode,
        'PhoneNumber': phone,
        'CallBackURL': callback_url,
        'AccountReference': reference,
        'TransactionDesc': f'Uzuri payment: {reference}'
    }
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'} if token else {'Content-Type': 'application/json'}
    r = requests.post(stk_url, json=payload, headers=headers, timeout=timeout)
    return r, payload

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

from core.permissions import HasRole


class PaymentViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    # default permissions; sensitive actions further guarded by HasRole
    permission_classes = [permissions.IsAuthenticated]
    required_roles = ['Finance Staff', 'System Administrator']
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stripe_initiate(request):
    """Create a Payment and return a simulated Stripe session id.
    Expects: amount, currency (optional), description (optional)
    """
    amount = request.data.get('amount')
    currency = request.data.get('currency', 'KES')
    description = request.data.get('description', '')
    if not amount:
        return Response({'detail': 'amount is required'}, status=status.HTTP_400_BAD_REQUEST)
    # create a payment record
    reference = str(uuid.uuid4())
    payment = Payment.objects.create(
        user=request.user,
        amount=amount,
        currency=currency,
        status='pending',
        reference=reference,
        description=description,
    )
    # In production, create a Stripe Checkout Session and return its url
    session_url = None
    try:
        if stripe and getattr(settings, 'STRIPE_SECRET_KEY', ''):
            stripe.api_key = settings.STRIPE_SECRET_KEY
            # build success/cancel URLs (frontend should handle these routes)
            success = request.build_absolute_uri('/payments/success/')
            cancel = request.build_absolute_uri('/payments/cancel/')
            # Stripe expects amount in cents for many currencies, but for KES we keep as is depending on account config.
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': currency.lower(),
                        'product_data': {'name': description or 'Uzuri Payment'},
                        'unit_amount': int(float(amount) * 100),
                    },
                    'quantity': 1,
                }],
                success_url=success + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel,
                client_reference_id=reference,
            )
            session_url = session.url
    except Exception:
        session_url = None

    if session_url:
        return Response({'reference': reference, 'session_url': session_url}, status=200)

    # fallback simulated
    session_id = f"simulated_stripe_session_{reference}"
    return Response({'reference': reference, 'session_id': session_id}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mpesa_initiate(request):
    """Create a Payment and simulate MPESA STK push initiation.
    Expects: amount, phone
    """
    amount = request.data.get('amount')
    phone = request.data.get('phone')
    if not amount or not phone:
        return Response({'detail': 'amount and phone are required'}, status=status.HTTP_400_BAD_REQUEST)
    reference = str(uuid.uuid4())
    description = request.data.get('description', '')
    payment = Payment.objects.create(
        user=request.user,
        amount=amount,
        currency='KES',
        status='processing',
        reference=reference,
        description=f'M-Pesa payment initiated for {phone}',
    )
    # Try real Daraja integration if credentials provided
    mpesa_env = getattr(settings, 'MPESA_ENV', 'sandbox')
    mpesa_key = getattr(settings, 'MPESA_CONSUMER_KEY', '')
    mpesa_secret = getattr(settings, 'MPESA_CONSUMER_SECRET', '')
    shortcode = getattr(settings, 'MPESA_SHORTCODE', '')
    passkey = getattr(settings, 'MPESA_PASSKEY', '')
    callback = getattr(settings, 'MPESA_CALLBACK_URL', '') or request.build_absolute_uri('/api/v1/payments/mpesa/callback/')

    if mpesa_key and mpesa_secret and shortcode and passkey:
        try:
            token = _mpesa_get_token(mpesa_env, mpesa_key, mpesa_secret)
            r, payload = _mpesa_stk_push(mpesa_env, shortcode, passkey, amount, phone, reference, callback, token)
            resp_json = None
            status_code = '0'
            try:
                if r is not None and r.content:
                    resp_json = r.json()
                status_code = str(r.status_code) if r is not None else '0'
            except Exception:
                resp_json = {'status': 'invalid-json'}

            try:
                PaymentIntegrationLog.objects.create(
                    payment=payment,
                    gateway=payment.gateway,
                    request_payload=payload,
                    response_payload=resp_json or {},
                    status_code=status_code
                )
            except Exception:
                pass

            return Response({'detail': 'MPESA STK push initiated', 'reference': reference, 'response': resp_json or {}}, status=200)
        except Exception:
            # fall through to simulated fallback logging
            pass

    try:
        PaymentIntegrationLog.objects.create(
            payment=payment,
            gateway=payment.gateway,
            request_payload={'phone': phone, 'amount': amount, 'reference': reference},
            response_payload={'message': 'STK push simulated fallback'},
            status_code='0'
        )
    except Exception:
        pass

    return Response({'detail': 'MPESA STK push initiated (simulated)', 'reference': reference}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def airtel_initiate(request):
    """Create a Payment and simulate Airtel Money STK push initiation.
    Expects: amount, phone
    """
    amount = request.data.get('amount')
    phone = request.data.get('phone')
    if not amount or not phone:
        return Response({'detail': 'amount and phone are required'}, status=status.HTTP_400_BAD_REQUEST)
    reference = str(uuid.uuid4())
    description = request.data.get('description', '')
    payment = Payment.objects.create(
        user=request.user,
        amount=amount,
        currency='KES',
        status='processing',
        reference=reference,
        description=f'Airtel Money payment initiated for {phone}',
    )
    # Try real Airtel integration if credentials provided
    try:
        airtel_key = getattr(settings, 'AIRTEL_CONSUMER_KEY', '')
        airtel_secret = getattr(settings, 'AIRTEL_CONSUMER_SECRET', '')
        shortcode = getattr(settings, 'AIRTEL_SHORTCODE', '')
        callback = getattr(settings, 'AIRTEL_CALLBACK_URL', '')
        if airtel_key and airtel_secret and shortcode:
            # Placeholder for Airtel Money API integration.
            # Real implementation depends on provider API (OAuth, STK or USSD flow).
            stk_url = getattr(settings, 'AIRTEL_STK_URL', '')
            payload = {
                'shortcode': shortcode,
                'amount': amount,
                'phone': phone,
                'reference': reference,
                'description': description or 'Uzuri payment',
                'callback': callback or request.build_absolute_uri('/api/v1/payments/airtel/callback/'),
            }
            headers = {'Content-Type': 'application/json'}
            try:
                r = requests.post(stk_url, json=payload, headers=headers, timeout=10) if stk_url else None
                resp_json = None
                status_code = '0'
                try:
                    if r is not None and r.content:
                        resp_json = r.json()
                    status_code = str(r.status_code) if r is not None else '0'
                except Exception:
                    resp_json = {'status': 'invalid-json'}
                try:
                    PaymentIntegrationLog.objects.create(
                        payment=payment,
                        gateway=payment.gateway,
                        request_payload=payload,
                        response_payload=resp_json or {},
                        status_code=status_code
                    )
                except Exception:
                    pass
                return Response({'detail': 'Airtel STK push initiated', 'reference': reference, 'response': resp_json or {}}, status=200)
            except Exception:
                # fall through to simulated fallback
                pass
    except Exception:
        try:
            PaymentIntegrationLog.objects.create(
                payment=payment,
                gateway=payment.gateway,
                request_payload={'phone': phone, 'amount': amount, 'reference': reference},
                response_payload={'message': 'Airtel STK push simulated fallback'},
                status_code='0'
            )
        except Exception:
            pass

    return Response({'detail': 'Airtel STK push initiated (simulated)', 'reference': reference}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def airtel_callback(request):
    """Handle Airtel Money STK push webhook/callback.
    Similar parsing to mpesa_callback but more generic for provider payloads.
    """
    expected = getattr(settings, 'AIRTEL_WEBHOOK_SECRET', '')
    if expected:
        secret = request.headers.get('X-Webhook-Secret') or request.META.get('HTTP_X_WEBHOOK_SECRET')
        if not secret or secret != expected:
            return Response({'detail': 'Invalid webhook secret.'}, status=403)

    payload = request.data
    reference = None
    receipt = None
    amount = None
    status_val = 'failed'
    try:
        # Provider-specific structure may vary; attempt to extract common fields
        if isinstance(payload, dict):
            reference = payload.get('account_reference') or payload.get('reference') or payload.get('AccountReference')
            receipt = payload.get('receipt') or payload.get('transaction_id') or payload.get('AirtelReceipt')
            amount = payload.get('amount') or payload.get('Amount')
            status_val = 'successful' if payload.get('status') in ('success', 'successful', '0') else payload.get('status', 'failed')
    except Exception:
        pass

    from .models import Payment, PaymentIntegrationLog, PaymentCallback
    if not reference:
        return Response({'detail': 'reference not found in callback payload.'}, status=400)
    payment = Payment.objects.filter(reference=reference).first()
    try:
        PaymentIntegrationLog.objects.create(
            payment=payment,
            gateway=payment.gateway if payment else None,
            request_payload=payload,
            response_payload={'handled': True},
            status_code=str(payload.get('status', '')) if isinstance(payload, dict) else ''
        )
    except Exception:
        pass

    if not payment:
        return Response({'detail': 'Payment not found for reference.'}, status=404)

    # Idempotency: attempt to extract a provider callback id to avoid double-processing
    callback_id = None
    try:
        if isinstance(payload, dict):
            callback_id = payload.get('callback_id') or payload.get('transaction_id') or payload.get('AirtelReceipt')
    except Exception:
        callback_id = None

    if callback_id:
        # Use a retry loop to handle rare IntegrityError races across processes
        try:
            from django.db import transaction, IntegrityError
            import time
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    with transaction.atomic():
                        cb_obj, created = PaymentCallback.objects.get_or_create(
                            callback_id=callback_id,
                            defaults={'provider': 'airtel', 'payment': payment, 'payload': payload}
                        )
                        if not created:
                            return Response({'detail': 'Callback already processed.'}, status=200)
                        break
                except IntegrityError:
                    # possible concurrent insert, retry briefly
                    if attempt < max_attempts - 1:
                        time.sleep(0.1 * (attempt + 1))
                        continue
                    else:
                        # final attempt failed, fallthrough (best-effort)
                        break
        except Exception:
            pass

    payment.transaction_id = receipt or payment.transaction_id
    payment.status = status_val
    payment.is_verified = status_val == 'successful'
    if amount:
        try:
            payment.amount = amount
        except Exception:
            pass
    payment.save()
    # Create an in-app notification so WebSocket clients get updates
    try:
        Notification.objects.create(
            user=payment.user,
            category='finance',
            type='payment_update',
            title=f'Payment {payment.reference} updated',
            message=f'Payment {payment.reference} status changed to {payment.status}.',
            urgency='info',
            channels=['in_app'],
            personalized_context={'reference': payment.reference, 'status': payment.status, 'transaction_id': payment.transaction_id, 'amount': str(payment.amount), 'currency': payment.currency},
        )
    except Exception:
        pass
    return Response({'detail': 'Payment updated.'}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def mpesa_callback(request):
    """Handle M-Pesa STK push webhook/callback from Safaricom/Daraja.

    Accepts the typical Daraja STK callback body and updates the Payment by
    AccountReference (the reference we send in the initiation payload).
    If a webhook secret is configured in settings as MPESA_WEBHOOK_SECRET, the
    request must include header 'X-Webhook-Secret' with the same value.
    """
    # Verify secret if configured
    expected = getattr(settings, 'MPESA_WEBHOOK_SECRET', '')
    if expected:
        secret = request.headers.get('X-Webhook-Secret') or request.META.get('HTTP_X_WEBHOOK_SECRET')
        if not secret or secret != expected:
            return Response({'detail': 'Invalid webhook secret.'}, status=403)

    payload = request.data
    # Try to parse standard Daraja STK callback structure
    reference = None
    receipt = None
    amount = None
    phone = None
    status_val = 'failed'
    try:
        body = payload.get('Body') if isinstance(payload, dict) else None
        if body and 'stkCallback' in body:
            cb = body['stkCallback']
            result_code = cb.get('ResultCode')
            status_val = 'successful' if result_code == 0 else 'failed'
            metadata = cb.get('CallbackMetadata', {}) or {}
            items = metadata.get('Item', [])
            meta = {it.get('Name'): it.get('Value') for it in items if isinstance(it, dict)}
            reference = meta.get('AccountReference') or meta.get('Account')
            receipt = meta.get('MpesaReceiptNumber') or meta.get('ReceiptNumber')
            amount = meta.get('Amount')
            phone = meta.get('PhoneNumber') or meta.get('Phone')
        else:
            # Fallback generic payload
            reference = payload.get('reference') or payload.get('account_reference') or payload.get('AccountReference')
            status_val = 'successful' if payload.get('status') in ('success', 'successful', '0') else payload.get('status', 'failed')
            receipt = payload.get('mpesa_receipt') or payload.get('transaction_id') or payload.get('MpesaReceiptNumber')
            amount = payload.get('amount')
            phone = payload.get('phone') or payload.get('PhoneNumber')
    except Exception:
        # best-effort parsing; continue
        pass

    # Find payment and update
    from .models import Payment, PaymentIntegrationLog, PaymentCallback
    if not reference:
        return Response({'detail': 'reference not found in callback payload.'}, status=400)

    payment = Payment.objects.filter(reference=reference).first()
    # Log the incoming webhook regardless
    try:
        PaymentIntegrationLog.objects.create(
            payment=payment,
            gateway=payment.gateway if payment else None,
            request_payload=payload,
            response_payload={'handled': True},
            status_code=str(payload.get('ResultCode', '')) if isinstance(payload, dict) else ''
        )
    except Exception:
        pass

    if not payment:
        return Response({'detail': 'Payment not found for reference.'}, status=404)

    # Idempotency: try to determine a provider callback id
    callback_id = None
    try:
        if isinstance(payload, dict):
            cb = payload.get('Body', {}).get('stkCallback') if payload.get('Body') else None
            if cb:
                callback_id = cb.get('CheckoutRequestID') or cb.get('MerchantRequestID')
            else:
                callback_id = payload.get('CallbackID') or payload.get('transaction_id') or payload.get('MpesaReceiptNumber')
    except Exception:
        callback_id = None

    if callback_id:
        # Use retry/backoff to handle IntegrityError races during creation
        try:
            from django.db import transaction, IntegrityError
            import time
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    with transaction.atomic():
                        cb_obj, created = PaymentCallback.objects.get_or_create(
                            callback_id=callback_id,
                            defaults={'provider': 'mpesa', 'payment': payment, 'payload': payload}
                        )
                        if not created:
                            return Response({'detail': 'Callback already processed.'}, status=200)
                        break
                except IntegrityError:
                    if attempt < max_attempts - 1:
                        time.sleep(0.1 * (attempt + 1))
                        continue
                    else:
                        break
        except Exception:
            pass

    # Update payment
    payment.transaction_id = receipt or payment.transaction_id
    payment.status = status_val
    payment.is_verified = status_val == 'successful'
    if amount:
        try:
            payment.amount = amount
        except Exception:
            pass
    payment.save()
    # Create an in-app notification so WebSocket clients get updates
    try:
        Notification.objects.create(
            user=payment.user,
            category='finance',
            type='payment_update',
            title=f'Payment {payment.reference} updated',
            message=f'Payment {payment.reference} status changed to {payment.status}.',
            urgency='info',
            channels=['in_app'],
            personalized_context={'reference': payment.reference, 'status': payment.status, 'transaction_id': payment.transaction_id, 'amount': str(payment.amount), 'currency': payment.currency},
        )
    except Exception:
        pass
    return Response({'detail': 'Payment updated.'}, status=200)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
    event = None
    if stripe and webhook_secret:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except Exception:
            return Response({'detail': 'Invalid signature'}, status=400)
    else:
        try:
            event = json.loads(payload)
        except Exception:
            return Response({'detail': 'Invalid payload'}, status=400)

    # Handle the event
    typ = event.get('type') if isinstance(event, dict) else getattr(event, 'type', None)
    data = event.get('data', {}) if isinstance(event, dict) else getattr(event, 'data', {})
    # Example: checkout.session.completed
    if typ == 'checkout.session.completed' or (isinstance(data, dict) and data.get('object', {}).get('payment_status') == 'paid'):
        session = data.get('object') if isinstance(data, dict) else None
        reference = session.get('client_reference_id') if session else None
        if reference:
            from .models import Payment
            try:
                p = Payment.objects.get(reference=reference)
                p.status = 'successful'
                p.transaction_id = session.get('payment_intent') or session.get('id')
                p.is_verified = True
                p.save()
            except Payment.DoesNotExist:
                pass

    return Response({'received': True})
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
