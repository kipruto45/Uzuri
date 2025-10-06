
from django.db import models
from django.conf import settings
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
    # Link to the project's user model so tests that pass User instances work.
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_cards')

    def __init__(self, *args, **kwargs):
        # Accept legacy kwargs used in tests: 'card_type' -> 'exam_type', 'file' -> 'supporting_document'
        if 'card_type' in kwargs and 'exam_type' not in kwargs:
            kwargs['exam_type'] = kwargs.pop('card_type')
        if 'file' in kwargs and 'supporting_document' not in kwargs:
            kwargs['supporting_document'] = kwargs.pop('file')
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # No conversion to StudentProfile here; keep relation to AUTH_USER_MODEL
        super().save(*args, **kwargs)
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

    # Compatibility properties expected by older tests
    @property
    def card_type(self):
        return self.exam_type

    @card_type.setter
    def card_type(self, value):
        self.exam_type = value

    @property
    def file(self):
        return self.supporting_document

    @file.setter
    def file(self, value):
        self.supporting_document = value

# Create your models here.
