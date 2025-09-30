from django.test import TestCase
from django.contrib.auth import get_user_model
from .models_shared import StudentProfile

User = get_user_model()

class StudentIDRegressionTests(TestCase):
    def test_student_id_format_and_sequence(self):
        u1 = User.objects.create_user(email='s1@example.com', password='pass')
        u2 = User.objects.create_user(email='s2@example.com', password='pass')
        s1 = StudentProfile.objects.create(user=u1, program='BIT', year=2025, contact_info='a', emergency_contact='b', gpa=3.0)
        s2 = StudentProfile.objects.create(user=u2, program='BIT', year=2025, contact_info='c', emergency_contact='d', gpa=3.2)
        self.assertTrue(s1.student_id.startswith('UZ-2025-BI-'))
        self.assertTrue(s2.student_id.startswith('UZ-2025-BI-'))
        self.assertNotEqual(s1.student_id, s2.student_id)
        # Ensure zero-padded suffix
        self.assertRegex(s1.student_id, r"UZ-2025-BI-\d{5}")
