
from django.db import models
from django.conf import settings

class LoginActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='login_activities')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=256, null=True, blank=True)
    session_key = models.CharField(max_length=64, null=True, blank=True)
    def __str__(self):
        user = getattr(self, 'user', None)
        username = getattr(user, 'username', str(user)) if user else str(self.pk)
        return f"{username} - {self.timestamp}"

class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preference')
    email = models.BooleanField(default=True)
    sms = models.BooleanField(default=False)
    in_app = models.BooleanField(default=True)
    def __str__(self):
        user = getattr(self, 'user', None)
        username = getattr(user, 'username', str(user)) if user else str(self.pk)
        return f"Notification preferences for {username}"

class NotificationDeliveryLog(models.Model):
    """Stores each delivery attempt for a notification, including status, channel, error, and audit info."""
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE, related_name='delivery_logs')
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32)  # delivered, failed, retrying
    channel = models.CharField(max_length=32)  # email, sms, websocket
    error_message = models.TextField(null=True, blank=True)
    user_agent = models.CharField(max_length=256, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

class Notification(models.Model):
    TYPE_CHOICES = [
        ("info", "Info"),
        ("success", "Success"),
        ("error", "Error"),
        ("urgent", "Urgent"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="info")
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Delivery audit fields
    delivery_status = models.CharField(max_length=32, default="pending")  # pending, delivered, failed, retrying
    last_attempt = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user}: {self.message}"

class StudentProfile(models.Model):
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=64, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    program = models.CharField(max_length=100)
    year_of_study = models.PositiveIntegerField()
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    account_status = models.CharField(max_length=32, default='active')  # active, suspended, graduated, etc.
    emergency_contact = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    id_card_downloaded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # self.user is a OneToOneField to User, so access as self.user.get_full_name() if available
        user = getattr(self, 'user', None)
        if user:
            name = getattr(user, 'get_full_name', lambda: str(user))()
            username = getattr(user, 'username', str(user))
            return f"{name} ({username})"
        return str(self.pk)


class IDCardReplacementRequest(models.Model):
    REASON_CHOICES = [
        ("lost", "Lost"),
        ("stolen", "Stolen"),
        ("damaged", "Damaged"),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='id_card_requests')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending')
    admin_comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Defensive: student.user should exist, but check for attribute
        student = getattr(self, 'student', None)
        user = getattr(student, 'user', None)
        username = getattr(user, 'username', str(user)) if user else str(student)
        return f"Request by {username} ({self.reason}) - {self.status}"


# Create your models here.
