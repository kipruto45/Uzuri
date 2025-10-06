from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse
from rest_framework import status

User = get_user_model()

class AttachmentOwnerRegressionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='owner@example.com', password='pass')
        self.client.force_authenticate(self.user)

    def test_owner_can_access_new_attachment_and_soft_delete_restore(self):
        file = SimpleUploadedFile('t.txt', b'content')
        url = reverse('attachment-list')
        resp = self.client.post(url, {'file': file}, format='multipart', follow=True)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # extract id
        data = resp.data if isinstance(resp.data, dict) else (resp.data[0] if isinstance(resp.data, list) and resp.data else {})
        att_id = data.get('id')
        self.assertIsNotNone(att_id)
        soft_delete_url = f'/api/attachments/attachments/{att_id}/soft_delete/'
        resp2 = self.client.post(soft_delete_url, follow=True)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        restore_url = f'/api/attachments/attachments/{att_id}/restore/'
        resp3 = self.client.post(restore_url, follow=True)
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
