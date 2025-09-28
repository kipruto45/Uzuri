from django.db import models



from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .models import Receipt, Transaction, Invoice
from core.models_shared import CustomUser
import qrcode
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
TWILIO_FROM_NUMBER = getattr(settings, 'TWILIO_FROM_NUMBER', None)


@shared_task
def generate_receipt_pdf_task(receipt_id):
    from .models import Receipt
    receipt = Receipt.objects.get(id=receipt_id)
    tx = receipt.transaction
    # Generate QR code
    qr = qrcode.make(f"Verify: {tx.reference}")
    qr_io = io.BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    # Generate PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Payment Receipt")
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"Student: {tx.student}")
    c.drawString(100, 760, f"Invoice: {tx.invoice}")
    c.drawString(100, 740, f"Amount: {tx.amount}")
    c.drawString(100, 720, f"Method: {tx.method}")
    c.drawString(100, 700, f"Reference: {tx.reference}")
    c.drawString(100, 680, f"Status: {tx.status}")
    c.drawString(100, 660, f"Date: {tx.created_at}")
    # Add QR code
    c.drawImage(ImageReader(qr_io), 400, 700, width=40*mm, height=40*mm)
    # Digital signature (stub)
    c.drawString(100, 640, "Finance Signature: ______________")
    c.save()
    buffer.seek(0)
    # Save PDF and QR to model
    receipt.pdf_file.save(f'receipt_{receipt.id}.pdf', buffer)
    receipt.qr_code.save(f'qr_{receipt.id}.png', qr_io)
    receipt.save()

@shared_task
def send_notification_task(user_id, message):
    # Send email
    user = CustomUser.objects.get(id=user_id)
    if user.email:
        send_mail('Finance Notification', message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
    # Send SMS
    if hasattr(user, 'phone') and user.phone and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=user.phone
        )

@shared_task
def reconcile_payments_task(statement_file_path):
    # TODO: Parse bank statement and reconcile payments
    pass


@shared_task
def send_overdue_reminders_task():
    # Find overdue invoices and send reminders
    overdue_invoices = Invoice.objects.filter(status='overdue')
    for invoice in overdue_invoices:
        send_notification_task.delay(invoice.student.user.id, f'Invoice overdue! Settle balance by {invoice.due_date}.')

@shared_task
def auto_generate_invoices_task():
    # Example: Auto-generate invoices for all active students (stub logic)
    from my_profile.models import StudentProfile
    students = StudentProfile.objects.filter(is_active=True)
    for student in students:
        # Only create if not already invoiced for this period (stub)
        Invoice.objects.get_or_create(
            student=student,
            defaults={
                'amount': 10000,  # Placeholder
                'status': 'pending',
            }
        )

@shared_task
def auto_clearance_task():
    # Example: Auto-clear students who have paid all fees (stub logic)
    from my_profile.models import StudentProfile
    students = StudentProfile.objects.all()
    for student in students:
        total_invoiced = Invoice.objects.filter(student=student).aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_paid = Transaction.objects.filter(student=student, status='success').aggregate(models.Sum('amount'))['amount__sum'] or 0
        if total_paid >= total_invoiced and total_invoiced > 0:
            # Mark as cleared (add a field or status as needed)
            pass
