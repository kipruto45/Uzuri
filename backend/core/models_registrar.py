from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import models
from .models_shared import CustomUser, StudentProfile, Disability, StudyMode

class RegistrarRole(models.TextChoices):
    HEAD = 'head', 'Registrar – Academics'
    OFFICER = 'officer', 'Registrar Officer'
    ASSISTANT = 'assistant', 'Registrar Assistant'

class RegistrarProfile(models.Model):
    def __str__(self):
        return f"{self.user.email} ({self.get_role_display()})"
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=RegistrarRole.choices)

class DisabilityCategory(models.Model):
    def __str__(self):
        return f"{self.name} ({self.cue_code})"
    name = models.CharField(max_length=32, unique=True)
    cue_code = models.CharField(max_length=8, blank=True)

# Use the shared Disability and StudyMode models from core.models_shared to avoid
# duplicate model registrations which cause runtime conflicts during tests.
# The shared models are imported at the top of this file.

class StudentAdmission(models.Model):
    def clean(self):
        # Only one active study mode per student
        if StudentAdmission.objects.filter(student=self.student, study_mode=self.study_mode).exclude(pk=self.pk).exists():
            from django.core.exceptions import ValidationError
            raise ValidationError("Student already has this study mode assigned.")
        # Validate file uploads
        for field in ['kcse_certificate', 'result_slip', 'id_passport', 'admission_letter']:
            f = getattr(self, field)
            if f and not f.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise ValidationError(f"{field} must be a PDF or image file.")
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.student} ({self.intake_year} - {self.program})"
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    intake_year = models.IntegerField()
    program = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    kcse_certificate = models.FileField(upload_to='kcse/', blank=True, null=True)
    result_slip = models.FileField(upload_to='results/', blank=True, null=True)
    id_passport = models.FileField(upload_to='ids/', blank=True, null=True)
    admission_letter = models.FileField(upload_to='admission_letters/', blank=True, null=True)
    study_mode = models.ForeignKey(StudyMode, on_delete=models.SET_NULL, null=True)
    disability = models.ForeignKey(Disability, on_delete=models.SET_NULL, null=True, blank=True)

class LeaveOfAbsence(models.Model):
    def approve(self, registrar):
        self.status = 'approved'
        self.approved_by = registrar
        self.approved_at = timezone.now()
        self.save()
        # Notification logic
        send_mail(
            'Leave of Absence Approved',
            f'Your leave of absence has been approved.',
            settings.DEFAULT_FROM_EMAIL,
            [self.student.user.email],
        )
    def __str__(self):
        return f"{self.student} - {self.status} ({self.requested_at:%Y-%m-%d})"
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=16, choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected'),('deferred','Deferred'),('on_leave','On Leave')], default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(RegistrarProfile, on_delete=models.SET_NULL, null=True, blank=True)

class TransferRequest(models.Model):
    def approve(self, registrar):
        self.status = 'approved'
        self.approved_by = registrar
        self.approved_at = timezone.now()
        self.save()
        send_mail(
            'Transfer Request Approved',
            f'Your transfer from {self.from_program} to {self.to_program} has been approved.',
            settings.DEFAULT_FROM_EMAIL,
            [self.student.user.email],
        )
    def __str__(self):
        return f"{self.student} {self.from_program}→{self.to_program} ({self.status})"
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    from_program = models.CharField(max_length=100)
    to_program = models.CharField(max_length=100)
    status = models.CharField(max_length=16, choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(RegistrarProfile, on_delete=models.SET_NULL, null=True, blank=True)

class GraduationClearance(models.Model):
    def approve(self, registrar):
        self.status = 'approved'
        self.checked_by = registrar
        self.checked_at = timezone.now()
        self.save()
        send_mail(
            'Graduation Clearance Approved',
            f'You are now eligible for graduation.',
            settings.DEFAULT_FROM_EMAIL,
            [self.student.user.email],
        )
    # model fields for GraduationClearance
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=[('pending','Pending'),('eligible','Eligible'),('ineligible','Ineligible'),('approved','Approved')], default='pending')
    checked_at = models.DateTimeField(auto_now_add=True)
    checked_by = models.ForeignKey(RegistrarProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.student} ({self.status})"


class RegistrarAuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)
    encrypted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.action} @ {self.timestamp:%Y-%m-%d %H:%M}"


# Signals for audit logging (placed after model definitions)
@receiver(post_save, sender=LeaveOfAbsence)
def log_leave_of_absence(sender, instance, created, **kwargs):
    if created:
        RegistrarAuditLog.objects.create(
            user=instance.student.user,
            action='Leave of Absence Requested',
            details=f'Reason: {instance.reason}',
        )
    elif instance.status == 'approved':
        RegistrarAuditLog.objects.create(
            user=instance.student.user,
            action='Leave of Absence Approved',
            details=f'Approved by: {instance.approved_by}',
        )


@receiver(post_save, sender=TransferRequest)
def log_transfer_request(sender, instance, created, **kwargs):
    if created:
        RegistrarAuditLog.objects.create(
            user=instance.student.user,
            action='Transfer Requested',
            details=f'From: {instance.from_program} To: {instance.to_program}',
        )
    elif instance.status == 'approved':
        RegistrarAuditLog.objects.create(
            user=instance.student.user,
            action='Transfer Approved',
            details=f'Approved by: {instance.approved_by}',
        )


@receiver(post_save, sender=GraduationClearance)
def log_graduation_clearance(sender, instance, created, **kwargs):
    if created:
        RegistrarAuditLog.objects.create(
            user=instance.student.user,
            action='Graduation Clearance Created',
            details=f'Status: {instance.status}',
        )
    elif instance.status == 'approved':
        RegistrarAuditLog.objects.create(
            user=instance.student.user,
            action='Graduation Clearance Approved',
            details=f'Checked by: {instance.checked_by}',
        )
