
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import ClearanceDepartment, ClearanceRequest, ClearanceApproval, ClearanceDocument
from rest_framework.test import APIClient
from django.urls import reverse

class ClearanceModuleTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			email='student1@example.com', password='pass', first_name='Student', last_name='One')
		self.admin = get_user_model().objects.create_superuser(
			email='admin@example.com', password='adminpass', first_name='Admin', last_name='User')
		self.dept = ClearanceDepartment.objects.create(name='Library')
		self.client = APIClient()

	def test_clearance_request_creation(self):
		req = ClearanceRequest.objects.create(student=self.user)
		self.assertEqual(req.status, 'pending')

	def test_api_department_list_admin(self):
		self.client.force_authenticate(user=self.admin)
		url = reverse('clearancedepartment-list')
		resp = self.client.get(url, follow=True)
		self.assertEqual(resp.status_code, 200)

	def test_api_request_create(self):
		self.client.force_authenticate(user=self.user)
		url = reverse('clearancerequest-list')
		data = {'student': self.user.id}
		resp = self.client.post(url, data, follow=True)
		self.assertEqual(resp.status_code, 201)
