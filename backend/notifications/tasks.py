from celery import shared_task
from .models import Notification, NotificationAuditLog
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
# Africa's Talking SMS integration
import africastalking
from django.conf import settings
AFRICASTALKING_USERNAME = getattr(settings, 'AFRICASTALKING_USERNAME', None)
AFRICASTALKING_API_KEY = getattr(settings, 'AFRICASTALKING_API_KEY', None)
AFRICASTALKING_FROM_NUMBER = getattr(settings, 'AFRICASTALKING_FROM_NUMBER', None)
if AFRICASTALKING_USERNAME and AFRICASTALKING_API_KEY:
    africastalking.initialize(AFRICASTALKING_USERNAME, AFRICASTALKING_API_KEY)
    sms = africastalking.SMS

@shared_task(bind=True, max_retries=3)
def send_notification_task(self, notification_id):
    try:
        notif = Notification.objects.get(id=notification_id)
        # Analytics hooks
        try:
            import requests
            # Google Analytics Measurement Protocol
            GA_MEASUREMENT_ID = getattr(settings, 'GA_MEASUREMENT_ID', None)
            GA_API_SECRET = getattr(settings, 'GA_API_SECRET', None)
            if GA_MEASUREMENT_ID and GA_API_SECRET:
                ga_url = f'https://www.google-analytics.com/mp/collect?measurement_id={GA_MEASUREMENT_ID}&api_secret={GA_API_SECRET}'
                ga_payload = {
                    'client_id': str(notif.user.id),
                    'events': [{
                        'name': 'notification_sent',
                        'params': {
                            'category': notif.category,
                            'channels': ','.join(notif.channels),
                            'urgency': notif.urgency,
                        }
                    }]
                }
                requests.post(ga_url, json=ga_payload)
            # Mixpanel
            MIXPANEL_TOKEN = getattr(settings, 'MIXPANEL_TOKEN', None)
            if MIXPANEL_TOKEN:
                mixpanel_url = 'https://api.mixpanel.com/track'
                mixpanel_payload = {
                    'event': 'Notification Sent',
                    'properties': {
                        'token': MIXPANEL_TOKEN,
                        'distinct_id': str(notif.user.id),
                        'category': notif.category,
                        'channels': notif.channels,
                        'urgency': notif.urgency,
                    }
                }
                requests.post(mixpanel_url, json=mixpanel_payload)
        except Exception:
            pass
        # Example: send via all channels
        for channel in notif.channels:
            if channel == 'email' and notif.user.email:
                send_mail(
                    notif.title,
                    notif.message,
                    settings.DEFAULT_FROM_EMAIL,
                    [notif.user.email],
                    fail_silently=False,
                )
            elif channel == 'sms' and hasattr(notif.user, 'phone') and notif.user.phone:
                if AFRICASTALKING_USERNAME and AFRICASTALKING_API_KEY and AFRICASTALKING_FROM_NUMBER:
                    response = sms.send(
                        notif.message,
                        [notif.user.phone],
                        sender_id=AFRICASTALKING_FROM_NUMBER
                    )
            elif channel == 'push':
                # Firebase Cloud Messaging integration
                import requests
                fcm_url = 'https://fcm.googleapis.com/fcm/send'
                fcm_server_key = getattr(settings, 'FCM_SERVER_KEY', None)
                if hasattr(notif.user, 'device_token') and notif.user.device_token and fcm_server_key:
                    headers = {
                        'Authorization': f'key {fcm_server_key}',
                        'Content-Type': 'application/json',
                    }
                    payload = {
                        'to': notif.user.device_token,
                        'notification': {
                            'title': notif.title,
                            'body': notif.message,
                        },
                        'data': {
                            'notification_id': notif.id,
                        }
                    }
                    try:
                        response = requests.post(fcm_url, json=payload, headers=headers)
                        response.raise_for_status()
                        notif.push_status = 'sent'
                        notif.save()
                    except Exception as e:
                        notif.push_status = 'failed'
                        notif.save()
                        NotificationAuditLog.objects.create(
                            notification=notif,
                            channel=channel,
                            status='failed',
                            attempt=1,
                            response=str(e),
                        )
                        continue
                # OneSignal integration
                onesignal_app_id = getattr(settings, 'ONESIGNAL_APP_ID', None)
                onesignal_api_key = getattr(settings, 'ONESIGNAL_API_KEY', None)
                if onesignal_app_id and onesignal_api_key and notif.push_token:
                    onesignal_url = 'https://onesignal.com/api/v1/notifications'
                    headers = {
                        'Authorization': f'Basic {onesignal_api_key}',
                        'Content-Type': 'application/json',
                    }
                    payload = {
                        'app_id': onesignal_app_id,
                        'include_player_ids': [notif.push_token],
                        'headings': {'en': notif.title},
                        'contents': {'en': notif.message},
                        'data': {'notification_id': notif.id},
                    }
                    try:
                        response = requests.post(onesignal_url, json=payload, headers=headers)
                        response.raise_for_status()
                        notif.push_status = 'sent'
                        notif.save()
                    except Exception as e:
                        notif.push_status = 'failed'
                        notif.save()
                        NotificationAuditLog.objects.create(
                            notification=notif,
                            channel=channel,
                            status='failed',
                            attempt=1,
                            response=str(e),
                        )
                        continue
            NotificationAuditLog.objects.create(
                notification=notif,
                channel=channel,
                status='success',
                attempt=1,
                response='sent',
            )
            NotificationAuditLog.objects.create(
                notification=notif,
                channel=channel,
                status='success',
                attempt=1,
                response='Sent',
                timestamp=timezone.now()
            )
        notif.sent = True
        notif.sent_at = timezone.now()
        notif.save()
    except Exception as e:
        NotificationAuditLog.objects.create(
            notification_id=notification_id,
            channel='unknown',
            status='failed',
            attempt=self.request.retries + 1,
            response=str(e),
            timestamp=timezone.now()
        )
        raise self.retry(exc=e, countdown=60)
