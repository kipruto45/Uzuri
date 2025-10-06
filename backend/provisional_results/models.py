from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class GradingScale(models.Model):
    grade = models.CharField(max_length=2)
    min_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.grade}: {self.min_score}-{self.max_score} ({self.description})"

class Result(models.Model):
    STATUS_CHOICES = [
        ("provisional", "Provisional"),
        ("final", "Final"),
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit_code = models.CharField(max_length=20)
    unit_name = models.CharField(max_length=255)
    academic_hours = models.PositiveIntegerField()
    marks = models.FloatField()
    grade = models.CharField(max_length=2)
    semester = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='provisional')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_secure = models.BooleanField(default=True)
    audit_log = models.TextField(blank=True, default='')
    # Verification workflow
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='verified_results', on_delete=models.SET_NULL)
    verified_at = models.DateTimeField(null=True, blank=True)
    # Locking
    is_locked = models.BooleanField(default=False)
    # Versioning
    version = models.PositiveIntegerField(default=1)
    previous_version = models.ForeignKey('self', null=True, blank=True, related_name='next_versions', on_delete=models.SET_NULL)
    # Student comments/appeals
    student_comment = models.TextField(blank=True, default='')
    appeal_status = models.CharField(max_length=20, default='none')
    # Download tracking
    last_downloaded_at = models.DateTimeField(null=True, blank=True)
    last_downloaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='downloaded_results', on_delete=models.SET_NULL)
    # Notification preferences
    notify_email = models.BooleanField(default=True)
    notify_sms = models.BooleanField(default=True)
    notify_in_app = models.BooleanField(default=True)
    # Multi-language support
    description_en = models.TextField(blank=True, default='')
    description_fr = models.TextField(blank=True, default='')
    description_sw = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.student} - {self.unit_code} ({self.semester} {self.year})"

    @classmethod
    def calculate_gpa(cls, student, semester=None, year=None):
        results = cls.objects.filter(student=student)
        if semester:
            results = results.filter(semester=semester)
        if year:
            results = results.filter(year=year)
        total_points = 0
        total_hours = 0
        for r in results:
            points = cls.grade_to_points(r.grade)
            total_points += points * r.academic_hours
            total_hours += r.academic_hours
        return round(total_points / total_hours, 2) if total_hours else 0

    @classmethod
    def calculate_average(cls, student, semester=None, year=None):
        results = cls.objects.filter(student=student)
        if semester:
            results = results.filter(semester=semester)
        if year:
            results = results.filter(year=year)
        avg = results.aggregate(models.Avg('marks'))['marks__avg']
        return round(avg, 2) if avg else 0

    @staticmethod
    def grade_to_points(grade):
        # Example mapping, adjust as needed
        mapping = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
        return mapping.get(grade, 0)

    # Verification workflow
    def verify(self, user):
        self.is_verified = True
        self.verified_by = user
        self.verified_at = timezone.now()
        self.is_locked = True
        self.save()
        self.log_action(f"Verified by {user}")

    def reject(self, user):
        self.is_verified = False
        self.verified_by = user
        self.verified_at = timezone.now()
        self.is_locked = False
        self.save()
        self.log_action(f"Rejected by {user}")

    # Versioning
    def save(self, *args, **kwargs):
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)

    # Audit log
    def log_action(self, action):
        entry = f"{timezone.now()}: {action}\n"
        self.audit_log += entry
        self.save(update_fields=['audit_log'])

    # Download tracking
    def track_download(self, user):
        self.last_downloaded_at = timezone.now()
        self.last_downloaded_by = user
        self.save(update_fields=['last_downloaded_at', 'last_downloaded_by'])
        self.log_action(f"Downloaded by {user}")

    # Analytics
    @classmethod
    def grade_distribution(cls, student, semester=None, year=None):
        results = cls.objects.filter(student=student)
        if semester:
            results = results.filter(semester=semester)
        if year:
            results = results.filter(year=year)
        dist = {}
        for r in results:
            dist[r.grade] = dist.get(r.grade, 0) + 1
        return dist

    @classmethod
    def performance_trend(cls, student):
        results = cls.objects.filter(student=student).order_by('year', 'semester')
        trend = []
        for r in results:
            trend.append({'semester': r.semester, 'year': r.year, 'marks': r.marks, 'grade': r.grade})
        return trend

class Recommendation(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} ({self.semester} {self.year})"

# Signals for notifications and audit trail
from my_profile.tasks import send_notification

@receiver(post_save, sender=Result)
def result_saved(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    context = {
        'name': instance.student.get_full_name(),
        'semester': instance.semester,
        'unit_code': instance.unit_code,
    }
    channels = []
    if instance.notify_email:
        channels.append('email')
    if instance.notify_sms:
        channels.append('sms')
    if instance.notify_in_app:
        channels.append('in_app')
    send_notification.delay(instance.student.email, f'result_{action}', context, channels)
    instance.log_action(f"Result {action} by {instance.student} for {instance.unit_code} ({instance.semester} {instance.year})")

@receiver(post_delete, sender=Result)
def result_deleted(sender, instance, **kwargs):
    context = {
        'name': instance.student.get_full_name(),
        'semester': instance.semester,
        'unit_code': instance.unit_code,
    }
    channels = []
    if instance.notify_email:
        channels.append('email')
    if instance.notify_sms:
        channels.append('sms')
    if instance.notify_in_app:
        channels.append('in_app')
    send_notification.delay(instance.student.email, 'result_deleted', context, channels)
    # Could log deletion elsewhere
