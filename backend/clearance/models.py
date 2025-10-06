from django.db import models
from django.conf import settings


class ClearanceDepartment(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ClearanceRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    ]
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clearance_requests"
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending")
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True)
    # Automated eligibility checks
    is_fees_cleared = models.BooleanField(default=False)
    is_library_cleared = models.BooleanField(default=False)
    is_disciplinary_cleared = models.BooleanField(default=False)
    is_hostel_cleared = models.BooleanField(default=False)
    is_other_cleared = models.BooleanField(default=False)
    is_eligible = models.BooleanField(default=False)
    soft_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.student} - {self.status}"


class ClearanceWorkflowLog(models.Model):
    request = models.ForeignKey(
        "ClearanceRequest", on_delete=models.CASCADE, related_name="workflow_logs"
    )
    status = models.CharField(max_length=32)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    remarks = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request} - {self.status} at {self.timestamp}"


class ClearanceNotification(models.Model):
    request = models.ForeignKey(
        "ClearanceRequest", on_delete=models.CASCADE, related_name="notifications"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=32, default="system")
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.recipient} for {self.request}"


class ClearanceApproval(models.Model):
    request = models.ForeignKey(
        "ClearanceRequest", on_delete=models.CASCADE, related_name="approvals"
    )
    department = models.ForeignKey(
        "ClearanceDepartment", on_delete=models.CASCADE, related_name="approvals"
    )
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clearance_approvals",
    )
    remarks = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.request} - {self.department} ({'Approved' if self.approved else 'Pending'})"


class ClearanceComment(models.Model):
    approval = models.ForeignKey(
        "ClearanceApproval", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.approval}"


class ClearanceDigitalSignature(models.Model):
    approval = models.OneToOneField(
        "ClearanceApproval", on_delete=models.CASCADE, related_name="digital_signature"
    )
    signed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    signature_file = models.FileField(
        upload_to="clearance_signatures/%Y/%m/%d/", null=True, blank=True
    )
    signed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signature by {self.signed_by} on {self.approval}"


class ClearanceDocument(models.Model):
    request = models.ForeignKey(
        "ClearanceRequest", on_delete=models.CASCADE, related_name="documents"
    )
    document = models.FileField(upload_to="clearance_documents/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_clearance_documents",
    )
    department = models.ForeignKey(
        "ClearanceDepartment",
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True,
    )
    soft_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Document for {self.request} ({self.department})"


class ClearanceAuditTrail(models.Model):
    request = models.ForeignKey(
        "ClearanceRequest", on_delete=models.CASCADE, related_name="audit_trails"
    )
    action = models.CharField(max_length=64)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.actor} on {self.request} at {self.timestamp}"
