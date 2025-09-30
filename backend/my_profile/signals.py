from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IDCardReplacementRequest
from django.core.mail import send_mail

def send_in_app_notification(student, message):
    import logging
    logger = logging.getLogger(__name__)
    from .models import Notification
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    # Provide conservative defaults for notification type and link when called from signals
    notif_type = 'system'
    link = ''
    notification = Notification.objects.create(user=student, message=message, type=notif_type, link=link)
    # Log delivery attempt for audit (WebSocket)
    from .tasks import log_notification_delivery
    # User agent and IP are not available in signal context, so pass None
    log_notification_delivery(notification, "delivered", "websocket", user_agent=None, ip_address=None)
    # Real-time WebSocket broadcast
    channel_layer = get_channel_layer()
    group_name = f"notifications_{student.id}"
    try:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send.notification",
                "content": {
                    "id": notification.id,
                    "message": notification.message,
                    "type": notification.type,
                    "link": notification.link,
                    "is_read": notification.is_read,
                    "created_at": str(notification.created_at),
                },
            },
        )
        logger.info(f"WebSocket notification sent to {student}")
    except Exception as e:
        logger.error(f"Failed to send WebSocket notification to {student}: {e}")

@receiver(post_save, sender=IDCardReplacementRequest)
def notify_id_card_request(sender, instance, created, **kwargs):
    if not created and instance.status in ['approved', 'declined']:
        student = instance.student.user
        if instance.status == 'approved':
            msg = "Your replacement request has been approved. You may now download your new ID card."
        else:
            msg = "Your replacement request was declined. Contact administration for details."
        send_in_app_notification(student, msg)
        send_mail(
            subject="ID Card Replacement Request Update",
            message=msg,
            from_email="noreply@uzuriuniversity.com",
            recipient_list=[student.email],
            fail_silently=True,
        )
