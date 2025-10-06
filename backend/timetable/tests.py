
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Timetable, TimetableEntry, TimetableChangeRequest

User = get_user_model()

class TimetableTests(APITestCase):
	def setUp(self):
		self.admin = User.objects.create_superuser('admin@example.com', 'pass', first_name='Admin', last_name='User')
		self.user = User.objects.create_user('user@example.com', 'pass', first_name='Test', last_name='User')
		self.timetable = Timetable.objects.create(
			program='BSc CS', year_of_study=1, semester='semester_1', academic_year='2023/2024'
		)
		self.entry = TimetableEntry.objects.create(
			timetable=self.timetable, unit_code='CS101', unit_name='Intro', lecturer='Dr. X',
			day_of_week='Monday', start_time='09:00', end_time='11:00', venue='A1'
		)

	def test_admin_can_create_timetable(self):
		self.client.force_authenticate(self.admin)
		data = {
			'program': 'BSc IT', 'year_of_study': 2, 'semester': 'semester_2', 'academic_year': '2023/2024'
		}
		resp = self.client.post('/api/timetable/timetables/', data, follow=True)
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

	def test_user_cannot_create_timetable(self):
		self.client.force_authenticate(self.user)
		data = {
			'program': 'BSc IT', 'year_of_study': 2, 'semester': 'semester_2', 'academic_year': '2023/2024'
		}
		resp = self.client.post('/api/timetable/timetables/', data, follow=True)
		self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

	def test_user_can_create_change_request(self):
		self.client.force_authenticate(self.user)
		data = {
			'timetable_entry': self.entry.id,
			'change_type': 'reschedule',
			'details': 'Move to Tuesday',
		}
		resp = self.client.post('/api/timetable/change-requests/', data, follow=True)
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

	def test_admin_can_approve_change_request(self):
		self.client.force_authenticate(self.user)
		cr = TimetableChangeRequest.objects.create(
			timetable_entry=self.entry, change_type='reschedule', details='Move', requested_by=self.user
		)
		self.client.force_authenticate(self.admin)
		resp = self.client.post(f'/api/timetable/change-requests/{cr.id}/approve/')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		cr.refresh_from_db()
		self.assertEqual(cr.status, 'approved')
