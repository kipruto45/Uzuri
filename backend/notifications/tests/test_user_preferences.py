from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from notifications.models import UserPreferences

class UserPreferencesAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_user_preferences(self):
        UserPreferences.objects.create(user=self.user, preferred_channels=['email'], language='en', accessibility_mode=True)
        url = reverse('userpreferences-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['language'], 'en')
        self.assertTrue(response.data[0]['accessibility_mode'])

    def test_update_user_preferences(self):
        prefs = UserPreferences.objects.create(user=self.user, preferred_channels=['email'], language='en', accessibility_mode=True)
        url = reverse('userpreferences-detail', args=[prefs.id])
        data = {'preferred_channels': ['sms', 'push'], 'language': 'fr', 'accessibility_mode': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['language'], 'fr')
        self.assertFalse(response.data['accessibility_mode'])
