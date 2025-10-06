from django.contrib.auth import get_user_model
from django.utils import timezone
from notifications.models import UserConsent, AuditLog
from rest_framework.test import APITestCase

class AuditConsentTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='audituser', password='testpass')

    def test_consent_creation(self):
        consent = UserConsent.objects.create(user=self.user, consent_type='privacy', consent_given=True, timestamp=timezone.now())
        self.assertTrue(consent.consent_given)
        self.assertEqual(consent.consent_type, 'privacy')

    def test_audit_log(self):
        log = AuditLog.objects.create(user=self.user, action='login', details='User logged in', timestamp=timezone.now())
        self.assertEqual(log.action, 'login')
        self.assertIn('logged in', log.details)
