from django.test import TestCase
from .models_registrar import *
from .models import CustomUser, StudentProfile

class RegistrarModuleTests(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create(email='admin@uzuri.ac.ke', first_name='Admin', last_name='User')
        self.registrar = RegistrarProfile.objects.create(user=self.admin, role=RegistrarRole.HEAD)
        self.student_user = CustomUser.objects.create(email='student@uzuri.ac.ke', first_name='Student', last_name='User')
        self.student = StudentProfile.objects.create(user=self.student_user, program='CS', year=2025, contact_info='A', emergency_contact='B', gpa=3.5)
        self.study_mode = StudyMode.objects.create(name='full_time')
        self.disability = Disability.objects.create(student=self.student, category='physical', support_needs='extra time')
        self.admission = StudentAdmission.objects.create(student=self.student, intake_year=2025, program='CS', campus='Main', department='Computing', study_mode=self.study_mode, disability=self.disability)

    def test_registrar_profile(self):
        self.assertEqual(self.registrar.role, RegistrarRole.HEAD)

    def test_student_admission(self):
        self.assertEqual(self.admission.intake_year, 2025)
        self.assertEqual(self.admission.study_mode.name, 'full_time')
        self.assertEqual(self.admission.disability.category, 'physical')

    def test_leave_of_absence(self):
        leave = LeaveOfAbsence.objects.create(student=self.student, reason='Medical', status='pending')
        self.assertEqual(leave.status, 'pending')

    def test_transfer_request(self):
        transfer = TransferRequest.objects.create(student=self.student, from_program='CS', to_program='BIT', status='pending')
        self.assertEqual(transfer.status, 'pending')

    def test_graduation_clearance(self):
        clearance = GraduationClearance.objects.create(student=self.student, status='pending')
        self.assertEqual(clearance.status, 'pending')

    def test_audit_log(self):
        log = RegistrarAuditLog.objects.create(user=self.admin, action='Created student', details='Student record created', encrypted=True)
        self.assertTrue(log.encrypted)
