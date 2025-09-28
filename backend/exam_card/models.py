
from django.db import models
from my_profile.models import StudentProfile
from unit_registration.models import UnitRegistration, UnitRegistrationItem
from finance_registration.models import FinanceRegistration

# Audit and analytics for exam card events
class ExamCardEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('generated', 'Generated'),
        ('downloaded', 'Downloaded'),
        ('verified', 'Verified'),
        ('blocked', 'Blocked'),
        ('unblocked', 'Unblocked'),
        ('override', 'Override'),
    ]
    card = models.ForeignKey('ExamCard', on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=16, choices=EVENT_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('my_profile.StudentProfile', on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event_type} {self.card} {self.timestamp}"

EXAM_TYPE_CHOICES = [
    ('ordinary', 'Ordinary'),
    ('special', 'Special'),
    ('supplementary', 'Supplementary'),
    ('retake', 'Retake'),
]

class ExamCard(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='exam_cards')
    semester = models.CharField(max_length=16)
    exam_type = models.CharField(max_length=16, choices=EXAM_TYPE_CHOICES)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='exam_cards/qrcodes/', null=True, blank=True)
    barcode = models.ImageField(upload_to='exam_cards/barcodes/', null=True, blank=True)
    download_history = models.JSONField(default=list, blank=True)  # Track reprints
    reprint_count = models.PositiveIntegerField(default=0)
    approved_by_registrar = models.BooleanField(default=False)
    finance_confirmed = models.BooleanField(default=False)
    override_reason = models.TextField(blank=True)
    supporting_document = models.FileField(upload_to='exam_cards/supporting_docs/', null=True, blank=True, help_text="Supporting document for special exam card")
    failed_units = models.JSONField(default=list, blank=True, help_text="List of failed units for supplementary card")
    exam_schedule = models.JSONField(default=list, blank=True, help_text="Exam schedule for this card")
    history = models.JSONField(default=list, blank=True, help_text="Tracking and history for special exam approvals")

    def __str__(self):
        return f"ExamCard {self.student} {self.semester} {self.exam_type}"

# Create your models here.
