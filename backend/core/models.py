# --- Student Feature Models ---
# Move these to the end of the file after all referenced models are defined
from django.db import models
from django.utils import timezone
from .models_shared import CustomUser, CustomUserManager, StudentProfile, Disability, StudyMode

class Role(models.Model):
    STUDENT = 'Student'
    LECTURER = 'Lecturer'
    FINANCE_STAFF = 'Finance Staff'
    REGISTRAR = 'Registrar'
    SYSTEM_ADMIN = 'System Administrator'
    PARENT_GUARDIAN = 'Parent/Guardian'
    GUEST = 'Guest'
    SUPPORT_STAFF = 'Support Staff'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (LECTURER, 'Lecturer'),
        (FINANCE_STAFF, 'Finance Staff'),
        (REGISTRAR, 'Registrar'),
        (SYSTEM_ADMIN, 'System Administrator'),
        (PARENT_GUARDIAN, 'Parent/Guardian'),
        (GUEST, 'Guest'),
        (SUPPORT_STAFF, 'Support Staff'),
    ]
    name = models.CharField(max_length=32, unique=True, choices=ROLE_CHOICES, default=None, null=True, blank=True)

    def __str__(self):
        return self.name





        return f"Profile: {email}"


# --- Academic Models ---
class Program(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

class Unit(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    credits = models.IntegerField()

class Registration(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

class Transcript(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='transcripts/')
    created_at = models.DateTimeField(auto_now_add=True)

class Grade(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    remarks = models.TextField(blank=True)

class Assignment(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True)

# --- Finance Models ---
class Invoice(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, default='unpaid')

class Transaction(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    reference = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

class Receipt(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    file = models.FileField(upload_to='receipts/')
    issued_at = models.DateTimeField(auto_now_add=True)

class Scholarship(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    awarded_at = models.DateTimeField(auto_now_add=True)

# --- Hostel & Leave ---
class HostelApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

class LeaveRequest(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)

# --- Notifications & Messaging ---
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=20)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

# --- Admin & System ---
class AuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='core_audit_logs')
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

class AdminActionLog(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

class SystemMetric(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)

class ExamCard(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=32)  # ordinary/supplementary/special
    file = models.FileField(upload_to='exam_cards/')
    issued_at = models.DateTimeField(auto_now_add=True)

class LecturerEvaluation(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role__name': 'Lecturer'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

class DisciplinaryCase(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    case_details = models.TextField()
    verdict = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=32, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class FieldAttachment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    organization = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100)
    evaluation = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=32, default='pending')

class Clearance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    stage = models.CharField(max_length=32)  # library, finance, registrar, hostel
    status = models.CharField(max_length=32, default='pending')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

class GraduationApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    eligibility_status = models.CharField(max_length=32, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

class Timetable(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    semester = models.CharField(max_length=32)
    file = models.FileField(upload_to='timetables/')
    generated_at = models.DateTimeField(auto_now_add=True)

class EMasomoMaterial(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='e_masomo/')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)