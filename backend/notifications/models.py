from django.conf import settings
from django.db import models
from django.utils import timezone


class UserConsent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    consent_type = models.CharField(max_length=64)
    consent_given = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=128)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)


class UserPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    preferred_channels = models.JSONField(default=list)  # e.g. ['email', 'sms', 'push']
    language = models.CharField(max_length=8, default='en')
    accessibility_mode = models.BooleanField(default=False)


class NotificationCategory(models.TextChoices):
    FINANCE = 'finance', 'Finance'
    UNITS = 'units', 'Units'
    EXAMS = 'exams', 'Exams'
    ASSIGNMENTS = 'assignments', 'Assignments'
    TIMETABLE = 'timetable', 'Timetable'
    HOSTEL = 'hostel', 'Hostel'
    CLEARANCE = 'clearance', 'Clearance'
    GRADUATION = 'graduation', 'Graduation'
    GENERAL = 'general', 'General'


class NotificationUrgency(models.TextChoices):
    INFO = 'info', 'Info'
    WARNING = 'warning', 'Warning'
    URGENT = 'urgent', 'Urgent'


class NotificationChannel(models.TextChoices):
    IN_APP = 'in_app', 'In-App'
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PUSH = 'push', 'Push Notification'


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='advanced_notifications')
    category = models.CharField(max_length=32, choices=NotificationCategory.choices)
    type = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    message = models.TextField()
    urgency = models.CharField(max_length=16, choices=NotificationUrgency.choices, default=NotificationUrgency.INFO)
    channels = models.JSONField(default=list)  # e.g. ["in_app", "email"]
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    action_links = models.JSONField(default=list, blank=True)  # e.g. [{"label": "View Invoice", "url": "/finance/invoice/123/"}]
    language = models.CharField(max_length=8, default='en')
    personalized_context = models.JSONField(default=dict, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    group = models.CharField(max_length=32, blank=True)  # e.g. All, Academics, Finance, Exams, General
    requires_ack = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=False)
    escalation_sent = models.BooleanField(default=False)
    escalation_at = models.DateTimeField(null=True, blank=True)
    offline_queued = models.BooleanField(default=False)
    offline_synced = models.BooleanField(default=False)
    push_token = models.CharField(max_length=256, blank=True, null=True)
    push_status = models.CharField(max_length=32, default='pending')  # pending, sent, failed

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'category']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.user} - {self.title} ({self.category})"


class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    channels = models.JSONField(default=list)  # e.g. ["in_app", "email"]
    categories = models.JSONField(default=list)  # e.g. ["finance", "exams"]
    language = models.CharField(max_length=8, default='en')
    receive_urgent_sms = models.BooleanField(default=True)
    receive_push = models.BooleanField(default=True)


class NotificationAuditLog(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='audit_logs')
    channel = models.CharField(max_length=16, choices=NotificationChannel.choices)
    status = models.CharField(max_length=32)  # success, failed, retried
    attempt = models.IntegerField(default=1)
    response = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class NotificationAnalytics(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='analytics')
    opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)
    ignored = models.BooleanField(default=False)
    ignored_at = models.DateTimeField(null=True, blank=True)


class NotificationSchedule(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='schedules')
    scheduled_for = models.DateTimeField()
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)


class NotificationGroup(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notification_groups')


class NotificationActionResponse(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    response = models.CharField(max_length=255)
    responded_at = models.DateTimeField(auto_now_add=True)


class NotificationDeliveryLog(models.Model):
    """Tracks delivery attempts and status for notifications."""
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="delivery_logs", null=True, blank=True
    )
    channel = models.CharField(max_length=16, choices=NotificationChannel.choices, blank=True, null=True)
    status = models.CharField(max_length=32)  # e.g. 'success', 'failed', 'queued'
    provider = models.CharField(max_length=64, blank=True)
    response = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nid = getattr(self, 'notification_id', None)
        return f"Delivery {self.status} for {nid if nid else 'unknown'} at {self.timestamp}"
