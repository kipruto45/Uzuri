from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from notifications.models import Notification

class PushAnalyticsWebhookTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='pushuser', password='testpass')
        Notification.objects.create(user=self.user, category='general', type='info', title='Push', message='Push test', channels=['push'])

    def test_push_status_field(self):
        notif = Notification.objects.filter(user=self.user).first()
        self.assertEqual(notif.push_status, 'pending')

    def test_analytics_endpoint(self):
        # This assumes an analytics endpoint exists
        response = self.client.get('/api/notifications/analytics/')
        self.assertIn('total', response.data)
        self.assertIn('unread', response.data)

    def test_webhook_logs(self):
        # This assumes a webhook logs endpoint exists
        response = self.client.get('/api/notifications/admin/dashboard/')
        self.assertIn('webhook_logs', response.data)
