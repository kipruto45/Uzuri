import requests
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from .models import Transaction, Invoice
from .tasks import generate_receipt_pdf_task, send_notification_task

# M-Pesa STK Push Initiation (production)
def initiate_mpesa_stk_push(phone_number, amount, reference):
    # Use production credentials from settings
    mpesa_env = getattr(settings, 'MPESA_ENV', 'sandbox')
    consumer_key = getattr(settings, 'MPESA_CONSUMER_KEY', 'your_key')
    consumer_secret = getattr(settings, 'MPESA_CONSUMER_SECRET', 'your_secret')
    shortcode = getattr(settings, 'MPESA_SHORTCODE', '123456')
    passkey = getattr(settings, 'MPESA_PASSKEY', 'passkey')
    callback_url = getattr(settings, 'MPESA_CALLBACK_URL', 'https://yourdomain.com/api/fees/mpesa-webhook/')
    # Token request
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials' if mpesa_env == 'sandbox' else 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    access_token = r.json().get('access_token')
    # STK push request
    stk_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest' if mpesa_env == 'sandbox' else 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    import base64
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": reference,
        "TransactionDesc": "Fee Payment"
    }
    resp = requests.post(stk_url, json=payload, headers=headers)
    return resp.json()


# Webhook for M-Pesa payment confirmation
from .models import AuditTrail
class MpesaWebhookView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    def post(self, request):
        # Webhook security: check secret token
        secret = request.headers.get('X-Webhook-Secret')
        if secret != getattr(settings, 'MPESA_WEBHOOK_SECRET', 'changeme'):
            return Response({'detail': 'Invalid webhook secret.'}, status=403)
        # Parse M-Pesa callback
        data = request.data
        reference = data.get('reference')
        status = data.get('status')
        amount = data.get('amount')
        tx = Transaction.objects.filter(reference=reference).first()
        if tx and status == 'success':
            tx.status = 'success'
            tx.amount = amount
            tx.save()
            generate_receipt_pdf_task.delay(tx.receipt.id)
            send_notification_task.delay(tx.student.user.id, f'Payment received: {amount}')
            # Audit log
            AuditTrail.objects.create(user=tx.student.user, action='payment_confirmed', model='Transaction', object_id=tx.id, changes=f'after: success')
        return Response({'detail': 'OK'})

# Bank/Manual Payment Recording (Finance)
def record_manual_payment(invoice_id, amount, reference, user):
    invoice = Invoice.objects.get(id=invoice_id)
    tx = Transaction.objects.create(
        student=invoice.student,
        invoice=invoice,
        amount=amount,
        method='manual',
        reference=reference,
        status='success',
    )
    generate_receipt_pdf_task.delay(tx.receipt.id)
    send_notification_task.delay(tx.student.user.id, f'Manual payment recorded: {amount}')
    return tx

# Notification Delivery (Email/SMS)
def send_email_notification(user, subject, message):
    from django.core.mail import send_mail
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def send_sms_notification(phone, message):
    # Integrate with Africa's Talking using API key from settings
    sms_api_key = getattr(settings, 'SMS_API_KEY', 'atsk_c8f2fd938d2c2ddcc46c353f9e1e2f5a71c12fab5e490d2a80142c0cf78f4ae473b492f0')
    sms_sender = getattr(settings, 'SMS_SENDER', 'Uzurisystem')
    sms_url = getattr(settings, 'SMS_URL', 'https://api.africastalking.com/version1/messaging')
    headers = {
        'apiKey': sms_api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'username': sms_sender,  # Africa's Talking username
        'to': phone,
        'message': message,
        'from': sms_sender,  # Sender ID (if allowed by your account)
    }
    try:
        resp = requests.post(sms_url, data=data, headers=headers)
        return resp.json()
    except Exception as e:
        return {'status': 'error', 'detail': str(e)}

# Celery Beat Task for Overdue Reminders
from celery import shared_task
@shared_task
def send_overdue_reminders():
    from .models import Invoice
    overdue = Invoice.objects.filter(status='overdue')
    for inv in overdue:
        send_notification_task.delay(inv.student.user.id, f'Invoice overdue! Settle by {inv.due_date}')
