
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from my_profile.models import StudentProfile
from fees.models import Invoice
from .models import Hostel, Room, HostelApplication, RoomAllocation
from django.contrib.auth import get_user_model

User = get_user_model()

class HostelStudentEndpointsTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			email='student@example.com',
			password='pass',
			first_name='Test',
			last_name='Student'
		)
		self.profile = StudentProfile.objects.create(
			user=self.user,
			program='BSc CS',
			year_of_study=1,
			dob='2000-01-01',
			gender='M',
			phone='0712345678',
			address='123 Main St',
			emergency_contact='Parent',
		)
		self.hostel = Hostel.objects.create(name='Alpha', location='Campus', description='Test hostel')
		self.room = Room.objects.create(hostel=self.hostel, number='101', capacity=2)
		# Obtain JWT token
		login_url = reverse('auth-login')
		resp = self.client.post(login_url, {'email': 'student@example.com', 'password': 'pass'}, format='json', follow=True)
		assert resp.status_code in [200, 201], f"Login failed: {resp.data}"
		token = resp.data.get('access')
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

	def test_list_rooms(self):
		url = reverse('student-hostel-rooms')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue(len(resp.data) > 0)

	def test_apply_for_room(self):
		url = reverse('student-hostel-apply')
		data = {'semester': '2025-1', 'room_id': self.room.id}
		resp = self.client.post(url, data)
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertIn('Your hostel application has been submitted.', resp.data['detail'])

	def test_prevent_duplicate_application(self):
		HostelApplication.objects.create(student=self.profile, room=self.room, semester='2025-1', status='pending')
		url = reverse('student-hostel-apply')
		data = {'semester': '2025-1', 'room_id': self.room.id}
		resp = self.client.post(url, data)
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_my_applications(self):
		HostelApplication.objects.create(student=self.profile, room=self.room, semester='2025-1', status='pending')
		url = reverse('student-hostel-my-applications')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue(len(resp.data) > 0)

	def test_my_room_none(self):
		url = reverse('student-hostel-my-room')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

	def test_fees_none(self):
		url = reverse('student-hostel-fees')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
