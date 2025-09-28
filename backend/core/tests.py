from django.test import TestCase
from .models import StudentProfile

class StudentIDGenerationTests(TestCase):
    def setUp(self):
        from .models import CustomUser
        self.user1 = CustomUser.objects.create(email='u1@example.com', first_name='A', last_name='B')
        self.user2 = CustomUser.objects.create(email='u2@example.com', first_name='C', last_name='D')
        self.user3 = CustomUser.objects.create(email='u3@example.com', first_name='E', last_name='F')
        self.user4 = CustomUser.objects.create(email='u4@example.com', first_name='G', last_name='H')
        self.user5 = CustomUser.objects.create(email='u5@example.com', first_name='I', last_name='J')

    def test_sequential_ids_same_year(self):
        s1 = StudentProfile.objects.create(user=self.user1, program='BIT', year=2025, contact_info='A', emergency_contact='B', gpa=3.5)
        s2 = StudentProfile.objects.create(user=self.user2, program='BIT', year=2025, contact_info='C', emergency_contact='D', gpa=3.6)
        self.assertTrue(s1.student_id.endswith('00001'))
        self.assertTrue(s2.student_id.endswith('00002'))
        self.assertNotEqual(s1.student_id, s2.student_id)

    def test_sequence_resets_different_years(self):
        s1 = StudentProfile.objects.create(user=self.user1, program='BIT', year=2025, contact_info='A', emergency_contact='B', gpa=3.5)
        s2 = StudentProfile.objects.create(user=self.user2, program='BIT', year=2026, contact_info='C', emergency_contact='D', gpa=3.6)
        self.assertTrue(s1.student_id.endswith('00001'))
        self.assertTrue(s2.student_id.endswith('00001'))
        self.assertNotEqual(s1.student_id, s2.student_id)

    def test_no_duplicates_concurrent(self):
        import threading
        from django.db import connection
        users = [self.user1, self.user2, self.user3, self.user4, self.user5]
        results = []
        def create_student(user):
            s = StudentProfile.objects.create(user=user, program='BIT', year=2027, contact_info='A', emergency_contact='B', gpa=3.5)
            results.append(s.student_id)
        if connection.vendor == 'sqlite':
            # Run sequentially for SQLite
            for user in users:
                create_student(user)
        else:
            threads = [threading.Thread(target=create_student, args=(user,)) for user in users]
            for t in threads: t.start()
            for t in threads: t.join()
        self.assertEqual(len(set(results)), 5)
