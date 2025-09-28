
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification
from rest_framework.test import APIClient

class NotificationDeliveryTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(email='student1@example.com', password='testpass')
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)
		Notification.objects.create(user=self.user, message='Test notification', channels=['in_app', 'email', 'sms', 'push'])

	def test_notification_analytics(self):
		response = self.client.get('/api/notifications/analytics/')
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertIn('opened', data)
		self.assertIn('ignored', data)
		self.assertIn('total', data)
