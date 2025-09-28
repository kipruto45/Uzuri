from django.test import TestCase
from lms.models import LMSCourse, LMSUser
from lms.sync import sync_courses, sync_users

class LMSSyncTest(TestCase):
    def test_sync_courses(self):
        # Simulate sync
        sync_courses()
        self.assertTrue(LMSCourse.objects.exists())

    def test_sync_users(self):
        # Simulate sync
        sync_users()
        self.assertTrue(LMSUser.objects.exists())
