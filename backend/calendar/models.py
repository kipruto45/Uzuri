from django.db import models
from django.conf import settings
from django.utils import timezone

class CalendarEvent(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('finance', 'Finance'),
        ('hostel', 'Hostel'),
        ('personal', 'Personal'),
        ('university', 'University'),
    ]
    COLOR_MAP = {
        'academic': 'blue',
        'finance': 'green',
        'hostel': 'purple',
        'personal': 'yellow',
        'university': 'grey',
    }
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=16, default='grey')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    recurrence = models.JSONField(default=dict, blank=True)  # e.g. {type: 'weekly', interval: 1, days: [1,3], end_date: ...}
    location = models.CharField(max_length=255, blank=True)
    related_module = models.CharField(max_length=64, blank=True, null=True)
    related_object_id = models.IntegerField(blank=True, null=True)
    notification_settings = models.JSONField(default=list, blank=True)  # e.g. ["24h", "1h", "10m"]
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_events')
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_events', blank=True)
    is_personal = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.color = self.COLOR_MAP.get(self.category, 'grey')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.category}) - {self.start_time:%Y-%m-%d %H:%M}"

class CalendarEventAuditLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('shared', 'Shared'),
        ('exported', 'Exported'),
    ]
    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=16, choices=ACTION_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.event.title} - {self.action} by {self.user} at {self.timestamp}"
