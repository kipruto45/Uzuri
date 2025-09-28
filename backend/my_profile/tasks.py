import logging
from celery import shared_task
logger = logging.getLogger(__name__)
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from .models import Notification, NotificationDeliveryLog
from datetime import timedelta
from django.utils import timezone

@shared_task
def send_notification(user_email, event, context=None, channels=None):
    """
    Send notification using templates and modular sender.
    event: 'special_approved', 'supplementary_ready', 'card_generated', 'exam_changed', etc.
    context: dict with dynamic content (student name, exam details, etc.)
    channels: list of channels ['email', 'sms', 'in_app']
    """
    if channels is None:
        channels = ['email', 'in_app', 'sms']
    templates = {
        'special_approved': {
            'subject': 'Special Exam Card Approval Notification',
            'message': 'Dear {name},\n\nYour request for a Special Exam Card for {semester} has been approved by the Registrar. Please log in to the student portal to view your card and exam details.\n\nBest regards,\nUzuri University Exams Office',
            'sms': 'Uzuri University: Your Special Exam Card for {semester} is approved. Log in to portal for details.'
        },
        'supplementary_ready': {
            'subject': 'Supplementary Exam Card Ready',
            'message': 'Dear {name},\n\nYour Supplementary Exam Card for {semester} is now available. The following units are scheduled: {units}. Please ensure you have cleared all required fees.\n\nBest regards,\nUzuri University Exams Office',
            'sms': 'Uzuri University: Supplementary Exam Card for {semester} ready. Units: {units}. Fees must be cleared.'
        },
        'card_generated': {
            'subject': 'Exam Card Generated',
            'message': 'Dear {name},\n\nYour Exam Card for {semester} has been generated and is available for download. Please check the student portal for your exam schedule and venue.\n\nBest regards,\nUzuri University Exams Office',
            'sms': 'Uzuri University: Exam Card for {semester} generated. Check portal for schedule and venue.'
        },
        'exam_changed': {
            'subject': 'Exam Schedule Update',
            'message': 'Dear {name},\n\nPlease note that your exam schedule for {semester} has changed. New details: {details}.\n\nBest regards,\nUzuri University Exams Office',
            'sms': 'Uzuri University: Exam schedule for {semester} updated. See portal for new details.'
        },
    }
    tpl = templates.get(event, templates['card_generated'])
    subject = tpl['subject']
    message = tpl['message'].format(**context)
    sms_message = tpl.get('sms', message).format(**context)
    # In-app notification
    if 'in_app' in channels:
        notif = Notification.objects.create(
            user=settings.AUTH_USER_MODEL.objects.get(email=user_email),
            message=message,
            type=event,
            delivery_status="delivered",
        )
        log_notification_delivery(notif, "delivered", "in_app")
    # Email notification
    if 'email' in channels:
        send_mail(subject, message, 'noreply@uzuriuniversity.com', [user_email], fail_silently=False)
        logger.info(f"Email sent to {user_email} with subject '{subject}'")
    # SMS notification
    if 'sms' in channels:
        phone = context.get('phone')
        if phone:
            send_notification_sms.delay(phone, sms_message)

@shared_task
def send_notification_sms(phone_number, message):
    import africastalking
    africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
    sms = africastalking.SMS
    try:
        response = sms.send(message, [phone_number])
        logger.info(f"Africa's Talking SMS sent to {phone_number}: {response}")
        notif = Notification.objects.filter(user__profile__phone_number=phone_number, message=message).first()
        if notif:
            notif.delivery_status = "delivered"
            notif.last_attempt = timezone.now()
            notif.error_message = None
            notif.save(update_fields=["delivery_status", "last_attempt", "error_message"])
            log_notification_delivery(notif, "delivered", "sms")
    except Exception as e:
        logger.error(f"Africa's Talking SMS failed for {phone_number}: {str(e)}")
        notif = Notification.objects.filter(user__profile__phone_number=phone_number, message=message).first()
        if notif:
            notif.delivery_status = "failed"
            notif.last_attempt = timezone.now()
            notif.error_message = str(e)
            notif.save(update_fields=["delivery_status", "last_attempt", "error_message"])
            log_notification_delivery(notif, "failed", "sms", error_message=str(e))

@shared_task
def auto_archive_notifications():
    threshold = timezone.now() - timedelta(days=90)
    Notification.objects.filter(created_at__lt=threshold).update(is_read=True)

def log_notification_delivery(notification, status, channel, error_message=None, user_agent=None, ip_address=None):
    NotificationDeliveryLog.objects.create(
        notification=notification,
        status=status,
        channel=channel,
        error_message=error_message,
        user_agent=user_agent,
        ip_address=ip_address,
    )
