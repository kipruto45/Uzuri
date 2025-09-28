from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification, NotificationDeliveryLog
from .tasks import send_notification_sms, log_notification_delivery

class NotificationDeliveryTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpass')
        self.notification = Notification.objects.create(user=self.user, message='Test message')

    def test_log_notification_delivery(self):
        log_notification_delivery(self.notification, 'delivered', 'email')
        self.assertEqual(NotificationDeliveryLog.objects.count(), 1)
        log = NotificationDeliveryLog.objects.first()
        self.assertEqual(log.status, 'delivered')
        self.assertEqual(log.channel, 'email')

	# Add more tests for retry logic, status updates, and management command as needed
from rest_framework.test import APIClient
from .models import StudentProfile, IDCardReplacementRequest

class PermissionsWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='student@example.com', password='testpass', first_name='Test', last_name='Student')
        self.profile = StudentProfile.objects.create(user=self.user, program='CS', year_of_study=2, dob='2000-01-01', gender='M', phone='123456789', address='Test Address', emergency_contact='Parent', profile_photo=None)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_view_profile(self):
        response = self.client.get('/api/student/profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user'], str(self.user))

    def test_update_profile(self):
        response = self.client.patch('/api/student/profile/', {'phone': '987654321'}, format='json', follow=True)
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(response.data['phone'], '987654321')

    def test_id_card_download_once(self):
        response = self.client.get('/api/student/profile/id-card/', follow=True)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.get('/api/student/profile/id-card/', follow=True)
        self.assertEqual(response2.status_code, 403)

    def test_id_card_request_and_admin_approval(self):
        response = self.client.post('/api/student/profile/id-card/request/', {'reason': 'lost'}, format='json', follow=True)
        self.assertEqual(response.status_code, 201)
        req = IDCardReplacementRequest.objects.get(student=self.profile)
        req.status = 'approved'
        req.save()
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.id_card_downloaded)
from django.test import TestCase

# Create your tests here.
