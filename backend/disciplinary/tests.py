
from django.test import TestCase
from django.contrib.auth import get_user_model
from my_profile.models import StudentProfile
from .models import DisciplinaryCase
from rest_framework.test import APIClient

class DisciplinaryAnalyticsTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(email='student1@example.com', password='testpass')
		self.profile = StudentProfile.objects.create(user=self.user, program='CS', year_of_study=1)
		self.staff = User.objects.create_user(email='staff1@example.com', password='testpass', is_staff=True)
		self.client = APIClient()
		self.client.force_authenticate(user=self.staff)
		for status in ['resolved', 'reported', 'appealed']:
			DisciplinaryCase.objects.create(student=self.profile, status=status)

	def test_analytics_endpoint(self):
		response = self.client.get('/api/disciplinary/cases/analytics/')
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(data['total_cases'], 3)
		self.assertEqual(data['resolved'], 1)
		self.assertEqual(data['pending'], 1)
		self.assertEqual(data['appeals'], 1)
