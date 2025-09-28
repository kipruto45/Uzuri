from django.test import TestCase
from django.contrib.auth import get_user_model
from my_profile.models import StudentProfile
from .models import AcademicLeaveRequest
from datetime import date, timedelta

class AcademicLeaveRequestTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(email='student1@example.com', password='testpass', first_name='Student', last_name='One')
		self.profile = StudentProfile.objects.create(user=self.user, program='CS', year_of_study=1, dob='2000-01-01', gender='M', phone='123', address='Test', registration_date=date.today(), emergency_contact='Test')
		self.staff = User.objects.create_user(email='staff1@example.com', password='testpass', first_name='Staff', last_name='User', is_staff=True)

	def test_create_leave_request(self):
		leave = AcademicLeaveRequest.objects.create(
			student=self.profile,
			leave_type='Medical',
			reason='Sick',
			start_date=date.today(),
			end_date=date.today() + timedelta(days=7)
		)
		self.assertEqual(leave.status, 'pending')
		self.assertEqual(str(leave), f"Leave #{leave.id} - {self.profile} ({leave.status})")

	def test_approve_leave_request(self):
		leave = AcademicLeaveRequest.objects.create(
			student=self.profile,
			leave_type='Medical',
			reason='Sick',
			start_date=date.today(),
			end_date=date.today() + timedelta(days=7)
		)
		leave.status = 'approved'
		leave.save()
		self.assertEqual(leave.status, 'approved')

	def test_reject_leave_request(self):
		leave = AcademicLeaveRequest.objects.create(
			student=self.profile,
			leave_type='Medical',
			reason='Sick',
			start_date=date.today(),
			end_date=date.today() + timedelta(days=7)
		)
		leave.status = 'rejected'
		leave.save()
		self.assertEqual(leave.status, 'rejected')

	def test_student_can_only_see_own_requests(self):
		leave1 = AcademicLeaveRequest.objects.create(
			student=self.profile,
			leave_type='Medical',
			reason='Sick',
			start_date=date.today(),
			end_date=date.today() + timedelta(days=7)
		)
		# Create another student and leave
		User = get_user_model()
		user2 = User.objects.create_user(email='student2@example.com', password='testpass', first_name='Student', last_name='Two')
		profile2 = StudentProfile.objects.create(user=user2, program='CS', year_of_study=1, dob='2000-01-01', gender='F', phone='456', address='Test', registration_date=date.today(), emergency_contact='Test')
		leave2 = AcademicLeaveRequest.objects.create(
			student=profile2,
			leave_type='Personal',
			reason='Family',
			start_date=date.today(),
			end_date=date.today() + timedelta(days=3)
		)
		# Simulate queryset filtering
		own_leaves = AcademicLeaveRequest.objects.filter(student=self.profile)
		self.assertIn(leave1, own_leaves)
		self.assertNotIn(leave2, own_leaves)
from django.test import TestCase

# Create your tests here.
