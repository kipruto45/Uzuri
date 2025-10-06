
from django.test import TestCase
from django.contrib.auth import get_user_model
from my_profile.models import StudentProfile
from .models import DisciplinaryCase
from rest_framework.test import APIClient

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

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

	def test_create_case_and_submit_appeal_and_upload_evidence(self):
		# create a case as staff
		payload = {
			'student_id': self.profile.id,
			'case_type': 'cheating',
			'description': 'Suspected cheating during exam',
		}
		resp = self.client.post('/api/disciplinary/', payload, format='json')
		self.assertIn(resp.status_code, (200, 201))
		case_data = resp.json()
		case_id = case_data.get('id')
		self.assertIsNotNone(case_id)

		# submit appeal as the student (authenticate as student)
		self.client.force_authenticate(user=self.user)
		appeal_payload = {'reason': 'I did not cheat'}
		resp2 = self.client.post(f'/api/disciplinary/{case_id}/appeal/', appeal_payload, format='json')
		self.assertIn(resp2.status_code, (200, 201))

		# upload evidence as student
		file = SimpleUploadedFile('evidence.txt', b'This is a test file')
		resp3 = self.client.post(f'/api/disciplinary/{case_id}/evidence/', {'file': file, 'description': 'Test'}, format='multipart')
		self.assertIn(resp3.status_code, (200, 201))

	def test_unauthenticated_cannot_create(self):
		# unauthenticated user cannot create a case
		self.client.force_authenticate(user=None)
		payload = {'student_id': self.profile.id, 'case_type': 'cheating', 'description': 'x'}
		resp = self.client.post('/api/disciplinary/', payload, format='json')
		self.assertIn(resp.status_code, (401, 403))

	def test_evidence_file_size_limit(self):
		# create a case as staff
		payload = {'student_id': self.profile.id, 'case_type': 'cheating', 'description': 'y'}
		resp = self.client.post('/api/disciplinary/', payload, format='json')
		case_id = resp.json().get('id')
		# create an oversized file (~12MB)
		big = SimpleUploadedFile('big.bin', b'a' * (12 * 1024 * 1024))
		self.client.force_authenticate(user=self.user)
		resp2 = self.client.post(f'/api/disciplinary/{case_id}/evidence/', {'file': big}, format='multipart')
		self.assertEqual(resp2.status_code, 400)

	def test_permission_for_case_list(self):
		# student should only see own cases
		self.client.force_authenticate(user=self.user)
		resp = self.client.get('/api/disciplinary/')
		self.assertEqual(resp.status_code, 200)
