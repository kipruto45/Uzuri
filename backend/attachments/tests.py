
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Attachment
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class AttachmentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user@example.com', 'pass', first_name='Test', last_name='User')
        self.client.force_authenticate(self.user)

    def test_upload_attachment(self):
        from rest_framework.reverse import reverse
        file = SimpleUploadedFile('test.txt', b'hello world')
        data = {'file': file, 'description': 'Test file'}
        url = reverse('attachment-list')
        resp = self.client.post(url, data, format='multipart', follow=True)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_soft_delete_and_restore(self):
        from rest_framework.reverse import reverse
        file = SimpleUploadedFile('test2.txt', b'hello again')
        url = reverse('attachment-list')
        resp = self.client.post(url, {'file': file}, format='multipart', follow=True)
        # Handle resp.data as list or dict
        if isinstance(resp.data, list) and len(resp.data) > 0 and 'id' in resp.data[0]:
            att_id = resp.data[0]['id']
        elif isinstance(resp.data, dict) and 'id' in resp.data:
            att_id = resp.data['id']
        else:
            resp_json = resp.json()
            if isinstance(resp_json, list) and len(resp_json) > 0:
                att_id = resp_json[0].get('id')
            elif isinstance(resp_json, dict):
                att_id = resp_json.get('id')
            else:
                self.fail('Attachment creation response returned empty list')
        soft_delete_url = f'/api/attachments/attachments/{att_id}/soft_delete/'
        resp2 = self.client.post(soft_delete_url, follow=True)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        restore_url = f'/api/attachments/attachments/{att_id}/restore/'
        resp3 = self.client.post(restore_url, follow=True)
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
