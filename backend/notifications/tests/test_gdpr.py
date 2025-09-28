from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from notifications.models import UserPreferences, Notification

class GDPRExportDeleteTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='gdpruser', password='testpass')
        self.client.login(username='gdpruser', password='testpass')
        UserPreferences.objects.create(user=self.user, preferred_channels=['email'], language='en', accessibility_mode=True)
        Notification.objects.create(user=self.user, category='general', type='info', title='Test', message='Test message')

    def test_export_data(self):
        url = reverse('userpreferences-export-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('preferences', response.data)
        self.assertIn('notifications', response.data)

    def test_delete_data(self):
        url = reverse('userpreferences-delete-data')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'User data deleted.')
        self.assertFalse(UserPreferences.objects.filter(user=self.user).exists())
        self.assertFalse(Notification.objects.filter(user=self.user).exists())
