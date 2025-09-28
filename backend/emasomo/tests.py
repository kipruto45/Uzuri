from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from core.models import CustomUser, Role
from rest_framework.authtoken.models import Token

class LoginWithEmailTests(APITestCase):
    def setUp(self):
        role = Role.objects.create(name='Student')
        self.user = CustomUser.objects.create_user(email='student@example.com', password='testpass123', first_name='Test', last_name='Student', role=role)

    def test_login_success(self):
        url = reverse('login-with-email')
        response = self.client.post(url, {'email': 'student@example.com', 'password': 'testpass123'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_failure(self):
        url = reverse('login-with-email')
        response = self.client.post(url, {'email': 'student@example.com', 'password': 'wrongpass'}, follow=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)
