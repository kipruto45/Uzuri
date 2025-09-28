
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import GraduationEvent, GraduationApplication, GraduationClearance, GraduationCertificate
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import date

class GraduationModuleTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			email='student1@example.com', password='pass', first_name='Student', last_name='One')
		self.admin = get_user_model().objects.create_superuser(
			email='admin@example.com', password='adminpass', first_name='Admin', last_name='User')
		self.event = GraduationEvent.objects.create(name='2025 Main', date=date.today(), location='Hall A')
		self.client = APIClient()

	def test_graduation_application_creation(self):
		app = GraduationApplication.objects.create(student=self.user, event=self.event)
		self.assertEqual(app.status, 'pending')
		self.assertFalse(app.is_eligible)

	def test_api_event_list_admin(self):
		self.client.force_authenticate(user=self.admin)
		url = reverse('graduationevent-list')
		resp = self.client.get(url, follow=True)
		self.assertEqual(resp.status_code, 200)

	def test_api_application_create(self):
		self.client.force_authenticate(user=self.user)
		url = reverse('graduationapplication-list')
		data = {'student': self.user.id, 'event': self.event.id}
		resp = self.client.post(url, data, follow=True)
		self.assertEqual(resp.status_code, 201)
